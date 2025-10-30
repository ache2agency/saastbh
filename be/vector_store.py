# be/vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer
import os
import logging

class VectorStore:
    def __init__(self, collection_name="tbl_activities"):
        print("🚀 Iniciando vector_store.py...")
        try:
            # Configura logging
            logging.basicConfig(level=logging.INFO)
            
            print("🔧 Inicializando ChromaDB...")
            # Usar cliente persistente
            self.chroma_client = chromadb.PersistentClient(path="./chroma_data")
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
            print("✅ Colección ChromaDB creada")
            
            # NO cargar el modelo aquí - carga perezosa
            self.model = None
            print("✅ VectorStore inicializado (modelo se cargará bajo demanda)")
            
        except Exception as e:
            print(f"❌ Error inicializando VectorStore: {e}")
            raise

    def get_embeddings(self, texts):
        """Carga el modelo solo cuando sea necesario"""
        if self.model is None:
            print("🔧 Cargando modelo de embeddings...")
            # Usar modelo más pequeño para ahorrar memoria
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Modelo de embeddings cargado")
        
        if isinstance(texts, str):
            texts = [texts]
        
        return self.model.encode(texts).tolist()

    def add_activity(self, activity_data):
        """Añadir actividad a la base vectorial"""
        try:
            embedding = self.get_embeddings(activity_data.get("description", ""))
            
            self.collection.add(
                embeddings=[embedding],
                documents=[str(activity_data)],
                metadatas=[activity_data],
                ids=[f"activity_{len(self.collection.get()['ids'])}"]
            )
            return True
        except Exception as e:
            print(f"Error añadiendo actividad: {e}")
            return False

    def search_similar(self, query, n_results=3):
        """Buscar actividades similares"""
        try:
            query_embedding = self.get_embeddings(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return None