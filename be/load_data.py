from vector_store import vector_store

# Datos de ejemplo de metodología TB Harden (reemplaza con tus documentos reales)
documentos_ejemplo = [
    "TB Harden enfatiza la enseñanza comunicativa: aprender hablando en contextos reales.",
    "La pronunciación británica (RP) es fundamental en la metodología TB Harden.",
    "Estructura de clase típica: warm-up, presentation, practice, production, cool-down.",
    "Los errores son oportunidades de aprendizaje, no fallas a corregir inmediatamente.",
    "Uso de material auténtico como periódicos, canciones y videos reales.",
    "Enfoque en la autonomía del estudiante: enseñar a aprender, no solo contenido."
]

# Cargar los documentos
vector_store.add_documents(documentos_ejemplo)
print("✅ Datos de ejemplo cargados en ChromaDB")