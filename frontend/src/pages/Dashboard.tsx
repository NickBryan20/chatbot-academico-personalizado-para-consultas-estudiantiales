import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Menu, Globe, Bell, MessageSquare, ChevronDown, ChevronRight,
  Clock, Calendar, Folder, BookOpen, User as UserIcon
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import api from '../services/api';
import ChatWindow from '../components/ChatWindow';

interface CourseGrade {
  subject_name: string;
}

interface ScheduleItem {
  day_display: string;
  start_time: string;
  end_time: string;
  subject_details: {
    name: string;
  };
  professor_details?: {
    full_name: string;
  };
  classroom_details?: {
    code: string;
  };
}

interface ActivitySubmission {
  file?: string;
  grade?: number | string | null;
  submitted_at: string;
}

interface StudentActivity {
  id: string | number;
  title: string;
  subject_name: string;
  due_date: string;
  created_at: string;
  file?: string;
  submission?: ActivitySubmission | null;
}

interface NotificationItem {
  id?: string | number;
  title?: string;
  message?: string;
}

interface SidebarItemProps {
  icon: React.ReactNode;
  label: string;
  active: boolean;
  onClick: () => void;
}

/**
 * Dashboard.tsx
 * Componente principal del área personal del estudiante.
 * Gestiona el layout (Sidebar, Header, Main Content) y obtiene los datos
 * académicos desde el backend (horarios, calificaciones, actividades pendientes).
 */
