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
    id: 'sports',
    title: 'Estadio y canchas',
    detail: 'Zona deportiva',
    services: ['Estadio', 'Basket', 'Vóley'],
    icon: Trophy,
    className: 'left-[6%] top-[24%] w-[21%] h-[33%] bg-green-700',
  },
  {
    id: 'building-1',
    title: 'Edificio 1',
    detail: 'Acceso estudiantil',
    services: ['Dirección Estudiantes', 'Bar / cafetería', 'Ingreso 1'],
    icon: Building2,
    className: 'right-[11%] bottom-[18%] w-[19%] h-[19%] bg-yellow-500',
  },
  {
    id: 'building-2',
    title: 'Edificio / Bloque 2',
    detail: 'Carnet, aulas y gastronomía',
    services: ['Carnet', '5.1.10', 'Taller gastronomía'],
    icon: GraduationCap,
    className: 'left-[48%] top-[31%] w-[18%] h-[19%] bg-rose-600',
  },
  {
    id: 'building-3',
    title: 'Edificio 3',
    detail: 'Laboratorios / copias',
    services: ['Copias', 'Laboratorios', '3.3.1'],
    icon: Monitor,
    className: 'left-[43%] bottom-[17%] w-[14%] h-[19%] bg-cyan-600',
  },
  {
    id: 'building-4',
    title: 'Edificio 4',
    detail: 'Biblioteca / servicios',
    services: ['Biblioteca', 'Bar / cafetería', 'Ingreso 4'],
    icon: Wallet,
    className: 'left-[24%] bottom-[12%] w-[22%] h-[23%] bg-violet-700',
  },
  {
    id: 'building-5',
    title: 'Edificio 5',
    detail: 'Ingreso 5',
    services: ['5.1.x', '5.2.x', 'Bloque 2'],
    icon: Building2,
    className: 'left-[49%] top-[12%] w-[18%] h-[17%] bg-orange-600',
  },
  {
    id: 'block-3',
    title: 'Bloque 3',
    detail: 'ECAA / investigación',
    services: ['Ing.', 'Germoplasma', 'Herbario'],
    icon: Landmark,
    className: 'left-[31%] top-[34%] w-[15%] h-[16%] bg-lime-600',
  },
];

const roomGuide = [
  {
    title: 'Edificio 1',
    lines: ['P1: 1.1.5, 1.1.6, 1.1.7', 'P2: 1.2.2, 1.2.3, 1.2.7, 1.2.8', 'P3-P6: aulas 1.3.x, 1.4.x, 1.5.x y 1.6.x'],
  },
  {
    title: 'Edificio 3',
    lines: ['P1 y P2: laboratorios', 'P3: laboratorios y aula 3.3.1'],
  },
  {
    title: 'Edificio 4',
    lines: ['P1: laboratorios de enfermería y biblioteca', 'P2: laboratorios ECAA, biblioteca y aula 4.2.12', 'P3: aulas 4.3.5 a 4.3.18'],
  },
  {
    title: 'Edificio 5 / Bloque 2',
    lines: ['Edificio 5: aulas 5.1.x y 5.2.x', 'Bloque 2: 5.1.10, 5.1.11, 5.0.1, 5.0.2, 5.0.3', 'Taller de gastronomía: 2.1.31'],
  },
  {
    title: 'Bloque 3',
    lines: ['P1: laboratorio de ingeniería, germoplasma y herbario'],
  },
];

const servicePoints = [
  { label: 'Entrada principal', value: 'Av. Jorge Guzmán Rueda y Av. Aurelio Espinosa Pólit', icon: MapPin },
  { label: 'Capilla', value: 'Pasando la entrada principal de la PUCESI', icon: Landmark },
  { label: 'Bar / cafetería', value: 'Edificio 1 y Edificio 4', icon: Coffee },
  { label: 'Copias e impresión', value: 'Edificio 3', icon: Copy },
  { label: 'Biblioteca', value: 'Dentro del Edificio 4', icon: BookOpen },
  { label: 'Carnet institucional', value: 'Edificio 2', icon: Megaphone },
  { label: 'Dirección de Estudiantes', value: 'Edificio 1', icon: GraduationCap },
  { label: 'Computación Sala 1', value: 'Laboratorios / Edificio 3', icon: Monitor },
  { label: 'Estadio PUCESI', value: 'Camino al Edificio 5, a la derecha junto a canchas de basket y vóley', icon: Trophy },
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
          <div className="flex flex-wrap gap-2">
            <a
              href="https://www.pucesi.edu.ec/webs2/tourvirtual/"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-md bg-[#0033A0] px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-[#00277a]"
            >
              <MapPin size={17} />
              Tour virtual oficial
            </a>
            <a
              href="https://www.pucesi.edu.ec/webs2/index.php/horarios-estudiantiles-2026-01/"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-md border border-[#0033A0] px-4 py-2 text-sm font-semibold text-[#0033A0] transition-colors hover:bg-[#e6f7fd]"
            >
              <BookOpen size={17} />
              Horarios 2026-01
            </a>
          </div>
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

          <div className="relative hidden min-h-[640px] overflow-hidden rounded-md border border-slate-200 bg-white shadow-sm md:block">
            <div className="absolute left-0 right-0 top-0 z-30 bg-[#00AEEF] px-5 py-3 text-center text-sm font-bold text-white">
              El campus crece y se renueva pensando en ti
            </div>
            <div className="absolute inset-6 rounded-md border-2 border-dashed border-slate-300" />
            <div className="absolute left-[7%] top-[62%] h-8 w-[78%] -translate-y-1/2 rounded-full bg-slate-200" />
            <div className="absolute left-[55%] top-[20%] h-[58%] w-8 -translate-x-1/2 rounded-full bg-slate-200" />
            <div className="absolute bottom-6 left-8 z-20 rounded-md bg-white px-3 py-2 text-xs font-semibold text-slate-700 shadow-sm">
              Acceso principal
            </div>
            <div className="absolute bottom-12 left-[23%] z-20 rounded-full bg-violet-100 px-3 py-2 text-xs font-bold text-violet-800 shadow-sm">Ingreso 4</div>
            <div className="absolute bottom-10 left-[43%] z-20 rounded-full bg-cyan-100 px-3 py-2 text-xs font-bold text-cyan-800 shadow-sm">Ingreso 3</div>
            <div className="absolute right-[7%] top-[32%] z-20 rounded-full bg-orange-100 px-3 py-2 text-xs font-bold text-orange-800 shadow-sm">Ingreso 5</div>
            <div className="absolute bottom-4 left-[4%] z-20 rounded-full bg-green-100 px-3 py-2 text-xs font-bold text-green-800 shadow-sm">Ingreso ECAA</div>

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
              Sigue las rutas señalizadas: los accesos y ubicaciones han cambiado temporalmente por obras en ejecución.
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
              Para aulas exactas usa el código de tu horario. El chatbot responderá con estas ubicaciones del campus y, si hay cambios operativos, sugerirá confirmar en garita.
            </p>

            <div className="mt-5 border-t border-slate-100 pt-5">
              <h3 className="text-lg font-bold text-[#1f2937]">Aulas por edificio</h3>
              <div className="mt-4 space-y-4">
                {roomGuide.map((group) => (
                  <div key={group.title}>
                    <p className="text-sm font-bold text-slate-800">{group.title}</p>
                    <ul className="mt-1 space-y-1 text-sm text-slate-600">
                      {group.lines.map((line) => (
                        <li key={line}>{line}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CampusMapSection;
