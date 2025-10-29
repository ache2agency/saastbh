import chromadb
from sentence_transformers import SentenceTransformer
import os

class TBHardenVectorStore:
    def __init__(self):
        # Inicializar ChromaDB (persistente)
        self.client = chromadb.PersistentClient(path="./tbharden_db")
        self.collection = self.client.get_or_create_collection(name="tbharden_knowledge")
        
        # Modelo para embeddings (gratuito - se ejecuta localmente)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Vector Store inicializado correctamente")
    
    def add_documents(self, documents):
        """Agregar documentos a la base vectorial"""
        if not documents:
            return
            
        print(f"📚 Agregando {len(documents)} documentos a la base de datos...")
        
        # Generar embeddings
        embeddings = self.embedder.encode(documents).tolist()
        
        # Generar IDs únicos
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Agregar a ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            ids=ids
        )
        print("✅ Documentos agregados exitosamente")
    
    def search(self, query, n_results=3):
        """Buscar documentos similares"""
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedder.encode([query]).tolist()
            
            # Buscar en ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []

# Instancia global
vector_store = TBHardenVectorStore()