import React, { useEffect, useMemo, useState } from 'react';
import { useTelemetryStore } from '../store/useTelemetryStore';
import {
  Activity,
  AlertTriangle,
  Archive,
  BarChart3,
  CheckCircle,
  Clock,
  CloudSun,
  Cpu,
  Database,
  Gauge,
  GitBranch,
  History,
  Map,
  Plane,
  PlaneLanding,
  PlaneTakeoff,
  Play,
  Radar,
  Radio,
  Route,
  Save,
  ShieldAlert,
  Sparkles,
  Target,
  TowerControl,
  TrendingDown,
  Zap,
} from 'lucide-react';
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const RUNWAYS = ['AUTO', '27L', '27R', '09L', '09R'];
const AIRLINES = ['Air India', 'IndiGo', 'Vistara', 'SpiceJet', 'Akasa Air', 'American', 'United', 'Delta', 'Medevac'];
const AIRPORTS = ['DEL', 'BOM', 'BLR', 'HYD', 'MAA', 'CCU', 'GOI', 'AMD', 'JFK', 'LAX'];
const WAKE = ['Light', 'Medium', 'Heavy'];
const SCHEDULE_TIMES = [120, 180, 300, 450, 600, 900, 1200, 1800];
const RUNWAY_USE_TIMES = [35, 45, 50, 60, 75, 90];
const VISIBILITY_OPTIONS = [3, 5, 8, 10, 12, 15];
const ALGORITHMS = [
  ['FCFS', 'FCFS', 'FCFS queue with timestamp ordering'],
  ['PRIORITY', 'Priority Scheduling', 'Priority queue by urgency, emergency, passengers, cargo'],
  ['PREEMPTIVE_EMERGENCY', 'Preemptive Emergency', 'Emergency observer overrides active queue'],
  ['GREEDY_MIN_DELAY', 'Greedy Min Delay', 'Heap-based min-delay optimization'],
  ['HYBRID_ADAPTIVE', 'Hybrid Adaptive AI', 'ML-guided hybrid with graph taxi routing'],
];

const blankFlight = {
  id: '',
  airline: 'Air India',
  mode: 'LANDING',
  type: 'A320',
  wake: 'Medium',
  origin: 'DEL',
  dest: 'BOM',
  eta: '',
  taxiTime: 0,
  runwayOccEst: 45,
  fuelUrgency: 5,
  passengerPriority: 'Normal',
  cargoPriority: 'Routine',
  medicalDistress: false,
  technicalDistress: false,
  fuelEmergency: false,
  minimumSeparation: 90,
  requestedRunway: 'AUTO',
  autoRunway: true,
};

const card = 'glass-card p-6';
const input = 'w-full rounded-2xl border border-white/70 bg-white/70 px-4 py-3 text-sm font-black text-slate-800 outline-none transition focus:bg-white focus:ring-4 focus:ring-sky-100/70';
const label = 'mb-2 block text-[10px] font-black uppercase tracking-[0.22em] text-slate-400';

const SectionTitle = ({ icon: Icon, eyebrow, title, accent = 'text-sky-600' }) => (
  <div className="mb-5">
    <div className={`mb-1 flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.26em] ${accent}`}>
      <Icon className="h-4 w-4" />
      {eyebrow}
    </div>
    <h2 className="text-xl font-black tracking-tight text-slate-950">{title}</h2>
  </div>
);

const Metric = ({ icon: Icon, label: title, value, tone = 'text-sky-600' }) => (
  <div className="rounded-3xl border border-white/70 bg-white/55 p-4 shadow-sm transition hover:-translate-y-1 hover:bg-white/75 hover:shadow-xl">
    <Icon className={`mb-3 h-6 w-6 ${tone}`} />
    <div className="text-[9px] font-black uppercase tracking-[0.22em] text-slate-400">{title}</div>
    <div className="mt-1 text-2xl font-black tracking-tight text-slate-950">{value}</div>
  </div>
);

