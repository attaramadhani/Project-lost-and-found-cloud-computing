import React from 'react';
import { Compass, PlusCircle, RefreshCw } from 'lucide-react';

export default function Navbar({ onOpenModal, onRefresh, loading }) {
  return (
    <header className="sticky top-0 z-30 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/20">
            <Compass className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-900 leading-tight">Campus Lost & Found</h1>
            <p className="text-xs text-slate-500 hidden sm:block">Cloud Computing Architecture Demo • SI UTM</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={onRefresh}
            disabled={loading}
            title="Refresh Data"
            className="p-2 text-slate-600 hover:text-sky-600 hover:bg-slate-100 rounded-lg transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin text-sky-600' : ''}`} />
          </button>
          
          <button
            onClick={onOpenModal}
            className="inline-flex items-center space-x-2 px-4 py-2 bg-sky-600 hover:bg-sky-700 active:bg-sky-800 text-white text-sm font-medium rounded-xl shadow-sm transition-all hover:shadow-md"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Lapor Barang</span>
          </button>
        </div>
      </div>
    </header>
  );
}
