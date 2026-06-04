import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mail, Lock, Globe, ShieldCheck, CheckCircle2, ArrowLeft } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuthStore } from '../store/authStore';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  // States
  const [step, setStep] = useState(1); // 1: Login, 2: 2FA OTP
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Form State
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  
  // 2FA State
  const [tempToken, setTempToken] = useState('');
  const [otpCode, setOtpCode] = useState('');
  
  // Language State
  const [language, setLanguage] = useState('ES');

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/login/', {
        username: formData.username.trim(),
        password: formData.password.trim()
      });

      if (response.data.requires_2fa) {
        setTempToken(response.data.temp_token);
        setStep(2);
      } else if (response.data.access && response.data.refresh) {
        // Direct Login Success
        const { user, access, refresh } = response.data;
        setAuth(user, access, refresh);
        navigate(user.role === 'teacher' ? '/teacher' : '/dashboard');
      }
    } catch (err: any) {
      const errorData = err.response?.data?.error;
      let message = 'Datos erróneos. Por favor, inténtelo otra vez.';
      
      if (typeof errorData === 'string') {
        message = errorData;
      } else if (errorData && typeof errorData === 'object') {
        const firstKey = Object.keys(errorData)[0];
        const errorVal = errorData[firstKey];
        message = Array.isArray(errorVal) ? errorVal[0] : String(errorVal);
      }
      
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleOtpSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/verify-otp/', {
        temp_token: tempToken,
        otp_code: otpCode.trim(),
      });

      const { user, access, refresh } = response.data;
      setAuth(user, access, refresh);
      navigate(user.role === 'teacher' ? '/teacher' : '/dashboard');
    } catch (err: any) {
      const errorData = err.response?.data?.error;
      let message = 'Código incorrecto o expirado.';
      
      if (typeof errorData === 'string') {
        message = errorData;
      } else if (errorData && typeof errorData === 'object') {
        const firstKey = Object.keys(errorData)[0];
        const errorVal = errorData[firstKey];
        message = Array.isArray(errorVal) ? errorVal[0] : String(errorVal);
      }
      
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans bg-[#F5F5F5]">
      {/* Header */}
      <header className="bg-white py-4 px-8 flex justify-between items-center shadow-sm z-10">
        <Link to="/">
          <img 
            src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
            alt="PUCE Ibarra" 
            className="h-10 object-contain"
          />
        </Link>
        {/* Language Selector */}
        <div className="relative group">
          <div className="text-[#0056A8] hover:text-[#003A70] cursor-pointer p-2 flex items-center gap-1">
            <Globe size={20} />
            <span className="text-sm font-bold uppercase">{language}</span>
          </div>
          
          <div className="absolute top-full right-0 bg-white shadow-xl border border-gray-100 rounded-md py-2 hidden group-hover:block min-w-[120px]">
            <button onClick={() => setLanguage('ES')} className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-[#0056A8] font-medium">Español</button>
            <button onClick={() => setLanguage('EN')} className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-[#0056A8] font-medium">English</button>
            <button onClick={() => setLanguage('FR')} className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-[#0056A8] font-medium">Français</button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow relative flex items-center justify-center lg:justify-end">
        {/* Background Image */}
        <div 
          className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
          style={{ 
            backgroundImage: "url('https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=2069&auto=format&fit=crop')",
            filter: "brightness(0.8)"
          }}
        />

        {/* Text overlay for left side */}
        <div className="hidden lg:block absolute left-16 top-1/3 z-10 max-w-xl">
          <h1 className="text-4xl font-normal text-white uppercase leading-relaxed drop-shadow-md">
            CAMPUS VIRTUAL PRIMER PERIODO 2026 - 01
          </h1>
          <h2 className="text-3xl font-normal text-white uppercase mt-8 drop-shadow-md">
            CAMPUS VIRTUAL PRIMER PERIODO 2026 - 01
          </h2>
        </div>

        {/* Login Box */}
        <div className="relative z-10 w-full max-w-[480px] bg-white p-8 lg:mr-24 shadow-2xl">
          <AnimatePresence mode="wait">
            {step === 1 ? (
              <motion.div
                key="login"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <h3 className="text-[#0056A8] text-2xl mb-6">Accede a la plataforma</h3>
                
                <form onSubmit={handleLoginSubmit} className="space-y-4">
                  <div>
                    <label className="block text-gray-700 text-sm mb-1">Nombre de usuario</label>
                    <div className="flex border border-gray-300 bg-gray-50 focus-within:border-gray-400">
                      <div className="p-3 bg-gray-100 border-r border-gray-300 text-gray-500">
                        <Mail size={18} />
                      </div>
                      <input 
                        type="text" 
                        placeholder="Nombre de usuario"
                        className="w-full p-2 outline-none bg-transparent"
                        required
                        value={formData.username}
                        onChange={(e) => setFormData({...formData, username: e.target.value})}
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm mb-1">Contraseña</label>
                    <div className="flex border border-gray-300 bg-gray-50 focus-within:border-gray-400">
                      <div className="p-3 bg-gray-100 border-r border-gray-300 text-gray-500">
                        <Lock size={18} />
                      </div>
                      <input 
                        type="password" 
                        placeholder="Contraseña"
                        className="w-full p-2 outline-none bg-transparent"
                        required
                        value={formData.password}
                        onChange={(e) => setFormData({...formData, password: e.target.value})}
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="text-red-500 bg-red-50 p-3 text-sm border border-red-200">
                      {error}
                    </div>
                  )}

                  <button 
                    type="submit" 
                    disabled={loading}
                    className="bg-[#4299B5] hover:bg-[#34829A] text-white px-6 py-2 transition-colors disabled:opacity-70 mt-2"
                  >
                    {loading ? 'Accediendo...' : 'Acceder'}
                  </button>

                  <div className="mt-6">
                    <a href="#" className="text-[#4299B5] hover:underline text-sm">
                      ¿Olvidó su nombre de usuario o contraseña?
                    </a>
                  </div>
                </form>
              </motion.div>
            ) : (
              <motion.div
                key="2fa"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <h3 className="text-[#0056A8] text-2xl mb-6">Verificación 2FA</h3>
                
                <div className="bg-blue-50 p-4 border border-blue-100 mb-6 flex gap-3">
                  <ShieldCheck className="text-blue-500 shrink-0 mt-1" size={20} />
                  <p className="text-sm text-gray-700">
                    Se ha enviado un código a su correo institucional. Revise la consola del servidor para el código simulado.
                  </p>
                </div>

                <form onSubmit={handleOtpSubmit} className="space-y-4">
                  <div>
                    <label className="block text-gray-700 text-sm mb-1">Código de 6 dígitos</label>
                    <input 
                      type="text" 
                      placeholder="000000"
                      maxLength={6}
                      className="w-full p-3 border border-gray-300 outline-none text-center text-xl tracking-widest bg-gray-50 focus:border-gray-400"
                      required
                      autoFocus
                      value={otpCode}
                      onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                    />
                  </div>

                  {error && (
                    <div className="text-red-500 bg-red-50 p-3 text-sm border border-red-200">
                      {error}
                    </div>
                  )}

                  <div className="flex flex-col gap-3 pt-2">
                    <button 
                      type="submit" 
                      disabled={loading || otpCode.length !== 6}
                      className="bg-[#4299B5] hover:bg-[#34829A] text-white px-6 py-2 transition-colors disabled:opacity-70 flex justify-center items-center gap-2"
                    >
                      {loading ? 'Verificando...' : 'Confirmar Acceso'}
                      {!loading && <CheckCircle2 size={18} />}
                    </button>
                    
                    <button 
                      type="button"
                      onClick={() => setStep(1)}
                      className="text-[#4299B5] hover:underline text-sm flex justify-center items-center gap-1 mt-2"
                    >
                      <ArrowLeft size={14} /> Regresar al login
                    </button>
                  </div>
                </form>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white py-6 px-12 border-t border-gray-200 z-10 flex items-center gap-12">
        <div className="text-gray-500 font-bold uppercase tracking-widest text-sm">
          PUCE IBARRA
        </div>
        <div className="flex items-center gap-2 text-[#0056A8] text-sm">
          <Globe size={16} />
          <a href="http://www.pucesi.edu.ec" target="_blank" rel="noreferrer" className="hover:underline">
            http://www.pucesi.edu.ec
          </a>
        </div>
      </footer>
    </div>
  );
};

export default LoginPage;
