export type Punch = { code: number; time: string; created: string };
export type Slot = { source: string; time: string };
export type Audit = { at: string; author: string; reason: string; before: Slot[]; after: Slot[] };
export type AttendanceDay = { date: string; kind: 'scheduled' | 'off' | 'unassigned'; original: Punch[]; slots: Slot[]; reviewedExtras: boolean; history: Audit[] };
export const DEMO_NOW = '2026-11-16T10:30:00';
export const SLOT_LABELS = ['Entrada', 'Salida a almuerzo', 'Regreso', 'Salida final'];
export const EXPECTED = ['08:00', '12:00', '13:00', '17:00'];
export function minutes(time: string): number { const [hours = 0, mins = 0] = time.split(':').map(Number); return hours * 60 + mins; }
export function formatHours(total: number): string { return `${Math.floor(total / 60)} h ${String(total % 60).padStart(2, '0')} min`; }
export function confirmedMinutes(day: AttendanceDay): number {
  if (day.kind !== 'scheduled') return 0;
  return [0, 2].reduce((sum, index) => { const start = day.slots[index]?.time; const end = day.slots[index + 1]?.time; return sum + (start && end && minutes(end) > minutes(start) ? minutes(end) - minutes(start) : 0); }, 0);
}
export function extraPunches(day: AttendanceDay): Punch[] { return day.original.filter(punch => !day.slots.some(slot => slot.source === String(punch.code))); }
export function dayStatus(day: AttendanceDay, margin: number): string {
  if (day.kind === 'off') return 'Sin jornada prevista';
  if (day.kind === 'unassigned') return 'Sin horario de referencia';
  if (day.date > '2026-11-16') return 'Pendiente';
  const missing = day.slots.flatMap((slot, index) => slot.time ? [] : [index]);
  if (!missing.length && (!extraPunches(day).length || day.reviewedExtras)) return day.history.length ? 'Ajustado' : 'Completo';
  if (day.date === '2026-11-16' && !missing.some(index => minutes(EXPECTED[index] ?? '00:00') + margin < 630)) return 'En curso';
  return 'Por revisar';
}
export function validateSlots(slots: Slot[]): string {
  const used = slots.filter(slot => slot.source && slot.source !== 'manual').map(slot => slot.source);
  if (new Set(used).size !== used.length) return 'Una misma marca no puede usarse en dos posiciones.';
  if (slots.some(slot => slot.source && !slot.time)) return 'Completá la hora de las marcas manuales.';
  const entered = slots.filter(slot => slot.time).map(slot => minutes(slot.time));
  if (entered.some((value, index) => index > 0 && value <= (entered[index - 1] ?? 0))) return 'Las horas deben seguir el orden de la jornada, sin superponerse.';
  return '';
}
export function dateLabel(date: string): string { return new Intl.DateTimeFormat('es-UY', { weekday: 'short', day: '2-digit', month: 'short', timeZone: 'America/Montevideo' }).format(new Date(`${date}T12:00:00-03:00`)); }
export function demoDays(month: string): AttendanceDay[] {
  const [year = 2026, monthNumber = 11] = month.split('-').map(Number);
  const lastDay = new Date(Date.UTC(year, monthNumber, 0)).getUTCDate();
  return Array.from({ length: lastDay }, (_, index) => {
    const day = index + 1; const date = `${month}-${String(day).padStart(2, '0')}`;
    const weekday = new Date(`${date}T12:00:00Z`).getUTCDay();
    const kind = weekday === 0 || weekday === 6 ? 'off' : month === '2026-11' && day === 10 ? 'unassigned' : 'scheduled';
    const times = month !== '2026-11' || date > '2026-11-16' || kind === 'off' ? [] : day === 3 ? ['12:00', '13:00', '17:00'] : day === 5 ? ['08:00', '08:02', '12:00', '13:00', '17:00'] : day === 12 ? [] : day === 10 ? ['12:52'] : day === 16 ? ['08:00'] : ['08:00', '12:00', '13:00', '17:00'];
    const original = times.map((time, punchIndex) => ({ code: day * 100 + punchIndex, time, created: `${time}:49` }));
    const slots = EXPECTED.map((time, slotIndex) => { const punch = kind === 'scheduled' && !(month === '2026-11' && day === 5 && slotIndex === 0) ? original.find(mark => mark.time === time) : undefined; return { source: punch ? String(punch.code) : '', time: punch?.time ?? '' }; });
    return { date, kind, original, slots, reviewedExtras: false, history: [] };
  });
}
