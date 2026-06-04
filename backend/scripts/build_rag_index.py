import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.rag.engine import rag_engine

def build():
    print("Iniciando construccin del ndice RAG...")
    try:
        rag_engine.build_index(force_rebuild=True)
        print("ndice RAG construido exitosamente!")
    except Exception as e:
        print(f"Error construyendo el ndice: {e}")

if __name__ == "__main__":
    build()
