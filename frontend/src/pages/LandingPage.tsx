import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Phone, Mail, ChevronRight, Globe, GraduationCap, FileBadge, BookOpen, Users, Key } from 'lucide-react';
import { Link } from 'react-router-dom';
import ChatWindow from '../components/ChatWindow';

const slides = [
  {
    id: 1,
    bg: 'bg-gradient-to-r from-[#00AEEF] to-[#007AC3]',
    content: (
      <div className="grid h-full grid-cols-1 items-center gap-8 px-8 py-10 lg:grid-cols-2 lg:px-16 xl:px-20">
        <div className="flex justify-center lg:justify-start">
          {/* Placeholder for the woman image */}
          <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=600&q=80" alt="Estudiante" className="h-[300px] w-full max-w-[420px] rounded-2xl object-cover shadow-2xl xl:h-[360px]" />
        </div>
        <div className="min-w-0 text-white">
          <h2 className="text-2xl font-light xl:text-3xl">A PARTIR DEL <span className="block text-3xl font-bold text-accent xl:text-4xl">4 de mayo</span></h2>
          <p className="mb-6 mt-2 text-sm">para los estudiantes que hayan concluido su proceso de admisión</p>
          <h1 className="mb-6 text-4xl font-black leading-tight xl:text-5xl">Accesos a <br/>Ventanilla <br/>ZOOM</h1>
          <button className="flex items-center gap-2 rounded-full bg-secondary p-4 text-white shadow-lg transition-transform hover:scale-105">
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
      <div className="grid h-full grid-cols-1 items-center gap-8 px-8 py-10 lg:grid-cols-[minmax(0,0.95fr)_minmax(280px,0.9fr)] lg:px-16 xl:px-20">
        <div className="min-w-0 text-white">
          <h2 className="mb-2 text-2xl font-bold uppercase xl:text-3xl">Admisiones</h2>
          <h1 className="mb-2 text-4xl font-black leading-tight text-[#0033A0] xl:text-5xl">CURSO DE ADMISIÓN</h1>
          <div className="mb-2 inline-block rounded-full bg-white px-4 py-1 text-2xl font-black text-secondary xl:text-3xl">PRESENCIAL</div>
          <h1 className="mb-5 text-5xl text-transparent xl:text-6xl" style={{ WebkitTextStroke: '2px white' }}>2026</h1>
          
          <div className="mb-2 inline-block bg-white px-4 py-1 text-sm font-bold text-secondary">DIRIGIDO A:</div>
          <p className="mb-4 max-w-[440px] text-sm font-medium leading-relaxed shadow-sm">• Bachilleres y estudiantes de tercer año de bachillerato que aspiran ingresar a nuestra universidad.</p>
          
          <div className="mb-2 inline-block bg-white px-4 py-1 text-sm font-bold text-accent">INSCRIPCIONES ABIERTAS HASTA:</div>
          <p className="text-base font-bold text-[#0033A0] shadow-sm xl:text-lg">• Martes, 26 de mayo de 2026</p>
        </div>
        <div className="flex justify-center">
          <img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80" alt="Estudiantes" className="h-[300px] w-full max-w-[430px] rounded-2xl object-cover shadow-2xl xl:h-[400px]" />
        </div>
      </div>
    )
  },
  {
    id: 3,
    bg: 'bg-white',
    content: (
      <div className="grid h-full grid-cols-1 items-center lg:grid-cols-2">
        <div className="p-8 text-secondary lg:p-16 xl:p-20">
          <h2 className="mb-2 text-2xl font-bold">ADMISIONES</h2>
          <h1 className="mb-4 text-4xl font-black leading-tight text-[#0056A8] xl:text-5xl">EXAMEN DE <br/>ADMISIÓN</h1>
          <h2 className="mb-6 text-4xl font-bold text-accent xl:text-5xl">PUCE-I 2026</h2>
          
          <div className="rounded-r-3xl bg-[#0056A8] p-5 text-white lg:-ml-16 lg:pl-16 xl:-ml-20 xl:pl-20">
            <h3 className="mb-1 text-xl font-bold text-accent xl:text-2xl">Inscripciones Abiertas</h3>
            <p className="text-lg">• Del 14 de mayo al 15 de junio de 2026</p>
          </div>
        </div>
        <div className="h-full min-h-[300px]">
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
          <a href="https://www.puce.edu.ec/sitios/formularios/sugerencias/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors">BUZÓN DE SUGERENCIAS</a>
          <a href="mailto:uci@pucesi.edu.ec"><Mail size={18} className="text-secondary hover:text-primary cursor-pointer" /></a>
        </div>
      </nav>

      {/* Hero Section with Slider and Right Menu */}
      <div id="inicio" className="relative flex min-h-[560px] overflow-hidden">
        
        {/* Slider Area (Left 75%) */}
        <div className="relative min-h-[560px] w-[75%]">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.5 }}
              className={`min-h-[560px] w-full ${slides[currentSlide].bg}`}
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
        <div className="flex min-h-[560px] w-[25%] flex-col justify-center bg-[#0033A0] py-8">
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
