import React from 'react';
import { Search, MapPin, Briefcase } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const BolsaEmpleoPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#F5F5F5] font-sans">
      {/* Navbar Minimalista */}
      <nav className="bg-white py-4 px-8 flex justify-between items-center shadow-sm">
        <Link to="/">
          <img 
            src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
            alt="PUCE Ibarra" 
            className="h-10 object-contain"
          />
        </Link>
        <div className="text-gray-500 font-bold uppercase tracking-wider text-sm">
          Bolsa de Empleo
        </div>
      </nav>

      {/* Hero Section */}
      <div 
        className="relative h-[400px] flex flex-col items-center justify-center bg-cover bg-center"
        style={{ 
          backgroundImage: "url('https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80')",
        }}
      >
        <div className="absolute inset-0 bg-black/40" />
        
        <div className="relative z-10 w-full max-w-4xl px-4 text-center">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl font-bold text-white mb-4 drop-shadow-lg"
          >
            Las mejores ofertas de empleos
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-white text-lg mb-8 drop-shadow-md"
          >
            Encuentra el tuyo ahora
          </motion.p>

          {/* Search Box */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col md:flex-row bg-white rounded-sm shadow-2xl overflow-hidden"
          >
            <div className="flex-1 flex items-center px-4 py-4 md:py-0 border-b md:border-b-0 md:border-r border-gray-200">
              <Search className="text-gray-400 mr-3" size={20} />
              <input 
                type="text" 
                placeholder="Puesto, descripción, requisitos o beneficios"
                className="w-full outline-none text-gray-700 bg-transparent placeholder-gray-400"
              />
            </div>
            <div className="flex-1 flex items-center px-4 py-4 md:py-0">
              <MapPin className="text-gray-400 mr-3" size={20} />
              <input 
                type="text" 
                placeholder="Provincia, ciudad o código postal"
                className="w-full outline-none text-gray-700 bg-transparent placeholder-gray-400"
              />
            </div>
            <button className="bg-[#007AC3] hover:bg-[#0056A8] text-white px-8 py-4 font-bold transition-colors">
              Buscar empleos
            </button>
          </motion.div>
          <div className="text-right mt-2 text-white text-sm font-bold drop-shadow-md cursor-pointer hover:underline">
            Búsqueda avanzada
          </div>
        </div>
      </div>

      {/* Empleos Recientes */}
      <div className="max-w-4xl mx-auto py-16 px-4">
        <div className="text-center mb-12">
          <p className="text-gray-400 text-xs tracking-widest uppercase mb-2">Últimos</p>
          <h2 className="text-3xl font-bold text-[#444444]">Empleos Recientes</h2>
          <div className="w-12 h-0.5 bg-[#007AC3] mx-auto mt-4" />
        </div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 }}
          className="bg-[#EBF5FB] border border-[#D6EAF8] p-8 text-center rounded-sm flex flex-col items-center justify-center text-[#007AC3]"
        >
          <Briefcase size={32} className="mb-4 opacity-50" />
          <p className="font-medium">No hay empleos disponibles por el momento.</p>
        </motion.div>
      </div>
    </div>
  );
};

export default BolsaEmpleoPage;