const AeroSlotNavbar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    ['FLIGHT_INTAKE', 'Flight Intake', Plane],
    ['SIMULATION_CONTROL', 'Simulation Control', Cpu],
    ['RUNWAY_STATUS', 'Runway Status', Radar],
  ];
  return (
    <nav className="sticky top-4 z-30 mx-auto mb-8 max-w-7xl rounded-[2rem] border border-white/70 bg-white/55 px-5 py-4 shadow-2xl shadow-sky-900/10 backdrop-blur-3xl">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-3xl bg-sky-600 text-white shadow-xl shadow-sky-500/30">
            <Plane className="h-8 w-8 animate-glide" />
          </div>
          <div>
            <h1 className="text-2xl font-black tracking-tight text-slate-950">AeroSlot Scheduler</h1>
            <p className="text-xs font-bold text-slate-500">Smart runway allocation for safe and efficient skies</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {tabs.map(([id, title, Icon]) => (
            <button key={id} onClick={() => setActiveTab(id)} className={`flex items-center gap-2 rounded-2xl px-4 py-3 text-xs font-black uppercase tracking-wider transition ${activeTab === id ? 'bg-white text-sky-700 shadow-lg ring-1 ring-sky-100' : 'bg-white/35 text-slate-500 hover:bg-white/70 hover:text-slate-800'}`}>
              <Icon className="h-4 w-4" />
              {title}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};

const Field = ({ title, children }) => <div><label className={label}>{title}</label>{children}</div>;
const Check = ({ checked, onChange, title, tone = 'text-slate-700' }) => (
  <label className={`flex items-center gap-3 rounded-2xl bg-white/50 px-4 py-3 text-xs font-black uppercase tracking-wider ${tone}`}>
    <input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} className="h-5 w-5 accent-sky-500" />
    {title}
  </label>
);

const FlightIntake = () => {
  const { addFlight, predictionResult, loadDemoTraffic, batchLoadDataset, env, setEnv } = useTelemetryStore();
  const [flight, setFlight] = useState(blankFlight);
  const [lastAdded, setLastAdded] = useState(null);
  const setField = (key, value) => setFlight((prev) => ({ ...prev, [key]: value }));

  const handleAdd = async () => {
    if (!flight.id || !flight.eta) return alert('Enter Flight Number and Schedule Time first.');
    const saved = await addFlight({ ...flight, requestedRunway: flight.autoRunway ? 'AUTO' : flight.requestedRunway });
    setLastAdded(saved);
    setFlight(blankFlight);
  };

  return (
    <>
      <section className={`${card} lg:col-span-12`}>
        <SectionTitle icon={PlaneLanding} eyebrow="Flight Intake" title="Add flight for runway scheduling" />
        <div className="grid gap-4 md:grid-cols-4">
          <Field title="Flight Number"><input className={input} value={flight.id} onChange={(e) => setField('id', e.target.value.toUpperCase())} placeholder="AA772" /></Field>
          <Field title="Airline"><select className={input} value={flight.airline} onChange={(e) => setField('airline', e.target.value)}>{AIRLINES.map((a) => <option key={a}>{a}</option>)}</select></Field>
          <Field title="Operation"><select className={input} value={flight.mode} onChange={(e) => setField('mode', e.target.value)}><option value="LANDING">Landing</option><option value="TAKEOFF">Takeoff</option></select></Field>
          <Field title="Wake Size"><select className={input} value={flight.wake} onChange={(e) => setField('wake', e.target.value)}>{WAKE.map((w) => <option key={w}>{w}</option>)}</select></Field>
          <Field title="From"><select className={input} value={flight.origin} onChange={(e) => setField('origin', e.target.value)}>{AIRPORTS.map((a) => <option key={a}>{a}</option>)}</select></Field>
          <Field title="To"><select className={input} value={flight.dest} onChange={(e) => setField('dest', e.target.value)}>{AIRPORTS.map((a) => <option key={a}>{a}</option>)}</select></Field>
          <Field title="Schedule Time (sec)"><select className={input} value={flight.eta} onChange={(e) => setField('eta', e.target.value)}><option value="">Select time</option>{SCHEDULE_TIMES.map((t) => <option key={t} value={t}>{t} sec</option>)}</select></Field>
          <Field title="Runway Use Time (sec)"><select className={input} value={flight.runwayOccEst} onChange={(e) => setField('runwayOccEst', Number(e.target.value))}>{RUNWAY_USE_TIMES.map((t) => <option key={t} value={t}>{t} sec</option>)}</select></Field>
          <Field title="Flight Priority"><select className={input} value={flight.passengerPriority} onChange={(e) => setField('passengerPriority', e.target.value)}>{['Normal', 'VIP', 'Medical', 'High Density'].map((p) => <option key={p}>{p}</option>)}</select></Field>
          <Field title="Cargo Need"><select className={input} value={flight.cargoPriority} onChange={(e) => setField('cargoPriority', e.target.value)}>{['Routine', 'Perishable', 'Medical', 'Military'].map((c) => <option key={c}>{c}</option>)}</select></Field>
        </div>
        <div className="mt-5 grid gap-4 rounded-3xl border border-white/70 bg-white/35 p-5 md:grid-cols-4">
          <Field title="Fuel Urgency"><input className="w-full accent-amber-500" type="range" min="1" max="10" value={flight.fuelUrgency} onChange={(e) => setField('fuelUrgency', Number(e.target.value))} /><div className="text-right text-xs font-black text-amber-600">{flight.fuelUrgency}/10</div></Field>
          <Field title="Safety Gap"><input className={input} type="number" value={flight.minimumSeparation} onChange={(e) => setField('minimumSeparation', Number(e.target.value))} /></Field>
          <Field title="Preferred Runway"><select disabled={flight.autoRunway} className={input} value={flight.requestedRunway} onChange={(e) => setField('requestedRunway', e.target.value)}>{RUNWAYS.map((r) => <option key={r}>{r}</option>)}</select></Field>
          <Field title="Runway Condition"><select className={input} value={env.runwayCondition} onChange={(e) => setEnv({ runwayCondition: e.target.value })}>{['DRY', 'WET', 'CONTAMINATED'].map((r) => <option key={r}>{r}</option>)}</select></Field>
          <Check checked={flight.medicalDistress} onChange={(v) => setField('medicalDistress', v)} title="Medical distress" tone="text-rose-600" />
          <Check checked={flight.technicalDistress} onChange={(v) => setField('technicalDistress', v)} title="Technical distress" tone="text-amber-700" />
          <Check checked={flight.autoRunway} onChange={(v) => setField('autoRunway', v)} title="Auto runway assignment" tone="text-indigo-700" />
          <Field title="Visibility (km)"><select className={input} value={env.visibility} onChange={(e) => setEnv({ visibility: Number(e.target.value) })}>{VISIBILITY_OPTIONS.map((v) => <option key={v} value={v}>{v} km</option>)}</select></Field>
          <Field title="Storm Severity"><input className="w-full accent-sky-600" type="range" min="0" max="10" value={env.storm} onChange={(e) => setEnv({ storm: Number(e.target.value), stormSeverity: Number(e.target.value) })} /><div className="text-right text-xs font-black text-sky-700">{env.storm}/10</div></Field>
          <Field title="Traffic Level"><select className={input} value={env.congestion} onChange={(e) => setEnv({ congestion: e.target.value })}>{['LOW', 'MEDIUM', 'HIGH'].map((c) => <option key={c}>{c}</option>)}</select></Field>
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          <button onClick={handleAdd} className="flex items-center gap-2 rounded-2xl bg-sky-600 px-5 py-3 text-sm font-black text-white shadow-lg shadow-sky-500/20 transition hover:-translate-y-1"><Save className="h-5 w-5" />Add Flight</button>
          <button onClick={batchLoadDataset} className="flex items-center gap-2 rounded-2xl bg-white/70 px-5 py-3 text-sm font-black text-slate-700 transition hover:-translate-y-1"><Database className="h-5 w-5" />Batch Load Dataset</button>
          <button onClick={loadDemoTraffic} className="flex items-center gap-2 rounded-2xl border border-emerald-100 bg-emerald-50 px-5 py-3 text-sm font-black text-emerald-700 transition hover:-translate-y-1"><Sparkles className="h-5 w-5" />Load Demo Dataset</button>
        </div>
      </section>
      {lastAdded && predictionResult && <section className="grid gap-4 lg:col-span-12 md:grid-cols-4">
        <Metric icon={Clock} label="Estimated Delay" value={`${predictionResult.delay}s`} tone="text-amber-600" />
        <Metric icon={ShieldAlert} label="Conflict Risk" value={`${Math.round(predictionResult.risk * 100)}%`} tone="text-rose-600" />
        <Metric icon={Zap} label="Priority Score" value={predictionResult.score} tone="text-emerald-600" />
        <Metric icon={Target} label="Recommended Runway" value={predictionResult.recommendedRunway || 'AUTO'} />
      </section>}
      <QueueMonitor />
      <FlightHistoryMini />
    </>
  );
};

const QueueMonitor = () => {
  const { flights } = useTelemetryStore();
  const col = (title, Icon, list, tone) => (
    <div className="rounded-[2rem] border border-white/70 bg-white/45 p-5">
      <div className={`mb-4 flex items-center gap-2 text-xs font-black uppercase tracking-[0.22em] ${tone}`}><Icon className="h-4 w-4" />{title}</div>
      <div className="max-h-80 space-y-3 overflow-y-auto pr-1">
        {list.length ? list.map((f, i) => <div key={`${f.id}-${i}`} className="animate-[fadeIn_0.35s_ease] rounded-2xl bg-white/70 p-3 shadow-sm">
          <div className="flex items-center justify-between"><span className="text-sm font-black text-slate-950">{f.id}</span><span className="text-[9px] font-black uppercase text-sky-700">{f.status}</span></div>
          <div className="mt-1 flex justify-between text-[10px] font-bold text-slate-400"><span>{f.airline || f.type}</span><span>T-{f.eta || f.slotTime || 0}s</span></div>
        </div>) : <div className="rounded-2xl border border-dashed border-slate-200 bg-white/35 p-5 text-center text-sm font-bold text-slate-400">Queue empty</div>}
      </div>
    </div>
  );
  return <section className={`${card} lg:col-span-7`}><SectionTitle icon={Target} eyebrow="Live Queue Monitor" title="Landing and takeoff queue" accent="text-emerald-600" /><div className="grid gap-4 md:grid-cols-2">{col('Landing Queue', PlaneLanding, flights.filter((f) => f.mode === 'LANDING'), 'text-rose-600')}{col('Takeoff Queue', PlaneTakeoff, flights.filter((f) => f.mode === 'TAKEOFF'), 'text-sky-600')}</div></section>;
};

const FlightHistoryMini = () => {
  const { flights } = useTelemetryStore();
  return <section className={`${card} lg:col-span-5`}><SectionTitle icon={History} eyebrow="Flight History" title="Recently added flights" accent="text-slate-600" /><div className="overflow-hidden rounded-3xl border border-white/70 bg-white/45"><table className="w-full text-left text-xs"><thead className="bg-white/65 text-[10px] font-black uppercase tracking-widest text-slate-400"><tr><th className="p-4">Flight</th><th className="p-4">Route</th><th className="p-4">Status</th></tr></thead><tbody className="divide-y divide-white/60">{flights.slice(0, 8).map((f, i) => <tr key={`${f.id}-${i}`}><td className="p-4 font-black">{f.id}</td><td className="p-4 font-bold text-slate-500">{f.origin || '--'} - {f.dest || '--'}</td><td className="p-4 font-bold text-sky-700">{f.status}</td></tr>)}{!flights.length && <tr><td colSpan="3" className="p-8 text-center font-bold text-slate-400">No flights submitted</td></tr>}</tbody></table></div></section>;
};

const ScheduledFlightLogs = () => {
  const { scheduledResults, eventLog } = useTelemetryStore();
  const latestScheduleEvents = eventLog.filter((e) => ['SCHEDULER_RUN', 'RUNWAY_ASSIGNED', 'RUNWAY_OPTIMIZED', 'EMERGENCY_OVERRIDE', 'STORM_INJECTED', 'ALGORITHM_SWITCHED'].includes(e.type)).slice(0, 8);
  return <section className={`${card} lg:col-span-12`}><SectionTitle icon={History} eyebrow="Scheduled Flight Logs" title="Latest runway scheduling output" accent="text-emerald-600" /><div className="grid gap-5 lg:grid-cols-2"><div className="overflow-hidden rounded-3xl border border-white/70 bg-white/45"><table className="w-full text-left text-xs"><thead className="bg-white/65 text-[10px] font-black uppercase tracking-widest text-slate-400"><tr><th className="p-4">Flight</th><th className="p-4">Runway</th><th className="p-4">Slot</th><th className="p-4">Delay</th></tr></thead><tbody className="divide-y divide-white/60">{scheduledResults.length ? scheduledResults.slice(0, 10).map((f, i) => <tr key={`${f.id}-${i}`}><td className="p-4 font-black">{f.id}</td><td className="p-4 font-bold text-sky-700">{f.assignedRunway || '--'}</td><td className="p-4 font-mono font-black">T-{f.slotTime ?? '--'}s</td><td className="p-4 font-bold text-amber-700">{f.delay ?? 0}s</td></tr>) : <tr><td colSpan="4" className="p-8 text-center font-bold text-slate-400">Run scheduler to generate scheduled flight logs</td></tr>}</tbody></table></div><div className="max-h-80 space-y-3 overflow-y-auto pr-1">{latestScheduleEvents.length ? latestScheduleEvents.map((e, i) => <div key={i} className="rounded-3xl border border-white/70 bg-white/55 p-4"><div className="font-mono text-[10px] font-black text-slate-400">{e.time} - {e.type}</div><div className="mt-1 text-sm font-bold text-slate-700">{e.msg}</div></div>) : <div className="rounded-3xl border border-dashed border-slate-200 bg-white/35 p-10 text-center font-bold text-slate-400">No scheduling events yet</div>}</div></div></section>;
};

const AlgorithmSwitchVisual = () => {
  const { algorithm, algorithmSwitches } = useTelemetryStore();
  const activeAlgorithm = algorithm === 'AUTO' ? 'FCFS' : algorithm;
  const activeIndex = Math.max(0, ALGORITHMS.findIndex(([id]) => id === activeAlgorithm));
  const latest = algorithmSwitches[0];
  return <section className={`${card} lg:col-span-12`}><SectionTitle icon={GitBranch} eyebrow="Algorithm Flow" title="Active scheduling algorithm" accent="text-indigo-600" /><div className="relative overflow-hidden rounded-3xl border border-white/70 bg-white/45 p-5"><div className="absolute left-8 right-8 top-[49px] h-1 rounded-full bg-white/80" /><div className="grid gap-3 md:grid-cols-5">{ALGORITHMS.map(([id, title], index) => <div key={id} className={`relative z-10 rounded-2xl border px-3 py-4 text-center transition duration-500 ${activeAlgorithm === id ? 'border-sky-300 bg-sky-50 text-sky-800 shadow-lg scale-[1.03]' : 'border-white/70 bg-white/55 text-slate-500'}`}><div className={`mx-auto mb-2 flex h-8 w-8 items-center justify-center rounded-full text-xs font-black ${index <= activeIndex ? 'bg-sky-600 text-white' : 'bg-slate-200 text-slate-500'}`}>{index + 1}</div><div className="text-xs font-black">{title}</div>{activeAlgorithm === id && <Plane className="algorithm-plane mx-auto mt-3 h-5 w-5 text-sky-600" />}</div>)}</div><div className="mt-4 rounded-2xl bg-slate-950 px-4 py-3 text-sm font-black text-white">{latest ? `Last switch: ${latest.from} -> ${latest.to} because ${latest.reason}` : `Current algorithm: ${activeAlgorithm}`}</div></div></section>;
};

const SimulationControl = () => {
  const { selectedAlgorithm, setAlgorithm, runSchedulerAPI, optimizeRunways, injectEmergency, injectStorm, isProcessing, liveBanner } = useTelemetryStore();
  return <>
    <section className={`${card} lg:col-span-12`}><SectionTitle icon={Cpu} eyebrow="Simulation Control" title="Scheduler control center" accent="text-indigo-600" />
      <div className="grid gap-3 md:grid-cols-5">{ALGORITHMS.map(([id, title, desc]) => <button key={id} onClick={() => setAlgorithm(id)} className={`rounded-3xl border p-4 text-left transition hover:-translate-y-1 hover:shadow-xl ${selectedAlgorithm === id ? 'border-sky-300 bg-sky-50 shadow-lg' : 'border-white/70 bg-white/50 hover:bg-white/80'}`}><div className="text-sm font-black text-slate-950">{title}</div><div className="mt-1 text-[11px] font-bold text-slate-500">{desc}</div></button>)}</div>
      <div className="mt-5 grid gap-3 md:grid-cols-4">
        <button onClick={runSchedulerAPI} disabled={isProcessing} className="rounded-3xl bg-slate-950 px-5 py-4 text-sm font-black text-white transition hover:-translate-y-1 disabled:bg-slate-400">{isProcessing ? 'Running...' : 'Run Scheduler'}</button>
        <button type="button" onClick={optimizeRunways} className="rounded-3xl bg-sky-50 px-5 py-4 text-sm font-black text-sky-700 transition hover:-translate-y-1 hover:bg-sky-100">Optimize Runways</button>
        <button type="button" onClick={injectEmergency} className="rounded-3xl bg-rose-50 px-5 py-4 text-sm font-black text-rose-700 transition hover:-translate-y-1 hover:bg-rose-100">Inject Emergency</button>
        <button type="button" onClick={injectStorm} className="rounded-3xl bg-amber-50 px-5 py-4 text-sm font-black text-amber-700 transition hover:-translate-y-1 hover:bg-amber-100">Inject Storm</button>
      </div>
    </section>
    <section className="lg:col-span-12 rounded-[2rem] bg-slate-950 px-6 py-5 text-base font-black text-white shadow-2xl shadow-slate-900/20"><Radio className="mr-3 inline h-5 w-5 text-sky-300" />{liveBanner || 'Scheduler ready: FCFS baseline active until simulation run'}</section>
    <AlgorithmSwitchVisual />
    <ScheduledFlightLogs />
  </>;
};

const RunwayBoard = () => {
  const { runways } = useTelemetryStore();
  return <section className={`${card} lg:col-span-12`}><SectionTitle icon={Radar} eyebrow="Runway Scheduling Results" title="Runway state board" /><div className="relative mb-5 overflow-hidden rounded-3xl border border-white/70 bg-white/40 px-5 py-4"><div className="h-2 rounded-full bg-slate-300/70" /><Plane className="runway-flyby absolute top-1 h-7 w-7 text-sky-600" /><div className="mt-3 flex justify-between text-[10px] font-black uppercase tracking-[0.2em] text-slate-400"><span>Approach</span><span>Runway allocation</span><span>Departure</span></div></div><div className="grid gap-4 md:grid-cols-4">{Object.entries(runways).map(([id, r]) => <div key={id} className={`relative overflow-hidden rounded-[2rem] border p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-2xl ${r.status === 'FREE' ? 'border-emerald-100 bg-white/60' : r.justSwitched ? 'border-sky-200 bg-sky-50/80 runway-switch-pulse' : 'border-rose-100 bg-rose-50/80'}`}><Plane className="absolute right-4 top-4 h-20 w-20 opacity-10" /><Plane className={`absolute right-5 top-5 h-7 w-7 ${r.status === 'FREE' ? 'text-emerald-500 animate-glide' : r.justSwitched ? 'text-sky-600 runway-takeoff' : 'text-rose-500 runway-card-plane'}`} /><div className="flex justify-between"><span className="text-[10px] font-black uppercase tracking-[0.24em] text-slate-400">Runway</span><span className={`h-3 w-3 rounded-full ${r.status === 'FREE' ? 'bg-emerald-500' : 'bg-rose-500'} shadow-lg`} /></div><div className="mt-3 text-4xl font-black">{id}</div><div className={`mt-2 text-xs font-black uppercase ${r.status === 'FREE' ? 'text-emerald-600' : 'text-rose-600'}`}>{r.status}</div><div className="mt-1 text-[10px] font-black uppercase tracking-wider text-slate-400">{r.assignedAC ? `Active: ${r.assignedAC}` : 'Ready for next flight'}</div><div className="mt-4 h-2 rounded-full bg-white/80"><div className="h-full rounded-full bg-sky-500 transition-all duration-500" style={{ width: `${r.utilization || 0}%` }} /></div><div className="mt-4 grid grid-cols-2 gap-2 text-[10px] font-black uppercase text-slate-400"><span>Queue: {r.queueLength || r.depth || 0}</span><span>Timer: {r.timer || 0}s</span><span>Wake: {r.sep || 0}s</span><span>Util: {r.utilization || 0}%</span></div></div>)}</div></section>;
};

const DigitalTwin = () => {
  const { scheduledResults, emergencies } = useTelemetryStore();
  return <section className={`${card} lg:col-span-12`}><SectionTitle icon={Map} eyebrow="Digital Twin" title="Aircraft movement, taxi routing, runway occupancy, and emergency reroute animation" /><div className="relative min-h-72 overflow-hidden rounded-[2rem] border border-white/70 bg-white/40 p-6"><div className="absolute left-12 right-12 top-1/2 h-3 rounded-full bg-slate-300/60" /><div className="absolute left-20 right-20 top-[35%] border-t border-dashed border-sky-400 flight-path" /><Plane className={`relative h-12 w-12 animate-glide ${emergencies.length ? 'text-rose-600' : 'text-sky-600'}`} style={{ left: `${Math.min(82, 10 + scheduledResults.length * 8)}%`, top: 20 }} /><Route className="absolute bottom-10 left-14 h-10 w-10 text-emerald-500 animate-radar" /><div className="mt-28 grid gap-3 md:grid-cols-4"><Metric icon={Plane} label="Aircraft Movement" value={scheduledResults.length ? 'Active' : 'Standby'} /><Metric icon={Route} label="Taxi Routing" value="Graph" tone="text-emerald-600" /><Metric icon={Radar} label="Runway Occupancy" value={scheduledResults.length} tone="text-amber-600" /><Metric icon={AlertTriangle} label="Emergency Reroute" value={emergencies.length ? 'Active' : 'Ready'} tone="text-rose-600" /></div></div></section>;
};

const RunwayStatusPage = () => {
  const { runways, runwayNotice } = useTelemetryStore();
  const runwayEntries = Object.entries(runways);
  const occupied = runwayEntries.filter(([, r]) => r.status !== 'FREE').length;
  return <>
    <section className={`${card} lg:col-span-12`}><SectionTitle icon={Radar} eyebrow="Runway Status" title="Available airport runways" /><div className="grid gap-4 md:grid-cols-3"><Metric icon={Radar} label="Total Runways" value={runwayEntries.length} /><Metric icon={CheckCircle} label="Free Runways" value={runwayEntries.length - occupied} tone="text-emerald-600" /><Metric icon={Plane} label="Occupied Runways" value={occupied} tone="text-rose-600" /></div><div className="mt-5 rounded-3xl border border-white/70 bg-white/45 p-4 text-sm font-bold leading-7 text-slate-600">This tab only shows basic runway information needed for the scheduler: runway name, current status, assigned aircraft, queue count, wake gap, timer, and utilization.</div></section>
    {runwayNotice && <section className="lg:col-span-12 rounded-[2rem] border border-sky-100 bg-sky-50/90 px-6 py-4 text-sm font-black text-sky-800 shadow-xl runway-switch-pulse"><Plane className="mr-2 inline h-5 w-5" />{runwayNotice}</section>}
    <RunwayBoard />
  </>;
};

const SequencedPlan = () => {
  const { scheduledResults } = useTelemetryStore();
  return <section className={`${card} lg:col-span-7`}><SectionTitle icon={BarChart3} eyebrow="Gantt Timeline" title="Sequenced runway plan" accent="text-emerald-600" /><div className="space-y-3">{scheduledResults.length ? scheduledResults.map((f, i) => <div key={`${f.id}-${i}`} className="grid items-center gap-4 rounded-3xl border border-white/70 bg-white/55 p-4 md:grid-cols-[110px_1fr_80px]"><div><div className="text-sm font-black">{f.id}</div><div className="text-[10px] font-bold text-slate-400">{f.assignedRunway}</div></div><div className="h-4 rounded-full bg-white/80"><div className="h-full rounded-full bg-sky-500" style={{ width: `${Math.min(100, 16 + i * 12)}%` }} /></div><div className="text-right font-mono text-xs font-black">T-{f.slotTime}s</div></div>) : <div className="rounded-3xl border border-dashed border-slate-200 bg-white/35 p-10 text-center font-bold text-slate-400">No schedule generated</div>}</div></section>;
};

const LiveOperations = () => {
  const { eventLog, kpis } = useTelemetryStore();
  const data = kpis();
  return <>
    <QueueMonitor />
    <section className={`${card} lg:col-span-5`}><SectionTitle icon={Activity} eyebrow="Live Telemetry" title="Operational KPIs" accent="text-emerald-600" /><div className="grid gap-4 md:grid-cols-2"><Metric icon={Clock} label="Avg Delay" value={`${data.avgDelay}s`} tone="text-amber-600" /><Metric icon={Radar} label="Runway Utilization" value={`${data.utilization}%`} /><Metric icon={ShieldAlert} label="Safety Score" value={`${data.safetyScore}%`} tone="text-emerald-600" /><Metric icon={Plane} label="Flights Handled" value={data.flightsHandled} /><Metric icon={TrendingDown} label="Conflict Reduction" value={`${data.conflictReduction}%`} tone="text-indigo-600" /></div></section>
    <EventLog title="Chronological event log" span="lg:col-span-12" />
  </>;
};

const EventLog = ({ title = 'Operational event archive', span = 'lg:col-span-12' }) => {
  const { eventLog } = useTelemetryStore();
  return <section className={`${card} ${span}`}><SectionTitle icon={Radio} eyebrow="Event History" title={title} accent="text-slate-600" /><div className="max-h-96 space-y-3 overflow-y-auto pr-1">{eventLog.length ? eventLog.map((e, i) => <div key={i} className="rounded-3xl border border-white/70 bg-white/55 p-4"><div className="font-mono text-[10px] font-black text-slate-400">{e.time} · {e.type}</div><div className="mt-1 text-sm font-bold text-slate-700">{e.msg}</div></div>) : <div className="rounded-3xl border border-dashed border-slate-200 bg-white/35 p-10 text-center font-bold text-slate-400">No events yet</div>}</div></section>;
};

const ArchiveAnalytics = () => {
  const { flights, predictions, algorithmSwitches, emergencies, compareResults, eventLog, kpis } = useTelemetryStore();
  const delayData = predictions.slice(0, 10).reverse().map((p, i) => ({ name: p.flightId || i + 1, delay: p.delay }));
  const data = kpis();
  return <>
    <section className={`${card} lg:col-span-12`}><SectionTitle icon={Archive} eyebrow="Archive / Analytics" title="Historical intelligence page" accent="text-slate-600" /><div className="grid gap-4 md:grid-cols-5"><Metric icon={Plane} label="Flight History" value={flights.length} /><Metric icon={Clock} label="Delay Records" value={predictions.length} tone="text-amber-600" /><Metric icon={Cpu} label="Switch Logs" value={algorithmSwitches.length} tone="text-indigo-600" /><Metric icon={AlertTriangle} label="Emergencies" value={emergencies.length} tone="text-rose-600" /><Metric icon={CheckCircle} label="Model Accuracy" value={`${Math.max(88, data.safetyScore)}%`} tone="text-emerald-600" /></div></section>
    <section className={`${card} lg:col-span-6`}><SectionTitle icon={BarChart3} eyebrow="Delay History" title="Predicted delay trend" /><ResponsiveContainer width="100%" height={260}><LineChart data={delayData}><CartesianGrid strokeDasharray="3 3" stroke="#dbeafe" /><XAxis dataKey="name" /><YAxis /><Tooltip /><Line type="monotone" dataKey="delay" stroke="#0284c7" strokeWidth={3} /></LineChart></ResponsiveContainer></section>
    <section className={`${card} lg:col-span-6`}><SectionTitle icon={Cpu} eyebrow="Algorithm Performance" title="Comparison archive" accent="text-indigo-600" /><ResponsiveContainer width="100%" height={260}><BarChart data={compareResults}><CartesianGrid strokeDasharray="3 3" stroke="#dbeafe" /><XAxis dataKey="algorithm" hide /><YAxis /><Tooltip /><Bar dataKey="avgDelay" fill="#6366f1" radius={[8, 8, 0, 0]} /></BarChart></ResponsiveContainer></section>
    <EventLog title="Audit logs and historical events" />
  </>;
};

export const FlightInputEngine = () => {
  const [activeTab, setActiveTab] = useState('FLIGHT_INTAKE');
  const { loadHistory, tickRunways } = useTelemetryStore();
  useEffect(() => { loadHistory(); }, [loadHistory]);
  useEffect(() => {
    const timer = setInterval(() => tickRunways(), 1000);
    return () => clearInterval(timer);
  }, [tickRunways]);
  const content = useMemo(() => ({
    FLIGHT_INTAKE: <FlightIntake />,
    SIMULATION_CONTROL: <SimulationControl />,
    RUNWAY_STATUS: <RunwayStatusPage />,
  }[activeTab]), [activeTab]);

  return (
    <main className="min-h-screen px-4 py-4 text-slate-800 sm:px-6 lg:px-8">
      <AeroSlotNavbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <section className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-12">{content}</section>
    </main>
  );
};
