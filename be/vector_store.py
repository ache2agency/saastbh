import chromadb
from sentence_transformers import SentenceTransformer
import os
import sys

# Forzar que los prints se vean en los logs de Render
print("🚀 Iniciando vector_store.py...", file=sys.stderr)

class TBHardenVectorStore:
    def __init__(self):
        try:
            print("🔧 Inicializando ChromaDB...", file=sys.stderr)
            # Inicializar ChromaDB (persistente)
            self.client = chromadb.PersistentClient(path="./tbharden_db")
            print("✅ Cliente ChromaDB creado", file=sys.stderr)
            
            self.collection = self.client.get_or_create_collection(name="tbharden_knowledge")
            print("✅ Colección ChromaDB creada", file=sys.stderr)
            
            # Modelo para embeddings
            print("🔧 Cargando modelo de embeddings...", file=sys.stderr)
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Vector Store inicializado correctamente", file=sys.stderr)
            
        except Exception as e:
            print(f"❌ ERROR en Vector Store: {e}", file=sys.stderr)
            # Crear una versión dummy para que no falle la importación
            self.collection = None
            self.embedder = None
    
    def add_documents(self, documents):
        """Agregar documentos a la base vectorial"""
        if not documents or not self.collection:
            return
            
        try:
            print(f"📚 Agregando {len(documents)} documentos...", file=sys.stderr)
            embeddings = self.embedder.encode(documents).tolist()
            ids = [f"doc_{i}" for i in range(len(documents))]
            
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                ids=ids
            )
            print("✅ Documentos agregados exitosamente", file=sys.stderr)
        except Exception as e:
            print(f"❌ Error agregando documentos: {e}", file=sys.stderr)
    
    def search(self, query, n_results=3):
        """Buscar documentos similares"""
        if not self.collection:
            return []
            
        try:
            query_embedding = self.embedder.encode([query]).tolist()
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}", file=sys.stderr)
            return []

# Instancia global con manejo de errores
try:
    vector_store = TBHardenVectorStore()
    print("🎉 Vector Store creado exitosamente", file=sys.stderr)
except Exception as e:
    print(f"💥 ERROR creando Vector Store: {e}", file=sys.stderr)
    # Crear un objeto dummy para evitar errores de importación
    vector_store = None