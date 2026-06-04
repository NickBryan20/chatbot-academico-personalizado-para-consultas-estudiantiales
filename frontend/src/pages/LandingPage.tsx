import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Phone, Mail, ChevronRight, Globe, GraduationCap, FileBadge, BookOpen, Users, Key } from 'lucide-react';
import { Link } from 'react-router-dom';
import ChatWindow from '../components/ChatWindow';
import CampusMapSection from '../components/CampusMapSection';

const slides = [
  {
    id: 1,
    bg: 'bg-gradient-to-r from-[#00AEEF] to-[#007AC3]',
    content: (
      <div className="flex h-full items-center px-12 lg:px-24">
        <div className="w-1/2">
          {/* Placeholder for the woman image */}
          <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=600&q=80" alt="Estudiante" className="rounded-2xl shadow-2xl object-cover h-[400px]" />
        </div>
        <div className="w-1/2 text-white pl-12">
          <h2 className="text-3xl font-light mb-2">A PARTIR DEL <span className="text-accent font-bold text-4xl block">4 de mayo</span></h2>
          <p className="text-sm mb-8">para los estudiantes que hayan concluido su proceso de admisión</p>
          <h1 className="text-6xl font-black leading-none mb-8">Accesos a <br/>Ventanilla <br/>ZOOM</h1>
          <button className="bg-secondary text-white rounded-full p-4 hover:scale-105 transition-transform shadow-lg flex items-center gap-2">
            <span className="font-bold">Más Información</span>
            <ChevronRight />
          </button>
        </div>
      </div>
    )
  },
  {
    id: 2,
    bg: 'bg-[#00AEEF]',
    content: (
      <div className="flex h-full items-center px-12 lg:px-24">
        <div className="w-1/2 text-white pr-8">
          <h2 className="text-3xl font-bold uppercase mb-2">Admisiones</h2>
          <h1 className="text-5xl font-black leading-tight mb-2 text-[#0033A0]">CURSO DE ADMISIÓN</h1>
          <div className="bg-white text-secondary inline-block px-4 py-1 rounded-full text-3xl font-black mb-2">PRESENCIAL</div>
          <h1 className="text-6xl font-outline-2 text-transparent mb-6" style={{ WebkitTextStroke: '2px white' }}>2026</h1>
          
          <div className="bg-white text-secondary font-bold px-4 py-1 inline-block mb-2 text-sm">DIRIGIDO A:</div>
          <p className="text-sm mb-4 leading-relaxed font-medium shadow-sm">• Bachilleres y estudiantes de tercer año de bachillerato que aspiran ingresar a nuestra universidad.</p>
          
          <div className="bg-white text-accent font-bold px-4 py-1 inline-block mb-2 text-sm">INSCRIPCIONES ABIERTAS HASTA:</div>
          <p className="text-lg font-bold shadow-sm text-[#0033A0]">• Martes, 26 de mayo de 2026</p>
        </div>
        <div className="w-1/2 flex justify-center">
          <img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80" alt="Estudiantes" className="rounded-2xl shadow-2xl object-cover h-[400px]" />
        </div>
      </div>
    )
  },
  {
    id: 3,
    bg: 'bg-white',
    content: (
      <div className="flex h-full items-center">
        <div className="w-1/2 p-12 lg:p-24 text-secondary">
          <h2 className="text-2xl font-bold mb-2">ADMISIONES</h2>
          <h1 className="text-6xl font-black leading-tight mb-4 text-[#0056A8]">EXAMEN DE <br/>ADMISIÓN</h1>
          <h2 className="text-5xl font-bold text-accent mb-8">PUCE-I 2026</h2>
          
          <div className="bg-[#0056A8] text-white p-6 rounded-tr-3xl rounded-br-3xl -ml-24 pl-24">
            <h3 className="text-2xl font-bold text-accent mb-1">Inscripciones Abiertas</h3>
            <p className="text-lg">• Del 14 de mayo al 15 de junio de 2026</p>
          </div>
        </div>
        <div className="w-1/2 h-full">
          <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80" alt="Estudiantes en el campus" className="w-full h-full object-cover" />
        </div>
      </div>
    )
  }
];

