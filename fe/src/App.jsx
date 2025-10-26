import { useState } from 'react'

// La URL de la API viene de la variable de entorno o usa localhost por defecto
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [prompt, setPrompt] = useState('')
  const [claseGenerada, setClaseGenerada] = useState(null)
  const [loading, setLoading] = useState(false)

  const generarClase = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/generar-clase`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: prompt }),
      })
      const data = await response.json()
      setClaseGenerada(data)
    } catch (error) {
      console.error('Error:', error)
      alert('Error al generar la clase. Verifica que el backend esté ejecutándose.')
    } finally {
      setLoading(false)
    }
  }

  const descargarPDF = async () => {
    if (!claseGenerada) return
    
    try {
      const response = await fetch(`${API_URL}/descargar-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: claseGenerada.clase_generada }),
      })
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = 'clase_ingles.pdf'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error descargando PDF:', error)
      alert('Error al descargar el PDF')
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Generador de Clases de Inglés TB Harden
        </h1>
        
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <textarea
            className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ejemplo: Clase A1 sobre vocabulario de la casa para 5 estudiantes"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          
          <button
            onClick={generarClase}
            disabled={loading || !prompt.trim()}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Generando Clase...' : 'Generar Clase'}
          </button>
        </div>

        {/* Result Section */}
        {claseGenerada && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Clase Generada</h2>
              <button
                onClick={descargarPDF}
                className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg"
              >
                Descargar PDF
              </button>
            </div>
            
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg font-mono text-sm">
                {claseGenerada.clase_generada}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App