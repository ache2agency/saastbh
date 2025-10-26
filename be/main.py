import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI
from fpdf import FPDF
import uuid

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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    mensaje: str

@app.post("/generar-clase")
def generar_clase(data: Prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en enseñanza del inglés como T.B. Harden."},
                {"role": "user", "content": data.mensaje}
            ]
        )
        return {"clase_generada": response.choices[0].message.content}
    except Exception as e:
        return {"error": f"No se pudo generar la clase: {str(e)}"}

@app.post("/descargar-pdf")
def descargar_pdf(data: Prompt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    lineas = data.mensaje.replace('\r\n', '\n').split('\n')
    for linea in lineas:
        if linea.strip():
            pdf.multi_cell(w=190, h=10, txt=linea.strip(), border=0)
        else:
            pdf.ln(5)

    filename = f"clase_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)
    return FileResponse(path=filename, filename=filename, media_type='application/pdf')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)