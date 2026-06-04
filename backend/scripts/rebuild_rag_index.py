import os
import sys
import django
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.rag.engine import rag_engine

def main():
    print("Iniciando reconstrucción del índice RAG...")
    try:
        # Forzar reconstrucción del índice FAISS
        rag_engine.build_index(force_rebuild=True)
        print("Indice RAG reconstruido exitosamente.")
    except Exception as e:
        print(f"Error reconstruyendo el indice: {e}")

if __name__ == "__main__":
    main()
