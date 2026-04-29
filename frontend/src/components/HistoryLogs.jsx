import React, { useEffect, useState } from 'react';
import { History, Database, Trash2, Clock, CheckCircle2 } from 'lucide-react';

export const HistoryLogs = () => {
    const [history, setHistory] = useState([]);
    const [stats, setStats] = useState({ total: 0, emergencies: 0 });

    const load = async () => {
        try {
            const res = await fetch('http://127.0.0.1:5000/api/history');
            const h = await res.json();
            setHistory(h || []);
            setStats({ total: h.length, emergencies: h.filter(l => l.event_type.includes('EMG') || l.event_type.includes('EMERGENCY')).length });
        } catch (e) {
            console.error("Failed to load history", e);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const clearHistory = async () => {
        if (window.confirm("ARE YOU SURE YOU WANT TO PURGE LIVE AEROSLOT AUDIT LOGS?")) {
            try {
                await fetch('http://127.0.0.1:5000/api/clear', { method: 'POST' });
                await load();
            } catch (e) {
                console.error("Purge failure", e);
            }
        }
    };

    return (
        <div className="flex flex-col gap-10 h-full overflow-y-auto w-full max-w-7xl mx-auto custom-scrollbar px-4">
            <div className="flex justify-between items-center bg-white/40 backdrop-blur-3xl p-8 rounded-[3rem] border border-white shadow-sm">
                <div>
                    <h2 className="text-3xl font-black text-slate-900 flex items-center gap-5 uppercase tracking-tighter">
                        <History className="w-12 h-12 text-sky-600"/> AeroSlot Audit Archive
                    </h2>
                    <p className="text-[11px] font-black text-slate-400 uppercase tracking-[0.3em] mt-2 ml-16 italic">Post-Simulation Tactical Audit (MySQL Replication 01)</p>
                </div>
                <button onClick={clearHistory} className="bg-white/60 border-2 border-rose-100 hover:bg-rose-50 text-rose-600 px-10 py-4 rounded-[1.7rem] font-black text-sm flex items-center gap-3 shadow-sm transition-all active:scale-95">
                    <Trash2 className="w-5 h-5"/> PURGE AUDIT LOGS
                </button>
            </div>

            <div className="grid grid-cols-3 gap-10">
                <div className="glass-card p-12 flex items-center gap-10 bg-white border-2 border-white">
                    <div className="w-24 h-24 rounded-[2rem] bg-sky-50 flex items-center justify-center shadow-inner border border-white"><Database className="w-12 h-12 text-sky-600"/></div>
                    <div>
                        <div className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2">AeroSlot Event Count</div>
                        <div className="text-6xl font-black text-slate-900 tracking-tighter">{stats.total}</div>
                    </div>
                </div>
                <div className="glass-card p-12 flex items-center gap-10 bg-white border-2 border-white">
                    <div className="w-24 h-24 rounded-[2rem] bg-rose-50 flex items-center justify-center shadow-inner border border-white"><Clock className="w-12 h-12 text-rose-500"/></div>
                    <div>
                        <div className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2">Tactical Disruptions</div>
                        <div className="text-6xl font-black text-rose-600 tracking-tighter">{stats.emergencies}</div>
                    </div>
                </div>
                <div className="glass-card p-12 flex items-center gap-10 bg-white border-2 border-white">
                    <div className="w-24 h-24 rounded-[2rem] bg-emerald-50 flex items-center justify-center shadow-inner border border-white"><CheckCircle2 className="w-12 h-12 text-emerald-500"/></div>
                    <div>
                        <div className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2">AeroPersistence Node</div>
                        <div className="text-2xl font-black text-emerald-600 tracking-tight italic">ENCRYPTED</div>
                    </div>
                </div>
            </div>

            <div className="glass-card bg-white/60 border-white overflow-hidden shadow-2xl mb-12">
                <table className="w-full text-left text-xs">
                    <thead className="bg-white/80 text-slate-400 border-b border-white backdrop-blur-3xl">
                        <tr>
                            <th className="p-8 uppercase tracking-widest font-black">Audit Timestamp</th>
                            <th className="p-8 uppercase tracking-widest font-black">Event Domain</th>
                            <th className="p-8 uppercase tracking-widest font-black">Detailed Operational Protocol Log</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/40">
                        {history.length > 0 ? history.map((h, i) => (
                            <tr key={h.id || i} className="hover:bg-sky-50/40 transition-all group backdrop-blur-sm">
                                <td className="p-8 font-mono font-black text-slate-500 group-hover:text-sky-700">{h.timestamp}</td>
                                <td className="p-8">
                                    <span className={`px-5 py-2 rounded-2xl text-[10px] font-black uppercase tracking-widest border shadow-sm ${
                                        h.event_type.includes('EMG') || h.event_type.includes('EMERGENCY') 
                                        ? 'bg-rose-50 text-rose-600 border-rose-100' 
                                        : 'bg-sky-50 text-sky-700 border-sky-100'
                                    }`}>
                                        {h.event_type}
                                    </span>
                                </td>
                                <td className="p-8 text-slate-600 font-bold group-hover:text-slate-800 transition-colors italic whitespace-pre-wrap leading-relaxed">
                                    {h.event_msg}
                                </td>
                            </tr>
                        )) : (
                            <tr>
                                <td colSpan={3} className="p-40 text-center">
                                    <div className="flex flex-col items-center gap-8 opacity-20 bg-white/20 p-16 rounded-[4rem] border-2 border-white border-dashed">
                                        <History className="w-24 h-24 text-slate-500" />
                                        <p className="text-md font-black uppercase tracking-[0.6em] text-slate-700">Audit Node Standby</p>
                                    </div>
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