const Dashboard: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  
  // Estados para la navegación visual (Sidebar y Pestañas)
  const [activeTab, setActiveTab] = useState('area-personal');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [coursesExpanded, setCoursesExpanded] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState<CourseGrade | null>(null);
  
  // Estado para la subida de deberes (Modal de Actividad)
  const [selectedActivity, setSelectedActivity] = useState<StudentActivity | null>(null);
  
  // Estados para almacenar la data obtenida del Backend (Django)
  const [grades, setGrades] = useState<CourseGrade[]>([]);
  const [schedule, setSchedule] = useState<ScheduleItem[]>([]);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [activities, setActivities] = useState<StudentActivity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [gradesRes, scheduleRes, notifRes, actRes] = await Promise.all([
          api.get('/students/grades/'),
          api.get('/students/schedule/'),
          api.get('/students/notifications/?unread_only=true'),
          api.get('/students/activities/')
        ]);
        setGrades(gradesRes.data.grades);
        setSchedule(scheduleRes.data.schedule);
        setNotifications(notifRes.data);
        setActivities(actRes.data);
      } catch (err) {
        console.error('Error fetching dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  // Group grades to get unique courses for "Mis Cursos"
  const uniqueCourses = grades.filter((g, index, self) => 
    index === self.findIndex((t) => t.subject_name === g.subject_name)
  );

  return (
    <div className="flex flex-col min-h-screen bg-white text-[#333333] font-sans">
      {/* Top Navbar */}
      <header className="h-14 border-b border-gray-200 flex items-center justify-between px-4 bg-white sticky top-0 z-40">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 bg-[#00AEEF] text-white rounded-md hover:bg-[#0096ce] transition-colors"
          >
            <Menu size={20} />
          </button>
          <img 
            src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png" 
            alt="PUCE Ibarra" 
            className="h-8 object-contain cursor-pointer"
            onClick={() => navigate('/')}
          />
        </div>
        
        <div className="flex items-center gap-4">
          <button className="text-[#00AEEF] hover:bg-gray-100 p-2 rounded-full transition-colors hidden sm:block">
            <Globe size={20} />
          </button>
          <button className="text-[#00AEEF] hover:bg-gray-100 p-2 rounded-full transition-colors relative">
            <Bell size={20} />
            {notifications.length > 0 && (
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            )}
          </button>
          <button className="text-[#00AEEF] hover:bg-gray-100 p-2 rounded-full transition-colors">
            <MessageSquare size={20} />
          </button>
          
          <div className="flex items-center gap-2 ml-2 pl-2 border-l border-gray-200 cursor-pointer group relative">
            <span className="text-xs font-bold text-[#00AEEF] uppercase hidden md:block tracking-wide">
              {user?.first_name} {user?.last_name}
            </span>
            <div className="w-8 h-8 bg-gray-200 rounded-full overflow-hidden border border-gray-300 flex items-center justify-center text-gray-500">
               <UserIcon size={16} />
            </div>
            <ChevronDown size={14} className="text-gray-400" />
            
            {/* Dropdown Logout */}
            <div className="absolute top-full right-0 mt-2 w-48 bg-white border border-gray-200 shadow-lg rounded-md hidden group-hover:block z-50">
              <button onClick={handleLogout} className="w-full text-left px-4 py-3 text-sm hover:bg-gray-50 text-red-600 font-medium border-t border-gray-100">
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <AnimatePresence>
          {isSidebarOpen && (
            <motion.aside 
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 260, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              className="bg-[#eef8fa] border-r border-gray-200 flex flex-col shrink-0 z-30 overflow-hidden"
            >
              <nav className="p-4 space-y-1 overflow-y-auto">
                <SidebarItem 
                  icon={<Clock size={18} />} 
                  label="Área personal" 
                  active={activeTab === 'area-personal'} 
                  onClick={() => { setActiveTab('area-personal'); setSelectedCourse(null); setSelectedActivity(null); }}
                />
                <SidebarItem 
                  icon={<Calendar size={18} />} 
                  label="Calendario" 
                  active={activeTab === 'calendario'} 
                  onClick={() => { setActiveTab('calendario'); setSelectedCourse(null); setSelectedActivity(null); }}
                />
                <SidebarItem 
                  icon={<Folder size={18} />} 
                  label="Archivos privados" 
                  active={activeTab === 'archivos'} 
                  onClick={() => { setActiveTab('archivos'); setSelectedCourse(null); setSelectedActivity(null); }}
                />
                
                <div className="pt-2">
                  <button 
                    onClick={() => setCoursesExpanded(!coursesExpanded)}
                    className="w-full flex items-center justify-between px-3 py-2 text-sm text-[#333333] hover:bg-[#dcedf0] rounded-md transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <BookOpen size={18} className="text-[#666]" />
                      <span>Mis cursos</span>
                    </div>
                    {coursesExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                  </button>
                  
                  <AnimatePresence>
                    {coursesExpanded && (
                      <motion.div 
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="pl-8 pr-2 py-1 space-y-1 overflow-hidden"
                      >
                        {uniqueCourses.map((course, idx) => (
                          <button 
                            key={idx}
                            onClick={() => setSelectedCourse(course)}
                            className="w-full text-left text-xs text-[#00AEEF] hover:underline py-1.5 truncate block"
                          >
                            {course.subject_name.substring(0, 30)}...
                          </button>
                        ))}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </nav>
              
              <div className="mt-auto bg-[#00AEEF] text-white p-3 text-[11px] font-medium flex items-center gap-2 cursor-pointer hover:bg-[#0096ce] transition-colors">
                <div className="w-5 h-5 bg-white rounded-full flex items-center justify-center text-[#00AEEF]">
                  <UserIcon size={12} />
                </div>
                <span>Configuraciones de accesibilidad</span>
              </div>
            </motion.aside>
          )}
        </AnimatePresence>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto bg-[#f8f9fa] p-4 md:p-6">
          {loading ? (
             <div className="flex items-center justify-center h-full">
               <div className="w-10 h-10 border-4 border-gray-200 border-t-[#00AEEF] rounded-full animate-spin"></div>
             </div>
          ) : selectedActivity ? (
             // Activity details view
             <div className="bg-white shadow-sm p-8 max-w-[1000px] w-full mx-auto h-full overflow-y-auto">
               <h2 className="text-[22px] font-normal text-[#333333] mb-4 leading-tight">{selectedActivity.title}</h2>
               
               {selectedActivity.file && (
               <div className="flex items-center gap-2 mb-8 border-b border-gray-200 pb-4">
                 <div className="bg-red-600 text-white px-1 py-0.5 rounded-sm text-[9px] font-bold">PDF</div>
                 <a href={selectedActivity.file} target="_blank" rel="noreferrer" className="text-[#00AEEF] text-[13px] hover:underline underline-offset-2">Descargar instrucciones</a>
                 <span className="text-[13px] text-[#333333] ml-1">{new Date(selectedActivity.created_at).toLocaleDateString()}</span>
               </div>
               )}
               
               <h3 className="text-[20px] font-normal text-[#333333] mb-4">Estado de la entrega</h3>
               
               <div className="mb-8">
                 <div className="grid grid-cols-12 border-b border-gray-200 bg-[#f8f9fa]">
                   <div className="col-span-3 p-3 font-bold text-[13px] text-[#333333]">Estado de la entrega</div>
                   <div className="col-span-9 p-3 text-[13px] text-[#333333] bg-white border-l border-gray-200">
                     {selectedActivity.submission ? 'Entregado' : 'No entregado'}
                   </div>
                 </div>
                 <div className="grid grid-cols-12 border-b border-gray-200 bg-[#f8f9fa]">
                   <div className="col-span-3 p-3 font-bold text-[13px] text-[#333333]">Estado de la calificación</div>
                   <div className="col-span-9 p-3 text-[13px] text-[#333333] bg-white border-l border-gray-200">
                     {selectedActivity.submission?.grade ? `${selectedActivity.submission.grade}/50` : 'Sin calificar'}
                   </div>
                 </div>
                 <div className="grid grid-cols-12 border-b border-gray-200 bg-[#f8f9fa]">
                   <div className="col-span-3 p-3 font-bold text-[13px] text-[#333333]">Fecha de entrega</div>
                   <div className="col-span-9 p-3 text-[13px] text-[#333333] bg-white border-l border-gray-200">
                     {new Date(selectedActivity.due_date).toLocaleString()}
                   </div>
                 </div>
                 <div className="grid grid-cols-12 border-b border-gray-200 bg-[#f8f9fa]">
                   <div className="col-span-3 p-3 font-bold text-[13px] text-[#333333]">Tiempo restante</div>
                   <div className="col-span-9 p-3 text-[13px] text-[#333333] bg-white border-l border-gray-200">
                     {selectedActivity.submission ? 'La tarea fue enviada' : '...'}
                   </div>
                 </div>
                 <div className="grid grid-cols-12 border-b border-gray-200 bg-[#f8f9fa]">
                   <div className="col-span-3 p-3 font-bold text-[13px] text-[#333333]">Última modificación</div>
                   <div className="col-span-9 p-3 text-[13px] text-[#333333] bg-white border-l border-gray-200">
                     {selectedActivity.submission ? new Date(selectedActivity.submission.submitted_at).toLocaleString() : '-'}
                   </div>
                 </div>
                 {selectedActivity.submission && selectedActivity.submission.file && (
                 <div className="grid grid-cols-12 border-b border-gray-200 bg-[#f8f9fa]">
                   <div className="col-span-3 p-3 font-bold text-[13px] text-[#333333] flex items-center">Archivos enviados</div>
                   <div className="col-span-9 p-3 text-[13px] text-[#333333] bg-white border-l border-gray-200 flex items-center gap-1">
                     <a href={selectedActivity.submission.file} target="_blank" rel="noreferrer" className="text-[#00AEEF] hover:underline underline-offset-2">Ver archivo enviado</a>
                   </div>
                 </div>
                 )}
               </div>
               
               <div className="flex flex-col items-center gap-4 mt-8 mb-16">
                 <label className="bg-[#e9ecef] border border-[#ced4da] text-[#495057] px-4 py-2 text-[14px] rounded hover:bg-[#dde0e3] transition-colors shadow-sm cursor-pointer">
                   {selectedActivity.submission ? 'Actualizar entrega' : 'Agregar entrega'}
                   <input type="file" className="hidden" onChange={async (e) => {
                     const file = e.target.files?.[0];
                     if (file) {
                       const formData = new FormData();
                       formData.append('file', file);
                       try {
                         const res = await api.post(`/students/activities/${selectedActivity.id}/submit/`, formData, {
                           headers: { 'Content-Type': 'multipart/form-data' }
                         });
                         const newAct = { ...selectedActivity, submission: res.data };
                         setSelectedActivity(newAct);
                         setActivities(activities.map(a => a.id === selectedActivity.id ? newAct : a));
                         alert("¡Archivo subido exitosamente!");
                      } catch {
                         alert("Error al subir archivo");
                       }
                     }
                   }} />
                 </label>
                 <p className="text-[14px] text-[#333333]">
                   {selectedActivity.submission ? 'Ya enviaste tu archivo.' : 'Todavía no has realizado una entrega.'}
                 </p>
               </div>
             </div>
          ) : activeTab === 'calendario' ? (
             // Full Calendar View
             <div className="max-w-6xl mx-auto h-full flex flex-col">
               <div className="bg-white border border-gray-200 p-6 mb-6">
                 <h1 className="text-2xl font-light text-[#666666] uppercase tracking-wide">Calendario Académico</h1>
                 <p className="text-sm text-gray-500 mt-2">Horario de clases para el periodo actual con detalle de horas, profesores y aulas.</p>
               </div>
               
               <div className="flex-1 bg-white border border-gray-200 overflow-hidden flex flex-col min-h-[500px]">
                 <div className="grid grid-cols-5 border-b border-gray-200 bg-gray-50">
                   {['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'].map(day => (
                     <div key={day} className="p-3 text-center font-bold text-[#00AEEF] text-sm border-r border-gray-200 last:border-r-0">
                       {day}
                     </div>
                   ))}
                 </div>
                 <div className="grid grid-cols-5 flex-1 overflow-y-auto bg-white">
                   {['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'].map(day => {
                     const dayItems = schedule.filter(item => item.day_display === day).sort((a, b) => a.start_time.localeCompare(b.start_time));
                     return (
                       <div key={day} className="border-r border-gray-200 last:border-r-0 p-2 space-y-3 relative">
                         {dayItems.map((item, idx) => (
                           <div key={idx} className="bg-[#eef8fa] border-l-4 border-[#00AEEF] p-3 rounded-sm shadow-sm hover:shadow-md transition-shadow group">
                             <h4 className="text-[12px] font-bold text-[#333333] mb-2 leading-tight group-hover:text-[#00AEEF] transition-colors">{item.subject_details.name}</h4>
                             <div className="text-[11px] text-gray-600 space-y-1.5">
                               <div className="flex items-center gap-2">
                                 <Clock size={12} className="text-[#00AEEF]" />
                                 <span className="font-medium">{item.start_time.substring(0,5)} - {item.end_time.substring(0,5)}</span>
                               </div>
                               <div className="flex items-center gap-2">
                                 <UserIcon size={12} className="text-[#00AEEF]" />
                                 <span className="truncate" title={item.professor_details?.full_name}>{item.professor_details?.full_name || 'Prof. Asignado'}</span>
                               </div>
                               <div className="flex items-center gap-2">
                                 <BookOpen size={12} className="text-[#00AEEF]" />
                                 <span>Aula {item.classroom_details?.code || 'N/A'}</span>
                               </div>
                             </div>
                           </div>
                         ))}
                         {dayItems.length === 0 && (
                           <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-50">
                             <span className="text-[10px] text-gray-400 uppercase tracking-widest rotate-[-90deg]">Libre</span>
                           </div>
                         )}
                       </div>
                     );
                   })}
                 </div>
               </div>
             </div>
          ) : selectedCourse ? (
             // Course Internal View
             <div className="bg-white border border-gray-200 shadow-sm p-8 max-w-5xl mx-auto">
               <div className="border-b border-gray-200 pb-4 mb-6">
                 <h1 className="text-2xl font-light text-[#333333] uppercase">{selectedCourse.subject_name}</h1>
                 <div className="text-[11px] font-medium text-gray-500 mt-3 flex items-center gap-2">
                   <span className="text-[#00AEEF] cursor-pointer hover:underline" onClick={() => setSelectedCourse(null)}>Mis cursos</span>
                   <ChevronRight size={12} />
                   <span className="bg-[#eef8fa] px-3 py-1 text-[#00AEEF]">{selectedCourse.subject_name}</span>
                 </div>
               </div>
               
               <div className="flex gap-4 mb-8">
                 <div className="flex items-center gap-2 text-[#00AEEF] text-sm font-medium hover:underline cursor-pointer">
                   <MessageSquare size={16} />
                   Avisos
                 </div>
               </div>

               <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                 {[1, 2, 3, 4, 5, 6].map(i => (
                   <div key={i} className="border border-gray-200 border-t-4 border-t-[#00AEEF] bg-white p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col items-center justify-center min-h-[140px] cursor-pointer group">
                     <div className="w-16 h-16 rounded-full mb-3 flex items-center justify-center text-gray-400 group-hover:text-[#00AEEF] transition-colors">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                     </div>
                     <span className="text-[#666666] font-medium text-sm">Mosaico {i}</span>
                   </div>
                 ))}
               </div>
             </div>
          ) : (
             // Dashboard Overview View
             <div className="max-w-6xl mx-auto">
               <div className="bg-white border border-gray-200 p-8 mb-6 relative overflow-hidden">
                 <h1 className="text-3xl font-light text-[#666666] uppercase tracking-wide relative z-10">PRIMER PERIODO 2026</h1>
               </div>

               <div className="bg-white border border-gray-200 p-6 md:p-8 relative">
                 <h2 className="text-xl font-medium text-[#00AEEF] text-center mb-10">Mis cursos</h2>
                 
                 <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                   {uniqueCourses.map((course, idx) => (
                     <div key={idx} className="border border-gray-200 bg-white flex flex-col group hover:border-[#00AEEF] transition-colors">
                       <div className="h-40 bg-[#f4f6f8] relative overflow-hidden flex flex-col items-center justify-center p-4">
                         
                         {/* Placeholder illustration from screenshot (green head with lightbulb) */}
                         <div className="relative transform group-hover:scale-105 transition-transform duration-500">
                           <svg width="80" height="80" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                             <path d="M50 90C72.0914 90 90 72.0914 90 50C90 27.9086 72.0914 10 50 10C27.9086 10 10 27.9086 10 50C10 72.0914 27.9086 90 50 90Z" fill="#008767"/>
                             <path d="M50 20C44.4772 20 40 24.4772 40 30C40 32.5516 40.9576 34.8804 42.5186 36.6433C43.1895 37.3888 44 38.653 44 40V45H56V40C56 38.653 56.8105 37.3888 57.4814 36.6433C59.0424 34.8804 60 32.5516 60 30C60 24.4772 55.5228 20 50 20Z" fill="#FFC107"/>
                           </svg>
                         </div>
                         
                         {/* Professor Avatar Placeholder */}
                         <div className="absolute -bottom-5 right-4 w-12 h-12 bg-white rounded-full border-4 border-[#f4f6f8] shadow-sm overflow-hidden z-10 flex items-center justify-center">
                            <UserIcon size={20} className="text-gray-400" />
                         </div>
                       </div>
                       
                       <div className="p-5 flex-1 flex flex-col">
                         <h3 className="text-[12px] font-bold text-[#00AEEF] uppercase mb-4 h-12 overflow-hidden line-clamp-3 leading-snug">
                           {course.subject_name}
                         </h3>
                         <div className="mt-auto border-t border-gray-100 pt-4 flex justify-center">
                           <button 
                             onClick={() => setSelectedCourse(course)}
                             className="bg-[#00AEEF] text-white text-[12px] font-bold px-5 py-2 rounded-sm hover:bg-[#0096ce] transition-colors w-24"
                           >
                             Acceso
                           </button>
                         </div>
                       </div>
                     </div>
                   ))}
                 </div>
               </div>
             </div>
          )}
        </main>

        {/* Right Sidebar (Events & Online Users) */}
        <aside className="w-[300px] bg-white border-l border-gray-200 flex flex-col hidden xl:flex shrink-0 overflow-y-auto custom-scrollbar">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-[16px] font-normal text-[#333333] mb-4">Próximos eventos</h3>
            
            <div className="space-y-4 mb-4">
              {activities.length > 0 ? activities.slice(0, 3).map((act, idx) => (
                <div className="flex gap-3" key={idx}>
                  <div className="bg-[#00AEEF] text-white p-1 rounded-sm h-fit mt-0.5"><Folder size={12} fill="white" /></div>
                  <div onClick={() => { setSelectedActivity(act); setSelectedCourse(null); setActiveTab('actividad'); }}>
                    <p className="text-[#00AEEF] hover:underline cursor-pointer text-[13px] leading-tight mb-1">
                      {act.title} pendiente
                    </p>
                    <p className="text-[#666666] text-[13px]">{new Date(act.due_date).toLocaleDateString()}</p>
                  </div>
                </div>
              )) : <p className="text-[13px] text-[#333333]">No hay eventos próximos.</p>}
            </div>
            
            <button className="text-[13px] text-[#00AEEF] hover:underline" onClick={() => setActiveTab('calendario')}>Ir al calendario...</button>
          </div>

          <div className="p-6 border-b border-gray-200">
            <h3 className="text-[16px] font-normal text-[#333333] mb-4">Línea de tiempo</h3>
            
            <div className="flex gap-2 mb-6">
              <div className="border border-gray-300 rounded px-3 py-1.5 flex items-center gap-2 cursor-pointer flex-1 justify-between hover:bg-gray-50">
                <Clock size={16} className="text-gray-500" />
                <ChevronDown size={14} className="text-gray-500" />
              </div>
              <div className="border border-gray-300 rounded px-3 py-1.5 flex items-center gap-2 cursor-pointer flex-1 justify-between hover:bg-gray-50">
                <div className="flex flex-col gap-[2px] w-4 items-center">
                  <div className="w-full h-0.5 bg-gray-500"></div>
                  <div className="w-3/4 h-0.5 bg-gray-500"></div>
                  <div className="w-1/2 h-0.5 bg-gray-500"></div>
                </div>
                <ChevronDown size={14} className="text-gray-500" />
              </div>
            </div>
            
            <div className="space-y-4 mb-6">
              {activities.length > 0 ? activities.slice(0, 3).map((act, idx) => (
                <div key={idx} className="mb-4">
                  <h4 className="text-[13px] text-[#666666] mb-2">{new Date(act.due_date).toLocaleDateString()}</h4>
                  <div className="flex gap-3">
                    <div className="bg-[#00AEEF] text-white p-1 rounded-sm h-fit mt-1"><Folder size={12} fill="white" /></div>
                    <div className="flex-1 border-b border-gray-100 pb-3">
                      <div className="flex justify-between items-start gap-2 cursor-pointer" onClick={() => { setSelectedActivity(act); setSelectedCourse(null); setActiveTab('actividad'); }}>
                        <p className="text-[#333333] hover:text-[#00AEEF] text-[13px] leading-tight transition-colors line-clamp-2">{act.title}</p>
                        <span className="text-[13px] text-[#333333]">{new Date(act.due_date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                      </div>
                      <p className="text-[11px] text-[#666666] uppercase mt-0.5">{act.subject_name}</p>
                      <button onClick={() => { setSelectedActivity(act); setSelectedCourse(null); setActiveTab('actividad'); }} className="text-[#00AEEF] text-[13px] mt-2 hover:underline">
                        {act.submission ? 'Actualizar entrega' : 'Agregar entrega'}
                      </button>
                    </div>
                  </div>
                </div>
              )) : <p className="text-[13px] text-[#333333]">No hay tareas pendientes.</p>}
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-[13px] text-[#333333]">Mostrar</span>
              <div className="border border-gray-300 rounded px-2 py-1 flex items-center gap-2 cursor-pointer hover:bg-gray-50">
                <span className="text-[13px]">5</span>
                <ChevronDown size={14} className="text-gray-500" />
              </div>
            </div>
          </div>

          <div className="p-6 border-b border-gray-200">
            <h3 className="text-[16px] font-normal text-[#333333] mb-4">Archivos privados</h3>
            <p className="text-[13px] text-[#333333]">No hay archivos disponibles</p>
          </div>

          <div className="p-6">
            <h3 className="text-[16px] font-normal text-[#333333] mb-4">Usuarios en línea</h3>
            <p className="text-[13px] text-[#666666] mb-5">
              12 usuarios online (últimos 5 minutos)
            </p>
            
            <div className="space-y-4">
               <div className="flex items-center gap-3 text-[12px]">
                 <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center shrink-0">
                   <UserIcon size={14} className="text-gray-400" />
                 </div>
                 <span className="text-[#00AEEF] font-bold uppercase truncate">{user?.first_name} {user?.last_name}</span>
                 <MessageSquare size={16} className="text-[#00AEEF] ml-auto shrink-0 cursor-pointer" />
               </div>
               
               <div className="flex items-center gap-3 text-[12px]">
                 <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center shrink-0">
                   <UserIcon size={14} className="text-gray-400" />
                 </div>
                 <span className="text-gray-600 uppercase truncate">JESSICA CAROLINA ARCOS</span>
                 <MessageSquare size={16} className="text-[#00AEEF] ml-auto shrink-0 cursor-pointer" />
               </div>
               
               <div className="flex items-center gap-3 text-[12px]">
                 <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center shrink-0">
                   <UserIcon size={14} className="text-gray-400" />
                 </div>
                 <span className="text-gray-600 uppercase truncate">BRITANY PAOLA TORRES</span>
                 <MessageSquare size={16} className="text-[#00AEEF] ml-auto shrink-0 cursor-pointer" />
               </div>
            </div>
          </div>
        </aside>
      </div>

      <ChatWindow unreadNotifications={notifications} />
    </div>
  );
};

const SidebarItem = ({ icon, label, active, onClick }: SidebarItemProps) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-sm transition-all text-[13px] ${
      active 
        ? 'bg-[#dcedf0] text-[#00AEEF] font-bold border-l-[3px] border-[#00AEEF]' 
        : 'text-[#333333] hover:bg-[#dcedf0] border-l-[3px] border-transparent'
    }`}
  >
    <span className={active ? 'text-[#00AEEF]' : 'text-[#666666]'}>{icon}</span>
    {label}
  </button>
);

export default Dashboard;
