import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Send, X } from 'lucide-react';
import api from '../services/api';
import { useAuthStore } from '../store/authStore';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWindowProps {
  initialMsg?: string;
  isPublic?: boolean;
  unreadNotifications?: any[];
}

/**
 * Componente ChatWindow
 * Widget interactivo (flotante) que gestiona la conversación con el Chatbot (IA).
 * Funciona tanto para usuarios públicos (visitantes) como autenticados.
 * Integra:
 * - Historial de mensajes.
 * - Grabación de voz (Audio a Texto).
 * - Indicadores de "escribiendo..." (loading).
 * - Envío de notificaciones pendientes si el usuario está autenticado.
 */
const ChatWindow: React.FC<ChatWindowProps> = ({ initialMsg, isPublic = false, unreadNotifications = [] }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const { isAuthenticated } = useAuthStore();
  const [sessionId] = useState(() => {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  });
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  // Handle external triggers (like clicking a career)
  useEffect(() => {
    if (initialMsg) {
      setIsOpen(true);
      if (!messages.some(m => m.content === initialMsg)) {
        sendMessage(undefined, initialMsg);
      }
    }
  }, [initialMsg]);

  // Handle proactive notifications
  useEffect(() => {
    if (!isPublic && unreadNotifications.length > 0 && messages.length === 0) {
      const count = unreadNotifications.length;
      const msg = `Hola, soy tu asistente digital. Tienes ${count} ${count === 1 ? 'notificación pendiente' : 'notificaciones pendientes'}. ¿Deseas que te las lea?`;
      
      // We don't want to add this to the "user" history, just make the assistant "say" it
      setMessages([{ role: 'assistant', content: msg }]);
      
      // Request audio for this message
      const getAudio = async () => {
        try {
          const res = await api.post('/chat/', { message: `ANUNCIO_NOTIFICACIONES: ${msg}`, session_id: sessionId });
          if (res.data.audio_base64) {
             const audio = new Audio(`data:audio/mp3;base64,${res.data.audio_base64}`);
             audio.play().catch(e => console.warn("Autoplay blocked:", e));
          }
        } catch (e) {
          console.error("Error announcing notifications:", e);
        }
      };
      getAudio();
    }
  }, [unreadNotifications]);

  const sendMessage = async (voiceBlob?: Blob, customMsg?: string) => {
    const textMsg = customMsg || input.trim();
    if (!voiceBlob && !textMsg) return;
    if (loading) return;

    setLoading(true);
    const newMessages = [...messages];
    if (textMsg) {
      newMessages.push({ role: 'user', content: textMsg });
      setMessages(newMessages);
      setInput('');
    }

    try {
      if (voiceBlob) {
        const formData = new FormData();
        formData.append('audio', voiceBlob, 'recording.webm');
        formData.append('session_id', sessionId);
        
        const res = await api.post('/voice/chat/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        const { transcript, response, audio_base64 } = res.data;
        newMessages.push({ role: 'user', content: transcript });
        newMessages.push({ role: 'assistant', content: response });
        
        // Robust Playback
        const audioUrl = `data:audio/mp3;base64,${audio_base64}`;
        const audio = new Audio(audioUrl);
        audio.play().catch(e => console.warn("Autoplay blocked:", e));
      } else {
        const res = await api.post('/chat/', { message: textMsg, session_id: sessionId });
        const { response, audio_base64 } = res.data;
        newMessages.push({ role: 'assistant', content: response });
        
        // Always play audio if available (even for text/career clicks)
        if (audio_base64) {
          const audioUrl = `data:audio/mp3;base64,${audio_base64}`;
          const audio = new Audio(audioUrl);
          audio.play().catch(e => console.warn("Autoplay blocked:", e));
        }
      }
      setMessages([...newMessages]);
    } catch (err) {
      console.error(err);
      setMessages([...newMessages, { role: 'assistant', content: 'Lo siento, ocurrió un error en la conexión.' }]);
    } finally {
      setLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks: Blob[] = [];
      recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        if (blob.size > 200) sendMessage(blob);
        stream.getTracks().forEach(track => track.stop());
      };
      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (err) {
      console.error('Mic access denied', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      {!isOpen && (
        <div className="fixed bottom-8 right-8 flex flex-col items-end gap-3 z-50">
          <motion.button 
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.1 }}
            onClick={() => setIsOpen(true)}
            className="w-16 h-16 bg-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 active:scale-95 transition-all group overflow-hidden border border-gray-100"
          >
            <img 
              src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
              alt="PUCE" 
              className="w-10 object-contain" 
            />
          </motion.button>
        </div>
      )}

      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, y: 100, scale: 0.9, x: 20 }}
            animate={{ opacity: 1, y: 0, scale: 1, x: 0 }}
            exit={{ opacity: 0, y: 100, scale: 0.9, x: 20 }}
            className="fixed bottom-8 right-8 w-96 max-w-[calc(100vw-48px)] h-[580px] bg-white rounded-3xl overflow-hidden flex flex-col z-[100] border border-gray-200 shadow-2xl"
          >
            {/* Header */}
            <div className="bg-[#0033A0] p-4 flex items-center justify-between shadow-md z-10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center overflow-hidden p-1">
                  <img 
                    src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
                    alt="PUCE" 
                    className="w-full object-contain" 
                  />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white tracking-wide">AcadBot PUCESI</h4>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                    <span className="text-[10px] text-gray-200 uppercase tracking-wider font-semibold">
                      {isPublic ? 'Atención Pública' : 'Portal Estudiantil'}
                    </span>
                  </div>
                </div>
              </div>
              <button 
                onClick={() => setIsOpen(false)}
                className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors"
                aria-label="Cerrar chat"
              >
                <X size={20} className="text-white" />
              </button>
            </div>

            {/* Messages Area */}
            <div 
              ref={scrollRef}
              className="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50/50"
            >
              {messages.length === 0 && (
                <div className="bg-white border border-gray-100 shadow-sm rounded-2xl p-5 text-sm text-gray-600 leading-relaxed text-center">
                  👋 ¡Hola! Soy el asistente inteligente de la PUCE Ibarra.
                  <br/><br/>
                  {isAuthenticated 
                    ? '¿En qué puedo ayudarte hoy con tu portal estudiantil?' 
                    : '¿Tienes alguna duda sobre admisiones, carreras o requisitos?'}
                </div>
              )}
              {messages.map((m, i) => (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  key={i} 
                  className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[85%] p-3.5 rounded-2xl text-sm leading-relaxed shadow-sm ${
                    m.role === 'user' 
                      ? 'bg-[#00AEEF] text-white rounded-tr-sm' 
                      : 'bg-white border border-gray-200 text-gray-800 rounded-tl-sm'
                  }`}>
                    {m.content}
                  </div>
                </motion.div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 p-3 rounded-2xl rounded-tl-sm flex gap-1.5 items-center shadow-sm">
                    <span className="w-1.5 h-1.5 bg-[#00AEEF] rounded-full animate-bounce [animation-delay:-0.3s]" />
                    <span className="w-1.5 h-1.5 bg-[#00AEEF] rounded-full animate-bounce [animation-delay:-0.15s]" />
                    <span className="w-1.5 h-1.5 bg-[#00AEEF] rounded-full animate-bounce" />
                  </div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-gray-100 bg-white">
              <div className="flex gap-2">
                <input 
                  type="text" 
                  value={input}
                  disabled={isRecording || loading}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder={isRecording ? 'Escuchando tu voz...' : 'Escribe tu consulta...'}
                  className="flex-1 bg-gray-50 border border-gray-200 rounded-full px-4 py-2.5 text-sm text-gray-800 focus:border-[#00AEEF] focus:ring-1 focus:ring-[#00AEEF] transition-all outline-none disabled:opacity-50"
                />
                
                <button 
                  onMouseDown={startRecording}
                  onMouseUp={stopRecording}
                  onTouchStart={startRecording}
                  onTouchEnd={stopRecording}
                  className={`w-11 h-11 rounded-full flex items-center justify-center transition-all shrink-0 ${
                    isRecording 
                    ? 'bg-red-500 text-white scale-110 shadow-lg animate-pulse' 
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                  }`}
                  title="Grabar Voz"
                >
                  <Mic size={18} />
                </button>

                <button 
                  onClick={() => sendMessage()}
                  disabled={loading || isRecording || !input.trim()}
                  className="w-11 h-11 bg-[#00AEEF] rounded-full flex items-center justify-center text-white shadow-md hover:bg-[#0096ce] active:scale-95 transition-all disabled:opacity-50 shrink-0"
                  title="Enviar Mensaje"
                >
                  <Send size={18} className="ml-1" />
                </button>
              </div>
              <p className="text-[10px] text-gray-400 text-center mt-3 tracking-wide">
                Desarrollado para PUCE Sede Ibarra
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default ChatWindow;
