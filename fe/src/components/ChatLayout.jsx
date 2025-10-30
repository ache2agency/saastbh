// fe/src/components/ChatLayout.jsx
import React, { useState, useRef, useEffect } from 'react';

// La URL de la API viene de la variable de entorno o usa localhost por defecto
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const ChatLayout = () => {
  const [conversation, setConversation] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  const generarClase = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toLocaleTimeString()
    };

    setConversation(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/generar-clase`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: inputMessage }),
      });
      
      const data = await response.json();
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.clase_generada || 'Clase generada exitosamente',
        activity: data,
        timestamp: new Date().toLocaleTimeString()
      };

      setConversation(prev => [...prev, assistantMessage]);
      
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: 'Error al generar la clase. Verifica que el backend esté ejecutándose.',
        timestamp: new Date().toLocaleTimeString()
      };
      setConversation(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const descargarPDF = async (activity) => {
    if (!activity) return;
    
    try {
      const response = await fetch(`${API_URL}/descargar-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: activity.clase_generada || activity.content }),
      });
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'clase_ingles.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error descargando PDF:', error);
      alert('Error al descargar el PDF');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      generarClase();
    }
  };

  // Extraer actividades del historial para el sidebar
  const conversationHistory = conversation.filter(msg => 
    msg.type === 'assistant' && msg.activity
  );

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar - Historial */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          <h3 className="font-semibold text-gray-800">Clases Generadas</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          {conversationHistory.map((item) => (
            <div 
              key={item.id}
              className="p-3 mb-2 bg-white border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
            >
              <div className="font-medium text-gray-800">
                {item.activity.topic || 'Clase de Inglés'}
              </div>
              <div className="text-xs text-gray-500 mt-1">{item.timestamp}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">Generador de Clases de Inglés TB Harden</h2>
          <p className="text-gray-600">Crea actividades para tus clases de inglés</p>
        </div>

        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          {conversation.map((message) => (
            <div key={message.id} className={`flex mb-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex max-w-2xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                  message.type === 'user' ? 'bg-blue-500 ml-3' : 
                  message.type === 'error' ? 'bg-red-500 mr-3' : 'bg-green-500 mr-3'
                }`}>
                  <span className="text-white">
                    {message.type === 'user' ? '👤' : 
                     message.type === 'error' ? '⚠️' : '🤖'}
                  </span>
                </div>
                <div className={`px-4 py-3 rounded-lg ${
                  message.type === 'user' ? 'bg-blue-500 text-white' : 
                  message.type === 'error' ? 'bg-red-100 border border-red-200 text-red-800' : 
                  'bg-white border border-gray-200'
                }`}>
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  {message.activity && (
                    <div className="mt-3 p-3 bg-gray-50 rounded border-l-4 border-blue-500">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-gray-800">
                          {message.activity.topic || 'Clase Generada'}
                        </h4>
                        <button
                          onClick={() => descargarPDF(message.activity)}
                          className="bg-green-600 hover:bg-green-700 text-white text-sm font-medium py-1 px-3 rounded-lg"
                        >
                          Descargar PDF
                        </button>
                      </div>
                      {message.activity.level && (
                        <p className="text-sm text-gray-600">
                          <strong>Nivel:</strong> {message.activity.level}
                        </p>
                      )}
                      {message.activity.duration && (
                        <p className="text-sm text-gray-600">
                          <strong>Duración:</strong> {message.activity.duration}
                        </p>
                      )}
                    </div>
                  )}
                  <div className={`text-xs mt-2 ${
                    message.type === 'user' ? 'text-blue-100' : 
                    message.type === 'error' ? 'text-red-600' : 'text-gray-500'
                  }`}>
                    {message.timestamp}
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="flex max-w-2xl">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 mr-3 flex items-center justify-center">
                  <span className="text-white">🤖</span>
                </div>
                <div className="px-4 py-3 bg-white border border-gray-200 rounded-lg">
                  <div className="flex items-center gap-2">
                    <span>Generando clase...</span>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-gray-200 bg-white">
          <div className="flex gap-2 mb-3">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ejemplo: Clase A1 sobre vocabulario de la casa para 5 estudiantes"
              rows="2"
              disabled={loading}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
            <button 
              onClick={generarClase}
              disabled={loading || !inputMessage.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm text-gray-600">Sugerencias rápidas:</span>
            {[
              'Clase A1 sobre vocabulario de la casa',
              'Actividad B1 para practicar presente simple', 
              'Juego A2 con vocabulario de comida'
            ].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => setInputMessage(suggestion)}
                disabled={loading}
                className="px-3 py-1 text-sm bg-gray-100 border border-gray-300 rounded-full hover:bg-gray-200 disabled:opacity-50"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatLayout;