import React from 'react';
import { Server, Activity, Database, Cpu } from 'lucide-react';

export default function FooterInspector({ serverMeta, onPing, pinging }) {
  return (
    <footer className="mt-16 bg-slate-900 text-slate-300 py-6 px-4 border-t border-slate-800">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Cloud Architecture Inspector
              </p>
              <p className="text-sm font-medium text-white">
                Live Deployment & Load Balancing Monitor
              </p>
            </div>
          </div>

          <button
            onClick={onPing}
            disabled={pinging}
            className="inline-flex items-center space-x-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 rounded-lg border border-slate-700 transition-colors"
          >
            <Activity className={`w-3.5 h-3.5 text-sky-400 ${pinging ? 'animate-spin' : ''}`} />
            <span>Tes Ping Load Balancer</span>
          </button>
        </div>

        {/* Cloud Metadata Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 pt-4 text-xs">
          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-800 flex items-start space-x-2.5">
            <Server className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
            <div>
              <div className="text-slate-400">Backend Instance (Node)</div>
              <div className="text-sky-300 font-mono font-semibold text-sm">
                {serverMeta?.served_by || 'Connecting...'}
              </div>
            </div>
          </div>

          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-800 flex items-start space-x-2.5">
            <Cpu className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <div>
              <div className="text-slate-400">Container Hostname</div>
              <div className="text-slate-200 font-mono">
                {serverMeta?.hostname || 'Unknown'}
              </div>
            </div>
          </div>

          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-800 flex items-start space-x-2.5">
            <Database className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <div className="text-slate-400">Database Layer (VM 3)</div>
              <div className="text-emerald-300 font-medium">
                {serverMeta?.database?.mode === 'mysql-connected'
                  ? 'MySQL Container Connected'
                  : 'In-Memory Fallback (Local)'}
              </div>
            </div>
          </div>

          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-800 flex items-start space-x-2.5">
            <Activity className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <div className="text-slate-400">Reverse Proxy / Load Balancer</div>
              <div className="text-slate-200 font-medium">Nginx Round-Robin Active</div>
            </div>
          </div>
        </div>

        <div className="pt-4 text-center text-slate-500 text-xs">
          Final Project Mata Kuliah Cloud Computing • Prodi Sistem Informasi • Universitas Trunojoyo Madura
        </div>
      </div>
    </footer>
  );
}
