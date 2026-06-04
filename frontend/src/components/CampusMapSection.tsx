import React from 'react';
import {
  BookOpen,
  Building2,
  Coffee,
  Copy,
  GraduationCap,
  Landmark,
  MapPin,
  Megaphone,
  Monitor,
  Trophy,
  Wallet,
} from 'lucide-react';

const campusZones = [
  {
    id: 'building-1',
    title: 'Edificio 1',
    detail: 'ENCI / Arquitectura',
    services: ['A-101', 'A-102', 'A-202', 'Bar / cafetería'],
    icon: Building2,
    className: 'left-[10%] top-[18%] w-[23%] h-[22%] bg-sky-600',
  },
  {
    id: 'building-2',
    title: 'Edificio 2',
    detail: 'ECOMS / GESTURH',
    services: ['B-101', 'B-105', 'Educación', 'Comunicación'],
    icon: GraduationCap,
    className: 'left-[38%] top-[12%] w-[21%] h-[24%] bg-indigo-700',
  },
  {
    id: 'building-3',
    title: 'Edificio 3',
    detail: 'Ingeniería / Idiomas',
    services: ['C-301', 'LAB-01', 'LAB-02', 'Carnet piso 3'],
    icon: Monitor,
    className: 'right-[9%] top-[19%] w-[24%] h-[23%] bg-emerald-700',
  },
  {
    id: 'building-4',
    title: 'Edificio 4',
    detail: 'ECAA / Diseño',
    services: ['Dirección Estudiantes', 'Secretaría', 'Tesorería', 'Copias'],
    icon: Wallet,
    className: 'left-[17%] bottom-[16%] w-[30%] h-[25%] bg-amber-600',
  },
  {
    id: 'library',
    title: 'Biblioteca',
    detail: 'Consulta y recursos digitales',
    services: ['Préstamos', 'Bases digitales', 'Turnitin'],
    icon: BookOpen,
    className: 'right-[16%] bottom-[17%] w-[25%] h-[23%] bg-slate-700',
  },
];

const servicePoints = [
  { label: 'Entrada principal', value: 'Av. Jorge Guzmán Rueda y Av. Aurelio Espinosa Pólit', icon: MapPin },
  { label: 'Bar / cafetería', value: 'Edificio 1, planta baja', icon: Coffee },
  { label: 'Copias e impresión', value: 'Zona de servicios estudiantiles, Edificio 4', icon: Copy },
  { label: 'Centro Fernando Rielo', value: 'Eventos y actos académicos', icon: Landmark },
  { label: 'Computación Sala 1', value: 'Laboratorios / Edificio 3', icon: Monitor },
  { label: 'Estadio PUCESI', value: 'Actividades deportivas', icon: Trophy },
  { label: 'Carnet institucional', value: 'Comunicación y Marketing, Edificio 3 piso 3', icon: Megaphone },
];

const CampusMapSection: React.FC = () => {
  return (
    <section id="mapa-campus" className="bg-[#f7fafc] py-16 px-6 sm:px-8">
      <div className="container mx-auto">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold text-[#0033A0]">Campus PUCE Ibarra</p>
            <h2 className="mt-1 text-3xl font-bold text-[#1f2937]">Mapa del campus y servicios</h2>
          </div>
          <a
            href="https://www.pucesi.edu.ec/webs2/tourvirtual/"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center justify-center gap-2 self-start rounded-md bg-[#0033A0] px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-[#00277a] md:self-auto"
          >
            <MapPin size={17} />
            Tour virtual oficial
          </a>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-8 xl:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.65fr)]">
          <div className="grid gap-3 md:hidden">
            {campusZones.map((zone) => {
              const Icon = zone.icon;
              return (
                <div key={zone.id} className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
                  <div className="flex items-start gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-[#e6f7fd] text-[#0033A0]">
                      <Icon size={20} />
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-slate-900">{zone.title}</h3>
                      <p className="text-sm text-slate-600">{zone.detail}</p>
                      <div className="mt-3 flex flex-wrap gap-1.5">
                        {zone.services.map((service) => (
                          <span key={service} className="rounded bg-slate-100 px-2 py-1 text-[11px] font-semibold text-slate-700">
                            {service}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="relative hidden min-h-[520px] overflow-hidden rounded-md border border-slate-200 bg-white shadow-sm md:block">
            <div className="absolute inset-6 rounded-md border-2 border-dashed border-slate-300" />
            <div className="absolute left-[6%] top-1/2 h-8 w-[88%] -translate-y-1/2 rounded-full bg-slate-200" />
            <div className="absolute left-1/2 top-[8%] h-[84%] w-8 -translate-x-1/2 rounded-full bg-slate-200" />
            <div className="absolute left-8 top-1/2 z-10 -translate-y-1/2 rounded-md bg-white px-3 py-2 text-xs font-semibold text-slate-700 shadow-sm">
              Acceso principal
            </div>

            {campusZones.map((zone) => {
              const Icon = zone.icon;
              return (
                <div
                  key={zone.id}
                  className={`absolute z-20 flex flex-col justify-between rounded-md p-4 text-white shadow-md ${zone.className}`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="text-lg font-bold leading-tight">{zone.title}</h3>
                      <p className="mt-1 text-xs font-medium text-white/85">{zone.detail}</p>
                    </div>
                    <Icon size={24} className="shrink-0 text-white/90" />
                  </div>
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {zone.services.map((service) => (
                      <span key={service} className="rounded bg-white/18 px-2 py-1 text-[11px] font-semibold">
                        {service}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}

            <div className="absolute bottom-5 left-6 right-6 z-20 rounded-md bg-white/95 px-4 py-3 text-sm text-slate-700 shadow-sm">
              Biblioteca, Centro de Convenciones Fernando Rielo, Banco de Germoplasma, Laboratorio de Cómputo Sala 1 y Estadio PUCESI se tratan como puntos estratégicos del campus.
            </div>
          </div>

          <div className="rounded-md border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="text-lg font-bold text-[#1f2937]">Ubicaciones rápidas</h3>
            <div className="mt-5 space-y-3">
              {servicePoints.map((point) => {
                const Icon = point.icon;
                return (
                  <div key={point.label} className="flex gap-3 border-b border-slate-100 pb-3 last:border-b-0 last:pb-0">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-[#e6f7fd] text-[#0033A0]">
                      <Icon size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-slate-800">{point.label}</p>
                      <p className="text-sm text-slate-600">{point.value}</p>
                    </div>
                  </div>
                );
              })}
            </div>
            <p className="mt-5 rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-900">
              Los servicios como copias o cafetería pueden cambiar de punto activo; el chatbot indicará confirmar en garita o Dirección de Estudiantes cuando sea necesario.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CampusMapSection;
