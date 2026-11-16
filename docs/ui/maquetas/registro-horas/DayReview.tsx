import { useEffect, useRef, useState } from 'react';
import type { AttendanceDay, Slot } from './attendance';
import { dateLabel, EXPECTED, SLOT_LABELS, validateSlots } from './attendance';
import { HoursIcon } from './HoursIcon';
export function DayReview({ day, onClose, onSave }: { day: AttendanceDay; onClose: () => void; onSave: (slots: Slot[], reason: string, reviewedExtras: boolean) => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [slots, setSlots] = useState(day.slots.map(slot => ({ ...slot })));
  const [reason, setReason] = useState('');
  const [extrasReviewed, setExtrasReviewed] = useState(day.reviewedExtras);
  const [error, setError] = useState('');
  const [discard, setDiscard] = useState(false);
  const [tab, setTab] = useState('review');
  const errorRef = useRef<HTMLParagraphElement>(null);
  useEffect(() => { const origin = document.activeElement; dialog.current?.showModal(); return () => { if (origin instanceof HTMLElement) origin.focus(); }; }, []);
  const dirty = JSON.stringify(slots) !== JSON.stringify(day.slots) || reason !== '' || extrasReviewed !== day.reviewedExtras;
  const canEdit = day.kind === 'scheduled' && day.date <= '2026-11-16';
  const unused = day.original.filter(punch => !slots.some(slot => slot.source === String(punch.code)));
  function close() { if (dirty) setDiscard(true); else onClose(); }
  function selectSource(index: number, source: string) { setError(''); setSlots(current => current.map((slot, position) => position !== index ? slot : { source, time: source === 'manual' ? '' : day.original.find(punch => String(punch.code) === source)?.time ?? '' })); }
  function save() { const problem = validateSlots(slots); if (problem) { setError(problem); setTimeout(() => errorRef.current?.focus(), 0); return; } onSave(slots, reason, extrasReviewed); }
  return <dialog ref={dialog} className="hr-drawer" aria-labelledby="day-review-title" onCancel={event => { event.preventDefault(); close(); }}>
    <header className="hr-drawer-header"><div><span className="hr-eyebrow">REGISTRO DIARIO</span><h2 id="day-review-title">{dateLabel(day.date)}</h2><p>Juanita González · Maestra</p></div><button aria-label="Cerrar revisión" className="hr-icon-button" onClick={close}><HoursIcon name="close"/></button></header>
    <div className="hr-drawer-tabs"><button className={tab === 'review' ? 'active' : ''} onClick={() => setTab('review')}>Revisar marcas</button><button className={tab === 'history' ? 'active' : ''} onClick={() => setTab('history')}>Historial ({day.history.length})</button></div>
    <div className="hr-drawer-content">{tab === 'history' ? <section><h3>Historial de ajustes</h3>{!day.history.length ? <p className="hr-muted">Todavía no se hicieron ajustes en este día.</p> : day.history.map((audit, index) => <article className="hr-audit" key={audit.at + index}><strong>{audit.author}</strong><small>{audit.at}</small><p>{audit.reason || 'Sin motivo indicado'}</p><small>Antes: {audit.before.map(slot => slot.time || '—').join(' · ')}</small><small>Después: {audit.after.map(slot => slot.time || '—').join(' · ')}</small></article>)}</section> : <>
      <section className="hr-schedule"><HoursIcon name="calendar"/><div><strong>{day.kind === 'scheduled' ? 'Jornada prevista · 8 horas' : day.kind === 'off' ? 'Sin jornada prevista' : 'Sin horario de referencia'}</strong><p>{day.kind === 'scheduled' ? '08:00–12:00 · Pausa 12:00–13:00 · 13:00–17:00' : 'No se interpretan las marcas automáticamente.'}</p></div></section>
      {day.date === '2026-11-03' && !day.history.length && <div className="hr-alert"><HoursIcon name="alert"/><div><strong>Posible salida a las 12:00</strong><p>Coincide con el fin del bloque de mañana. Falta confirmar la entrada; no se completará con las 08:00.</p></div></div>}
      <section><div className="hr-section-title"><h3>Marcas originales de Clock</h3><span>{day.original.length} marcas</span></div><p className="hr-small hr-muted">Se conservan sin modificaciones.</p><div className="hr-punches">{day.original.map(punch => <div key={punch.code}><strong>{punch.time}</strong><small>#{punch.code} · Registrada {punch.created}</small></div>)}</div>{!day.original.length && <p className="hr-small hr-muted">No se recibieron marcas para este día.</p>}</section>
      {canEdit ? <section><h3>Organizar la jornada</h3><p className="hr-small hr-muted">Asigná una marca original o ingresá una hora manual.</p><div className="hr-slot-edit">{slots.map((slot, index) => <div key={index}><label htmlFor={`source-${index}`}>{SLOT_LABELS[index]} <small>Prevista {EXPECTED[index]}</small></label><div className="hr-slot-input"><select id={`source-${index}`} value={slot.source} onChange={event => selectSource(index, event.target.value)}><option value="">Sin marca</option>{day.original.map(punch => <option key={punch.code} value={String(punch.code)}>{punch.time} · Clock #{punch.code}</option>)}<option value="manual">Agregar hora manual</option></select>{slot.source === 'manual' && <input aria-label={`Hora manual de ${SLOT_LABELS[index]}`} type="time" value={slot.time} onChange={event => setSlots(current => current.map((item, position) => position === index ? { ...item, time: event.target.value } : item))}/>}</div></div>)}</div>
      {unused.length > 0 && <div className="hr-unused"><strong>Marcas sin asignar: {unused.map(punch => punch.time).join(' · ')}</strong><label><input type="checkbox" checked={extrasReviewed} onChange={event => setExtrasReviewed(event.target.checked)}/> Revisé estas marcas y no corresponden a otro bloque</label><p>Se conservarán en el registro original.</p></div>}
      <label className="hr-reason" htmlFor="adjustment-reason">Motivo <span>Opcional</span></label><textarea id="adjustment-reason" rows={2} placeholder="Ej.: la maestra olvidó marcar la entrada" value={reason} onChange={event => setReason(event.target.value)}/><p className="hr-small hr-muted">El ajuste se guarda solo en KUME. No modifica Clock.</p>
      {error && <p ref={errorRef} tabIndex={-1} role="alert" className="hr-form-error">{error}</p>}</section> : <div className="hr-info">{day.date > '2026-11-16' ? 'La jornada aún no comenzó.' : 'Sin bloques previstos no se asignan horas. Revisá el horario en las asignaciones de la ficha.'}</div>}
    </>}</div>
    <footer className="hr-drawer-footer">{discard ? <><p>¿Descartar los cambios sin guardar?</p><div><button onClick={() => setDiscard(false)}>Seguir editando</button><button className="hr-primary" onClick={onClose}>Descartar cambios</button></div></> : <><p><HoursIcon name="people"/> Solo administración puede realizar ajustes</p><div>{canEdit && <button className="hr-primary" onClick={save} disabled={!dirty}><HoursIcon name="check"/> Guardar ajuste</button>}<button onClick={close}>{dirty ? 'Cancelar' : 'Cerrar'}</button></div></>}</footer>
  </dialog>;
}
