"""
Motor RAG (Retrieval-Augmented Generation) para el chatbot académico PUCESI.
Maneja la carga, fragmentación, embeddings y búsqueda semántica de documentos.
"""
import logging
import pickle
from typing import List, Tuple
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Motor RAG basado en FAISS + OpenAI Embeddings.
    Singleton: se instancia una sola vez y se reutiliza.
    """
    _instance = None
    _index = None
    _chunks = None  # Lista de textos correspondientes a cada vector
    _metadata = None  # Metadata de cada chunk (fuente, página, etc.)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_client(self):
        """Obtiene el cliente OpenAI configurado."""
        from openai import OpenAI
        return OpenAI(api_key=settings.OPENAI_API_KEY)

    def _excluded_sources(self) -> set:
        """Archivos locales que no deben entrar al RAG ni ser recuperados."""
        return set(getattr(settings, 'RAG_EXCLUDED_SOURCE_FILES', []))

    def _source_priority(self, source: str) -> int:
        """Prioriza documentos curados del proyecto sobre scraping web cambiante."""
        if source in {
            'informacion_institucional.txt',
            'puce_ibarra_info.txt',
            'campus_mapa_servicios.txt',
            'horarios_prerrequisitos_2026_01.txt',
        }:
            return 3
        if source == 'scraped_web_content.txt':
            return 2
        return 1

    def _source_type(self, source: str) -> str:
        if self._source_priority(source) >= 3:
            return 'documento_validado'
        if source == 'scraped_web_content.txt':
            return 'web_oficial_pucesi'
        return 'documento'

    def _documents_latest_mtime(self) -> float:
        docs_path = Path(settings.DOCUMENTS_PATH)
        if not docs_path.exists():
            return 0.0
        excluded_sources = self._excluded_sources()
        mtimes = [
            file_path.stat().st_mtime
            for file_path in docs_path.glob('**/*.txt')
            if file_path.name not in excluded_sources
        ]
        return max(mtimes, default=0.0)

    def _load_existing_index(self, index_path: Path, chunks_path: Path, metadata_path: Path) -> bool:
        import faiss

        if not (index_path.exists() and chunks_path.exists() and metadata_path.exists()):
            return False

        logger.info("Cargando índice FAISS existente...")
        self._index = faiss.read_index(str(index_path))
        with open(chunks_path, 'rb') as f:
            self._chunks = pickle.load(f)
        with open(metadata_path, 'rb') as f:
            self._metadata = pickle.load(f)
        logger.info(f"Índice cargado: {len(self._chunks)} chunks")
        return True

    def _get_embedding(self, text: str) -> List[float]:
        """Genera embedding para un texto usando OpenAI."""
        client = self.get_client()
        response = client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=text.replace('\n', ' ')
        )
        return response.data[0].embedding

    def _get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Genera embeddings para múltiples textos en batch."""
        client = self.get_client()
        response = client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=[t.replace('\n', ' ') for t in texts]
        )
        return [item.embedding for item in response.data]

    def build_index(self, force_rebuild: bool = False):
        """
        Construye o carga el índice FAISS desde los documentos institucionales.

        Args:
            force_rebuild: Si True, reconstruye aunque ya exista el índice.
        """
        import faiss
        import numpy as np

        index_path = Path(settings.FAISS_INDEX_PATH)
        chunks_path = index_path.parent / 'chunks.pkl'
        metadata_path = index_path.parent / 'metadata.pkl'

        index_is_fresh = (
            index_path.exists()
            and chunks_path.exists()
            and metadata_path.exists()
            and index_path.stat().st_mtime >= self._documents_latest_mtime()
        )

        # Cargar índice existente si no se fuerza reconstrucción y está actualizado.
        if not force_rebuild and index_is_fresh:
            self._load_existing_index(index_path, chunks_path, metadata_path)
            return

        # Construir desde cero
        logger.info("Construyendo índice RAG desde documentos...")
        all_chunks, all_metadata = self._load_and_chunk_documents()

        if not all_chunks:
            logger.warning("No se encontraron documentos para indexar.")
            return

        logger.info(f"Generando embeddings para {len(all_chunks)} chunks...")
        # Procesar en lotes de 100
        all_embeddings = []
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            embeddings = self._get_embeddings_batch(batch)
            all_embeddings.extend(embeddings)
            logger.info(f"  Embeddings: {min(i + batch_size, len(all_chunks))}/{len(all_chunks)}")

        # Crear índice FAISS
        dimension = len(all_embeddings[0])
        index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine con vectores normalizados)

        # Normalizar vectores para usar cosine similarity
        vectors = np.array(all_embeddings, dtype=np.float32)
        faiss.normalize_L2(vectors)
        index.add(vectors)

        # Guardar índice y chunks
        index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(index_path))
        with open(chunks_path, 'wb') as f:
            pickle.dump(all_chunks, f)
        with open(metadata_path, 'wb') as f:
            pickle.dump(all_metadata, f)

        self._index = index
        self._chunks = all_chunks
        self._metadata = all_metadata
        logger.info(f"✅ Índice RAG construido: {len(all_chunks)} chunks, dimensión {dimension}")

    def _load_and_chunk_documents(self) -> Tuple[List[str], List[dict]]:
        """
        Carga documentos desde la carpeta /documents y los fragmenta.
        Soporta archivos .txt (los documentos institucionales PUCESI).
        """
        docs_path = Path(settings.DOCUMENTS_PATH)
        chunk_size = settings.RAG_CHUNK_SIZE
        chunk_overlap = settings.RAG_CHUNK_OVERLAP

        all_chunks = []
        all_metadata = []

        if not docs_path.exists():
            logger.warning(f"Directorio de documentos no existe: {docs_path}")
            return [], []

        excluded_sources = self._excluded_sources()
        for file_path in sorted(docs_path.glob('**/*.txt')):
            if file_path.name in excluded_sources:
                logger.info(f"  Omitiendo fuente excluida del RAG: {file_path.name}")
                continue

            logger.info(f"  Procesando: {file_path.name}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # Fragmentar texto
                chunks = self._split_text(text, chunk_size, chunk_overlap)
                for j, chunk in enumerate(chunks):
                    if chunk.strip():
                        all_chunks.append(chunk)
                        all_metadata.append({
                            'source': file_path.name,
                            'source_type': self._source_type(file_path.name),
                            'priority': self._source_priority(file_path.name),
                            'chunk_index': j,
                            'total_chunks': len(chunks),
                        })

                logger.info(f"    → {len(chunks)} chunks generados")
            except Exception as e:
                logger.error(f"Error procesando {file_path}: {e}")

        return all_chunks, all_metadata

    def _split_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Fragmenta texto por palabras manteniendo overlap para contexto.
        Respeta párrafos cuando es posible.
        """
        # Dividir por párrafos primero
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        current_chunk = []
        current_size = 0

        for paragraph in paragraphs:
            words = paragraph.split()
            if current_size + len(words) > chunk_size and current_chunk:
                # Guardar chunk actual
                chunks.append(' '.join(current_chunk))
                # Overlap: conservar últimas palabras
                overlap_words = current_chunk[-overlap:] if overlap > 0 else []
                current_chunk = overlap_words
                current_size = len(overlap_words)

            current_chunk.extend(words)
            current_size += len(words)

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def search(self, query: str, top_k: int = None) -> List[dict]:
        """
        Búsqueda semántica en el índice FAISS.

        Args:
            query: Pregunta del usuario
            top_k: Número de resultados a retornar

        Returns:
            Lista de chunks relevantes con score y metadata
        """
        import faiss
        import numpy as np

        if self._index is None:
            logger.warning("Índice RAG no construido. Intentando cargar...")
            try:
                self.build_index()
            except Exception as e:
                logger.error(f"No se pudo reconstruir el índice RAG: {e}")
                index_path = Path(settings.FAISS_INDEX_PATH)
                loaded = self._load_existing_index(
                    index_path,
                    index_path.parent / 'chunks.pkl',
                    index_path.parent / 'metadata.pkl',
                )
                if not loaded:
                    return []
            if self._index is None:
                return []

        if top_k is None:
            top_k = settings.RAG_TOP_K

        # Generar embedding de la query
        query_embedding = np.array([self._get_embedding(query)], dtype=np.float32)
        faiss.normalize_L2(query_embedding)

        # Buscar más candidatos y luego reordenar por prioridad documental + similitud.
        search_k = min(max(top_k * 4, top_k), len(self._chunks))
        scores, indices = self._index.search(query_embedding, search_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or score < 0.3:  # Filtro de relevancia mínima
                continue
            source = self._metadata[idx]['source'] if self._metadata else 'desconocido'
            if source in self._excluded_sources():
                continue
            priority = self._source_priority(source)
            results.append({
                'content': self._chunks[idx],
                'score': float(score),
                'weighted_score': float(score) + (priority * 0.05),
                'source': source,
                'source_type': self._source_type(source),
                'priority': priority,
            })

        results.sort(key=lambda item: item['weighted_score'], reverse=True)
        results = results[:top_k]
        logger.debug(f"RAG search: {len(results)} resultados para '{query[:50]}'")
        return results

    def format_context(self, results: List[dict]) -> str:
        """Formatea los resultados RAG como contexto para el LLM."""
        if not results:
            return "No se encontró información relevante en los documentos institucionales."

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Fuente {i}: {result['source']} | tipo={result.get('source_type', 'documento')}]\n{result['content']}"
            )

        return "\n\n---\n\n".join(context_parts)


# Instancia global del motor RAG
rag_engine = RAGEngine()
