import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const AutoServicioBannerPage: React.FC = () => {
  const cards = [
    {
      title: "BANNER DOCENTES",
      image: "https://images.unsplash.com/photo-1577563908411-5077b6dc7624?auto=format&fit=crop&w=500&q=80",
    },
    {
      title: "BANNER ESTUDIANTES",
      image: "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=500&q=80",
    },
    {
      title: "BANNER ADMINISTRATIVOS",
      image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=500&q=80",
    }
  ];

  return (
    <div className="min-h-screen bg-[#F8F9FA] font-sans flex flex-col">
      {/* Navbar Minimalista */}
      <nav className="bg-white py-4 px-8 flex justify-between items-center shadow-sm border-b border-[#00AEEF]">
        <Link to="/">
          <img 
            src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
            alt="PUCE Ibarra" 
            className="h-10 object-contain"
          />
        </Link>
        <div className="text-[#0033A0] font-bold uppercase tracking-wider text-lg">
          Autoservicio Banner
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl w-full">
          {cards.map((card, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.2 }}
              className="group cursor-pointer flex flex-col h-[400px] rounded-t-3xl rounded-b-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all"
            >
              {/* Image Section */}
              <div className="flex-1 relative overflow-hidden">
                <img 
                  src={card.image} 
                  alt={card.title} 
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
                />
                <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors duration-500" />
              </div>
              
              {/* Title Section */}
              <div className="bg-[#666666] group-hover:bg-[#0033A0] transition-colors duration-300 py-6 text-center">
                <h3 className="text-white text-xl font-bold tracking-wide uppercase">
                  {card.title}
                </h3>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AutoServicioBannerPage;
