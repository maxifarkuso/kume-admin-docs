import { useState } from 'react';
import './HorariosLaboralesImportarDesdeClock.css';

const clock = [
  {id:'a', code:'M01', name:'Turno mañana', type:'Fijo', status:'seen'},
  {id:'b', code:'', name:'Turno tarde revisado', type:'Fijo', status:'review'},
  {id:'c', code:'', name:'Turno de talleres', type:'Fijo', status:'new'},
  {id:'d', code:'L01', name:'Día libre', type:'Libre', status:'new'},
];
const initial = [
  {id:'local-a', label:'Turno mañana', code:'M01', external:'Turno mañana', type:'Fijo'},
  {id:'local-b', label:'Turno tarde', code:'', external:'Turno tarde', type:'Fijo'},
];
const notes = {seen:'Coincidencia exacta', review:'Elegí si corresponde a una referencia local.', new:'Sin coincidencia exacta'};
const statuses = {seen:'Ya observada', review:'Requiere revisión', new:'Nueva referencia'};

export function HorariosLaboralesImportarDesdeClock() {
  const [catalog, setCatalog] = useState(initial);
  const [preview, setPreview] = useState(false);
  const [decisions, setDecisions] = useState<Record<string,string>>({});
  const [result, setResult] = useState('');
  const [last, setLast] = useState('23 nov 2026, 16:30');
  const rows = clock.map(row => ({
    ...row,
    status: catalog.some(local => local.code === row.code && local.external === row.name && local.type === row.type)
      ? 'seen' as const : row.status === 'review' ? 'review' as const : 'new' as const,
  }));
  const actionable = rows.filter(row => row.status !== 'seen');
  const selected = actionable.filter(row => decisions[row.id]);
  const destinations = selected.map(row => decisions[row.id]).filter(action => action !== 'create');
  const conflicting = new Set(destinations).size !== destinations.length;
  const count = rows.length - actionable.length;
  const number = (n: number, one: string, many: string) => n + ' ' + (n === 1 ? one : many);
  function openPreview() {
    setDecisions({});
    setResult('');
    setPreview(true);
  }
  function confirm() {
    if (!selected.length || conflicting) return;
    const updated = catalog.map(local => {
      const row = selected.find(observation => decisions[observation.id] === local.id);
      return row ? {...local, code:row.code, external:row.name, type:row.type} : local;
    });
    const added = selected.filter(row => decisions[row.id] === 'create');
    setCatalog([...updated, ...added.map(row => ({
      id:'local-' + row.id, label:row.name, code:row.code, external:row.name, type:row.type,
    }))]);
    setLast('24 nov 2026, 09:15');
    setResult([
      number(added.length,'alta','altas'),
      number(selected.length - added.length,'actualización','actualizaciones'),
      number(count,'repetida','repetidas'),
      number(actionable.length - selected.length,'pendiente','pendientes'),
    ].join(' · '));
    setPreview(false);
  }
  return (
    <div className="cu1">
      <aside className="cu1-sidebar" aria-label="Navegación de referencia">
        <div className="cu1-brand">KUME <span>Admin</span></div>
        <div className="cu1-nav-label">Trabajo diario</div>
        <div className="cu1-nav-item">Gastos</div><div className="cu1-nav-item">Personal</div>
        <div className="cu1-nav-label">Administración</div>
        <div className="cu1-nav-item">Rubros</div><div className="cu1-nav-item">Cursos</div><div className="cu1-nav-item">Talleres</div>
        <div className="cu1-nav-item current" aria-current="page">Horarios laborales</div>
      </aside>
      <main>
        <div className="cu1-top"><span>Administración</span><span className="cu1-demo">Prototipo · Datos ficticios</span></div>
        <div className="cu1-heading">
          <div><h1>Horarios laborales</h1><p>Catálogo de referencias de Clock en KUME.</p></div>
          {!preview && <button className="cu1-primary" onClick={openPreview}>↓ Importar desde Clock</button>}
        </div>
        {preview ? (
          <section className="cu1-card" aria-labelledby="cu1-preview">
            <header><h2 id="cu1-preview">Vista previa de importación</h2><p>Consulta de Clock · 24 nov 2026, 09:15</p></header>
            <div className="cu1-notice">Revisá qué referencias querés guardar. La importación conserva los horarios de las maestras.</div>
            <div className="cu1-summary"><strong>{rows.length} de Clock</strong><span>{count} ya observadas</span><span>{actionable.length} por revisar</span></div>
            <div className="cu1-table"><table>
              <thead><tr><th>Código Clock</th><th>Nombre y tipo en Clock</th><th>Estado</th><th>Acción en KUME</th></tr></thead>
              <tbody>{rows.map(row => {
                const destination = catalog.find(local => local.id === decisions[row.id]);
                return <tr key={row.id}>
                  <td>{row.code || <span className="cu1-muted">Sin código</span>}</td>
                  <td><strong>{row.name}</strong><small>{row.type}</small></td>
                  <td><span className={'cu1-pill ' + row.status}>{statuses[row.status]}</span><small>{notes[row.status]}</small></td>
                  <td>{row.status === 'seen' ? <span className="cu1-muted">Sin cambios</span> : <>
                    <select aria-label={'Acción para ' + row.name} value={decisions[row.id] || ''} onChange={event => setDecisions({...decisions,[row.id]:event.target.value})}>
                      <option value="">Dejar pendiente</option>
                      <option value="create">Crear referencia</option>
                      <optgroup label="Vincular a referencia existente">
                        {catalog.filter(local => !rows.some(other => other.status === 'seen' && other.code === local.code && other.name === local.external && other.type === local.type)).map(local =>
                          <option value={local.id} key={local.id}>Vincular a {local.label}</option>)}
                      </optgroup>
                    </select>
                    {destination && <small>Clock antes: {destination.external}<br/>Clock después: {row.name}<br/>Etiqueta KUME: {destination.label}</small>}
                  </>}</td>
                </tr>;
              })}</tbody>
            </table></div>
            <footer>
              <div className="cu1-actions"><button className="cu1-primary" disabled={!selected.length || conflicting} onClick={confirm}>Confirmar importación</button><button onClick={() => setPreview(false)}>Cancelar</button></div>
              <p role="status">{conflicting ? 'Elegí un destino distinto para cada turno.' : number(selected.length,'decisión seleccionada','decisiones seleccionadas')}</p>
            </footer>
          </section>
        ) : <>
          {result && <div className="cu1-success" role="status"><strong>Importación confirmada</strong><span>{result}</span></div>}
          <section className="cu1-card" aria-labelledby="cu1-catalog">
            <header><h2 id="cu1-catalog">Catálogo local</h2><p>Última importación confirmada · {last}</p></header>
            <div className="cu1-table"><table>
              <thead><tr><th>Referencia KUME</th><th>Código Clock</th><th>Nombre en Clock</th><th>Tipo</th></tr></thead>
              <tbody>{catalog.map(local => <tr key={local.id}><td><strong>{local.label}</strong></td><td>{local.code || <span className="cu1-muted">Sin código</span>}</td><td>{local.external}</td><td>{local.type}</td></tr>)}</tbody>
            </table></div>
            <div className="cu1-count">{number(catalog.length,'referencia','referencias')}</div>
          </section>
        </>}
      </main>
    </div>
  );
}
