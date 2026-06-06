import React, { useEffect, useState } from 'react';
import { BookOpen, Calendar, FileUp, LogOut, Plus, User as UserIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuthStore } from '../store/authStore';

interface Subject {
  id: string;
  name: string;
  code: string;
  semester: number;
}

interface ScheduleItem {
  id: string;
  day_display: string;
  start_time: string;
  end_time: string;
  subject_details: Subject;
  classroom_details?: { code: string };
}

interface Activity {
  id: string;
  subject_name: string;
  title: string;
  description: string;
  due_date: string;
  file?: string;
  submissions_count: number;
}

type ApiError = {
  response?: {
    data?: {
      error?: string;
    };
  };
};

const getApiErrorMessage = (err: unknown, fallback: string) => (
  (err as ApiError).response?.data?.error || fallback
);

const TeacherDashboard: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [schedule, setSchedule] = useState<ScheduleItem[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    subject: '',
    title: '',
    description: '',
    dueDate: '',
    file: null as File | null,
  });

  const loadTeacherData = async () => {
    setLoading(true);
    setError('');
    try {
      const [subjectsRes, scheduleRes, activitiesRes] = await Promise.all([
        api.get('/students/teacher/subjects/'),
        api.get('/students/teacher/schedule/'),
        api.get('/students/teacher/activities/'),
      ]);
      setSubjects(subjectsRes.data);
      setSchedule(scheduleRes.data.schedule);
      setActivities(activitiesRes.data);
      if (!form.subject && subjectsRes.data.length > 0) {
        setForm((current) => ({ ...current, subject: subjectsRes.data[0].id }));
      }
    } catch (err: unknown) {
      setError(getApiErrorMessage(err, 'No se pudo cargar la información docente.'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTeacherData();
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!form.subject || !form.title.trim() || !form.dueDate) return;

    setSaving(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('subject', form.subject);
      formData.append('title', form.title.trim());
      formData.append('description', form.description.trim());
      formData.append('due_date', new Date(form.dueDate).toISOString());
      if (form.file) {
        formData.append('file', form.file);
      }

      await api.post('/students/teacher/activities/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setForm({ subject: form.subject, title: '', description: '', dueDate: '', file: null });
      await loadTeacherData();
    } catch (err: unknown) {
      setError(getApiErrorMessage(err, 'No se pudo crear la actividad.'));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8f9fa] text-[#333333] font-sans">
      <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-5 sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <img
            src="https://www.pucesi.edu.ec/webs2/wp-content/uploads/2025/07/PUCE-IBARRA-1.png"
            alt="PUCE Ibarra"
            className="h-8 object-contain"
          />
          <div className="border-l border-gray-200 pl-3">
            <p className="text-xs uppercase tracking-wide text-gray-500">Aula virtual</p>
            <h1 className="text-sm font-bold text-[#0056A8]">Panel docente</h1>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 text-xs font-bold text-[#00AEEF] uppercase">
            <UserIcon size={16} />
            {user?.first_name} {user?.last_name}
          </div>
          <button
            onClick={handleLogout}
            className="h-9 px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-sm flex items-center gap-2 text-sm"
          >
            <LogOut size={16} />
            Salir
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-5 grid grid-cols-1 xl:grid-cols-[1fr_380px] gap-5">
        <section className="space-y-5">
          <div className="bg-white border border-gray-200 p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-[#0056A8] flex items-center gap-2">
                <Calendar size={18} />
                Horario asignado
              </h2>
              <span className="text-xs text-gray-500">Periodo 2026-01</span>
            </div>
            {loading ? (
              <div className="h-28 flex items-center justify-center text-sm text-gray-500">Cargando...</div>
            ) : schedule.length === 0 ? (
              <p className="text-sm text-gray-500">No hay horarios asignados.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {schedule.map((item) => (
                  <div key={item.id} className="border border-gray-200 p-4 bg-[#f8fbfc]">
                    <h3 className="text-sm font-bold text-[#333333]">{item.subject_details.name}</h3>
                    <p className="text-xs text-gray-600 mt-2">
                      {item.day_display} · {item.start_time.substring(0, 5)} - {item.end_time.substring(0, 5)}
                    </p>
                    <p className="text-xs text-[#00AEEF] mt-1">Aula {item.classroom_details?.code || 'N/A'}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="bg-white border border-gray-200 p-5">
            <h2 className="text-lg font-semibold text-[#0056A8] flex items-center gap-2 mb-4">
              <BookOpen size={18} />
              Actividades publicadas
            </h2>
            {activities.length === 0 ? (
              <p className="text-sm text-gray-500">Aún no hay actividades creadas.</p>
            ) : (
              <div className="space-y-3">
                {activities.map((activity) => (
                  <div key={activity.id} className="border border-gray-200 p-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                    <div>
                      <h3 className="text-sm font-bold text-[#333333]">{activity.title}</h3>
                      <p className="text-xs text-[#00AEEF] mt-1">{activity.subject_name}</p>
                      {activity.description && <p className="text-xs text-gray-500 mt-2">{activity.description}</p>}
                    </div>
                    <div className="text-xs text-gray-600 md:text-right">
                      <p>Entrega: {new Date(activity.due_date).toLocaleString()}</p>
                      <p>{activity.submissions_count} entregas recibidas</p>
                      {activity.file && (
                        <a href={activity.file} target="_blank" rel="noreferrer" className="text-[#00AEEF] hover:underline">
                          Ver instrucciones
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        <aside className="bg-white border border-gray-200 p-5 h-fit">
          <h2 className="text-lg font-semibold text-[#0056A8] flex items-center gap-2 mb-4">
            <Plus size={18} />
            Nueva actividad
          </h2>
          {error && <div className="mb-4 text-sm text-red-600 bg-red-50 border border-red-100 p-3">{error}</div>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-gray-600 uppercase mb-1">Materia</label>
              <select
                value={form.subject}
                onChange={(event) => setForm({ ...form, subject: event.target.value })}
                className="w-full border border-gray-300 p-2.5 text-sm outline-none focus:border-[#00AEEF]"
                required
              >
                {subjects.map((subject) => (
                  <option key={subject.id} value={subject.id}>
                    {subject.code} · {subject.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-600 uppercase mb-1">Título</label>
              <input
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
                className="w-full border border-gray-300 p-2.5 text-sm outline-none focus:border-[#00AEEF]"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-600 uppercase mb-1">Descripción</label>
              <textarea
                value={form.description}
                onChange={(event) => setForm({ ...form, description: event.target.value })}
                rows={4}
                className="w-full border border-gray-300 p-2.5 text-sm outline-none focus:border-[#00AEEF] resize-none"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-600 uppercase mb-1">Fecha de entrega</label>
              <input
                type="datetime-local"
                value={form.dueDate}
                onChange={(event) => setForm({ ...form, dueDate: event.target.value })}
                className="w-full border border-gray-300 p-2.5 text-sm outline-none focus:border-[#00AEEF]"
                required
              />
            </div>
            <label className="border border-dashed border-gray-300 p-4 text-sm text-gray-600 flex items-center gap-2 cursor-pointer hover:bg-gray-50">
              <FileUp size={18} className="text-[#00AEEF]" />
              {form.file ? form.file.name : 'Adjuntar instrucciones'}
              <input
                type="file"
                className="hidden"
                onChange={(event) => setForm({ ...form, file: event.target.files?.[0] || null })}
              />
            </label>
            <button
              type="submit"
              disabled={saving || subjects.length === 0}
              className="w-full bg-[#00AEEF] text-white py-2.5 text-sm font-bold hover:bg-[#0096ce] disabled:opacity-60"
            >
              {saving ? 'Publicando...' : 'Publicar actividad'}
            </button>
          </form>
        </aside>
      </main>
    </div>
  );
};

export default TeacherDashboard;