const LandingPage: React.FC = () => {
  const [chatInitialMsg, setChatInitialMsg] = useState<string | undefined>(undefined);
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const handleServiceClick = (serviceName: string) => {
    setChatInitialMsg(`Información sobre ${serviceName}`);
    setTimeout(() => setChatInitialMsg(undefined), 500);
  };

  return (
    <div className="bg-bg-light text-text-dark min-h-screen font-sans">
      {/* Top Bar Celeste */}
      <div className="bg-primary text-white text-xs py-2 px-8 flex justify-between items-center">
        <div className="flex gap-6">
          <span className="flex items-center gap-2"><Phone size={14}/> (+593) 06 2994700</span>
          <span className="flex items-center gap-2"><Mail size={14}/> uci@pucesi.edu.ec</span>
        </div>
        <div className="flex gap-4">
          <Globe size={14} className="cursor-pointer" />
        </div>
      </div>

      {/* Main Navbar Blanco */}
      <nav className="bg-white w-full z-50 py-4 px-8 flex justify-between items-center border-b border-gray-100 shadow-sm sticky top-0">
        <a href="#inicio" className="flex items-center">
          <img 
            src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
            alt="PUCE Ibarra" 
            className="h-10 object-contain hover:scale-105 transition-transform"
          />
        </a>
        
        <div className="hidden lg:flex gap-6 items-center font-semibold text-xs text-gray-600 uppercase tracking-wide">
          <a href="https://www.pucesi.edu.ec/webs2/index.php/blog-historia-50-anos-puce-ibarra/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors">50 años PUCE I</a>
          
          <div className="relative group">
            <a href="https://www.pucesi.edu.ec/webs2/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors flex items-center gap-1 py-4">OFERTA ACADÉMICA <span>▾</span></a>
            <div className="absolute top-full left-0 bg-white border-t-2 border-[#00AEEF] shadow-lg hidden group-hover:flex flex-col min-w-[220px] z-50">
               <a href="https://www.pucesi.edu.ec/webs2/index.php/grados/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">GRADO</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/posgrados/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">POSGRADO</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/carreras-tecnicas-y-tecnologicas/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">CARRERAS TÉCNICAS</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/formacion-permanente-menu/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">EDUCACIÓN CONTINUA</a>
            </div>
          </div>

          <div className="relative group">
            <a href="https://www.pucesi.edu.ec/webs2/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors flex items-center gap-1 py-4">ADMISIONES <span>▾</span></a>
            <div className="absolute top-full left-0 bg-white border-t-2 border-[#00AEEF] shadow-lg hidden group-hover:flex flex-col min-w-[220px] z-50">
               <a href="https://www.pucesi.edu.ec/webs2/index.php/admisiones-grado-menu/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">ADMISIONES DE GRADO</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/admisiones-tecnologias/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">ADMISIONES TECNOLOGÍAS</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/admisiones-posgrado-2/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">ADMISIONES POSGRADO</a>
            </div>
          </div>

          <a href="https://www.pucesi.edu.ec/webs2/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors">INVESTIGACIÓN</a>
          
          <div className="relative group">
            <a href="https://www.pucesi.edu.ec/webs2/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors flex items-center gap-1 py-4">NOSOTROS <span>▾</span></a>
            <div className="absolute top-full left-0 bg-white border-t-2 border-[#00AEEF] shadow-lg hidden group-hover:flex flex-col min-w-[340px] z-50">
               <a href="https://www.pucesi.edu.ec/webs2/index.php/convenios-presupuestos-y-plan-estrategico/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">CONVENIOS, PRESUPUESTOS Y PLAN ESTRATÉGICO</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/menu-normativa-puce-ibarra-2/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">GACETA OFICIAL</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/informe-de-actividades-y-rendicion-de-cuentas/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">RENDICIÓN DE CUENTAS</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/comite-de-etica/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">COMITÉ DE ÉTICA</a>
               <a href="https://www.pucesi.edu.ec/webs2/index.php/nosotros-organigrama-institucional/" target="_blank" rel="noreferrer" className="px-6 py-4 hover:bg-gray-50 text-gray-700 font-bold text-sm">ESTRUCTURA ORGANIZACIONAL</a>
            </div>
          </div>

          <a href="https://www.pucesi.edu.ec/webs2/index.php/blog-noticias-pucei/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors">BLOG</a>
          <a href="#mapa-campus" className="hover:text-primary transition-colors">MAPA CAMPUS</a>
          <a href="https://www.puce.edu.ec/sitios/formularios/sugerencias/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors">BUZÓN DE SUGERENCIAS</a>
          <a href="mailto:uci@pucesi.edu.ec"><Mail size={18} className="text-secondary hover:text-primary cursor-pointer" /></a>
        </div>
      </nav>

      {/* Hero Section with Slider and Right Menu */}
      <div id="inicio" className="flex h-[70vh] relative overflow-hidden">
        
        {/* Slider Area (Left 75%) */}
        <div className="w-[75%] h-full relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.5 }}
              className={`w-full h-full ${slides[currentSlide].bg}`}
            >
              {slides[currentSlide].content}
            </motion.div>
          </AnimatePresence>

          {/* Slider Indicators */}
          <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2">
            {slides.map((_, idx) => (
              <button 
                key={idx}
                onClick={() => setCurrentSlide(idx)}
                className={`w-3 h-3 rounded-full transition-colors ${currentSlide === idx ? 'bg-secondary' : 'bg-black/20'}`}
              />
            ))}
          </div>
        </div>

        {/* Right Menu (Right 25%) */}
        <div className="w-[25%] h-full bg-[#0033A0] flex flex-col justify-center py-8">
          <ul className="text-white space-y-2">
            {[
              { text: 'GRADO', icon: <GraduationCap size={32} /> },
              { text: 'POSGRADO', icon: <FileBadge size={32} /> },
              { text: 'TECNOLOGÍAS\nPUCE TEC', icon: <BookOpen size={32} /> },
              { text: 'FORMACIÓN\nPERMANENTE', icon: <Users size={32} /> },
              { text: 'ADMISIONES', icon: <Key size={32} /> },
            ].map((item, idx) => (
              <li key={idx}>
                <a href={`#${item.text.toLowerCase().replace(/\n/g, '')}`} className="flex items-center gap-4 px-12 py-4 hover:bg-[#0056A8] transition-colors group">
                  <div className="text-white/80 group-hover:text-white group-hover:scale-110 transition-all">
                    {item.icon}
                  </div>
                  <span className="font-bold tracking-wide whitespace-pre-line text-sm">{item.text}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* Grid de Accesos Directos (Iconos Azules) */}
      <section className="py-20 px-8 bg-white">
        <div className="container mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            
            {/* Campus Virtual - Enlace a Login */}
            <Link to="/login" className="group">
              <div className="bg-secondary p-8 flex flex-col items-center justify-center min-h-[160px] relative overflow-hidden transition-transform hover:-translate-y-2">
                 <div className="text-white mb-2">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/><path d="M8 11h8"/></svg>
                 </div>
                 <div className="absolute bottom-0 left-0 w-full bg-primary py-3 text-center text-white text-xs font-bold uppercase">
                   Campus Virtual
                 </div>
              </div>
            </Link>

            {[
              { id: 'app', name: 'Aplicaciones Internas', to: null, icon: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg> },
              { id: 'grad', name: 'Seguimiento a graduados', to: null, icon: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg> },
              { id: 'banner', name: 'AutoServicio Banner', to: '/banner', icon: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> },
              { id: 'empleo', name: 'Bolsa de Empleo', to: '/empleo', icon: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg> },
              { id: 'biblio', name: 'Biblioteca PUCE Ibarra', to: null, icon: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg> },
            ].map((item) => {
              const content = (
                <div className="bg-secondary p-8 flex flex-col items-center justify-center min-h-[160px] relative overflow-hidden transition-transform hover:-translate-y-2">
                   <div className="text-white mb-2">{item.icon}</div>
                   <div className="absolute bottom-0 left-0 w-full bg-primary py-3 text-center text-white text-xs font-bold uppercase leading-tight px-2">
                     {item.name}
                   </div>
                </div>
              );

              return item.to ? (
                <Link key={item.id} to={item.to} className="group text-left block">
                  {content}
                </Link>
              ) : (
                <button key={item.id} onClick={() => handleServiceClick(item.name)} className="group text-left block w-full">
                  {content}
                </button>
              );
            })}
          </div>
        </div>
      </section>

      <CampusMapSection />

      {/* Sección Oferta Académica */}
      <section className="py-16 bg-[#444444] relative overflow-hidden">
        {/* Decorative background pattern */}
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 10px, #000 10px, #000 20px)' }}></div>
        
        <div className="container mx-auto px-8 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              {
                title: "Educación\nContinua Cursos y\ndiplomados",
                image: "https://images.unsplash.com/photo-1577563908411-5077b6dc7624?auto=format&fit=crop&w=400&q=80",
                link: "https://www.pucesi.edu.ec/webs2/index.php/formacion-permanente-menu/"
              },
              {
                title: "Carreras técnicas\ny tecnológicas",
                image: "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=400&q=80",
                link: "https://www.pucesi.edu.ec/webs2/index.php/carreras-tecnicas-y-tecnologicas/"
              },
              {
                title: "Carreras de\ngrado",
                image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80",
                link: "https://www.pucesi.edu.ec/webs2/index.php/grados/"
              },
              {
                title: "Posgrados\nmodalidad\npresencial e híbrida",
                image: "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=400&q=80",
                link: "https://www.pucesi.edu.ec/webs2/index.php/posgrados/"
              },
              {
                title: "Posgrados\nmodalidad virtual",
                image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=400&q=80",
                link: "https://www.pucesi.edu.ec/webs2/index.php/posgrados/"
              }
            ].map((item, idx) => (
              <a key={idx} href={item.link} target="_blank" rel="noreferrer" className="group block relative h-[380px] rounded-sm overflow-hidden shadow-lg transition-transform hover:-translate-y-2">
                <div className="absolute inset-0">
                  <img src={item.image} alt="Oferta" className="w-full h-full object-cover" />
                </div>
                <div className="absolute bottom-0 left-0 w-full bg-[#007AC3] p-4 group-hover:bg-[#0056A8] transition-colors border-t border-blue-400">
                  <h4 className="text-white text-center font-bold text-sm leading-tight whitespace-pre-line">
                    {item.title}
                  </h4>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Sección Noticias */}
      <section className="py-12 bg-white">
        <div className="container mx-auto px-8">
          <div className="bg-[#0056a8] text-center py-4 mb-12">
            <h3 className="text-3xl font-bold text-white uppercase tracking-wider">Noticias PUCE Ibarra</h3>
            <div className="w-16 h-1 bg-accent mx-auto mt-4"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Card 1 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow flex flex-col">
              <div className="h-56 bg-gray-200">
                  <img src="https://images.unsplash.com/photo-1616469829581-73993eb86b02?auto=format&fit=crop&w=500&q=80" alt="Inmersión Dual" className="w-full h-full object-cover" />
              </div>
              <div className="p-6 flex-1 flex flex-col text-center">
                <h4 className="text-lg font-normal text-[#333333] mb-4 leading-tight">PUCE Ibarra fortalece la internacionalización con 26 sesiones de Inmersión Dual Virtual junto a universidades de AJCU</h4>
                <p className="text-sm text-gray-500 line-clamp-4 flex-1">La PUCE Ibarra continúa consolidando los procesos de internacionalización mediante el desarrollo de sesiones de Inmersión Dual Virtual (IDV), una metodología activa que promueve el intercambio cultural y la práctica auténtica del inglés en escenarios internacionales...</p>
              </div>
            </div>

            {/* Card 2 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow flex flex-col">
              <div className="h-56 bg-gray-200">
                  <img src="https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=500&q=80" alt="Creatibot" className="w-full h-full object-cover" />
              </div>
              <div className="p-6 flex-1 flex flex-col text-center">
                <h4 className="text-lg font-normal text-[#333333] mb-4 leading-tight">CREATIBOT IV Edición culminó con éxito impulsando la innovación y el talento tecnológico estudiantil</h4>
                <p className="text-sm text-gray-500 line-clamp-4 flex-1">La creatividad, la innovación y el talento estudiantil marcaron el cierre exitoso del CREATIBOT IV Edición, un encuentro de robótica educativa organizado por la Carrera de Software de la Escuela de Hábitat, Infraestructura y Creatividad de...</p>
              </div>
            </div>

            {/* Card 3 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow flex flex-col">
              <div className="h-56 bg-gray-200">
                  <img src="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=500&q=80" alt="Día del Maestro" className="w-full h-full object-cover" />
              </div>
              <div className="p-6 flex-1 flex flex-col text-center">
                <h4 className="text-lg font-normal text-[#333333] mb-4 leading-tight">Docentes PUCE Ibarra fueron homenajeados en la Segunda Jornada Humanística 2026</h4>
                <p className="text-sm text-gray-500 line-clamp-4 flex-1">En el marco de la conmemoración del Día del Maestro, la Pontificia Universidad Católica del Ecuador Sede Ibarra, a través de la Dirección de Docencia y Estudiantes y la Dirección de Identidad y Misión, desarrolló la...</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-12 flex flex-col lg:flex-row">
        {/* Lado Izquierdo Blanco */}
        <div className="w-full lg:w-2/3 bg-white p-12 lg:p-16 grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h4 className="text-xl font-bold text-primary mb-6">Sedes</h4>
            <ul className="space-y-3 text-sm text-gray-600">
              <li>Sede Quito</li>
              <li>Sede Ambato</li>
              <li>Sede Esmeraldas</li>
              <li>Sede Santo Domingo</li>
              <li>Sede Manabí</li>
              <li>Sede Amazonas</li>
            </ul>
          </div>
          <div>
            <h4 className="text-xl font-bold text-primary mb-6">Servicios</h4>
            <ul className="space-y-3 text-sm text-gray-600">
              <li>Agenda Telefónica</li>
              <li>Biblioteca</li>
              <li>Tour Virtual</li>
              <li>Campus Virtual</li>
              <li>Eventos Académicos</li>
            </ul>
          </div>
          <div>
            <h4 className="text-xl font-bold text-primary mb-6">Enlaces Frecuentes</h4>
            <ul className="space-y-3 text-sm text-gray-600">
              <li>Correo electrónico</li>
              <li>Aplicaciones Internas</li>
              <li>Hall de pagos</li>
              <li>Autoservicio Banner</li>
            </ul>
          </div>
          <div>
            <h4 className="text-xl font-bold text-primary mb-6">Gestión</h4>
            <ul className="space-y-3 text-sm text-gray-600">
              <li>Convenios</li>
              <li>Gaceta Oficial</li>
              <li>Plan Estratégico</li>
              <li>Presupuestos</li>
            </ul>
          </div>
        </div>

        {/* Lado Derecho Azul */}
        <div className="w-full lg:w-1/3 bg-secondary p-12 lg:p-16 text-white flex flex-col justify-center">
          <img src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" alt="PUCE Ibarra" className="h-16 object-contain mb-8 filter brightness-0 invert" />
          
          <div className="space-y-6">
            <div>
              <h5 className="font-bold mb-2 flex items-center gap-2">Dirección</h5>
              <p className="text-sm opacity-90 leading-relaxed">Av. Jorge Guzmán Rueda y Av. Aurelio Espinosa Pólit. ciudadela «La Victoria», Ecuador</p>
            </div>
            <div>
              <h5 className="font-bold mb-2 flex items-center gap-2">Teléfono</h5>
              <p className="text-sm opacity-90">Telf: (593-06) 2994-700, 2615-631</p>
              <p className="text-sm opacity-90">Fax: (593-06) 2615-446</p>
            </div>
            <div>
              <h5 className="font-bold mb-2 flex items-center gap-2">Web y correo</h5>
              <p className="text-sm opacity-90">web: https://www.pucesi.edu.ec</p>
              <p className="text-sm opacity-90">mail: uci@pucesi.edu.ec</p>
            </div>
          </div>
        </div>
      </footer>

      <div className="bg-slate-900 text-white text-xs p-3 text-center">
         https://www.pucesi.edu.ec/webs2/
      </div>

      <ChatWindow initialMsg={chatInitialMsg} isPublic={true} />
    </div>
  );
};

export default LandingPage;
