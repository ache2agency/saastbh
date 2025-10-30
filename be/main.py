import os
import sys
# Agregar esta línea para asegurar que Python encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI
from fpdf import FPDF
import uuid
from vector_store import vector_store

# El resto de tu código se mantiene igual...

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia esto a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "¡Hola! Tu backend está funcionando 🎉"}

# API key desde variable de entorno
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

class Prompt(BaseModel):
    mensaje: str

@app.post("/generar-clase")
def generar_clase(data: Prompt):
    try:
        # 1. Buscar en la base de conocimientos de TB Harden
        contexto_relevante = vector_store.search(data.mensaje, n_results=2)
        
        # 2. Crear prompt enriquecido con el contexto
        prompt_contextualizado = f"""
        Basándote en la metodología de TB Harden y este contexto específico:
        
        CONTEXTO TB HARDEN:
        {chr(10).join(contexto_relevante) if contexto_relevante else 'No se encontró contexto específico.'}
        
        SOLICITUD DEL USUARIO:
        {data.mensaje}
        
        Genera una clase estructurada siguiendo los principios de TB Harden.
        """
        
        # 3. Generar la clase con el contexto
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": "Eres un experto en enseñanza del inglés como T.B. Harden."},
                {"role": "user", "content": prompt_contextualizado}
            ]
        )
        return {"clase_generada": response.choices[0].message.content}
    except Exception as e:
        return {"error": f"No se pudo generar la clase: {str(e)}"}

@app.post("/descargar-pdf")
def descargar_pdf(data: Prompt):
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración mejorada
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Clase de Inglés Generada", ln=True, align='C')
    pdf.ln(10)
    
    # Contenido con mejor formato
    pdf.set_font("Arial", size=12)
    
    # Dividir el contenido en líneas manejables
    contenido = data.mensaje
    lineas = contenido.split('\n')
    
    for linea in lineas:
        if linea.strip():  # Si la línea tiene contenido
            # Si la línea es muy larga, dividirla
            if pdf.get_string_width(linea) > 180:
                palabras = linea.split(' ')
                linea_actual = ""
                for palabra in palabras:
                    if pdf.get_string_width(linea_actual + palabra + " ") <= 180:
                        linea_actual += palabra + " "
                    else:
                        if linea_actual:
                            pdf.multi_cell(0, 10, txt=linea_actual.strip())
                        linea_actual = palabra + " "
                if linea_actual:
                    pdf.multi_cell(0, 10, txt=linea_actual.strip())
            else:
                pdf.multi_cell(0, 10, txt=linea)
        pdf.ln(2)  # Espacio entre líneas
    
    filename = f"clase_ingles_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)
    
    return FileResponse(
        path=filename, 
        filename=filename, 
        media_type='application/pdf'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)