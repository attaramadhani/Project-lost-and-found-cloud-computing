import React from 'react';
import { Search, Filter } from 'lucide-react';

const CATEGORIES = [
  'Semua Kategori',
  'Dokumen/KTM',
  'Kendaraan/Kunci',
  'Elektronik',
  'Pakaian/Aksesoris',
  'Lain-lain'
];

export default function FilterBar({
  activeType,
  setActiveType,
  category,
  setCategory,
  search,
  setSearch,
  totalCount
}) {
  const tabs = [
    { id: 'all', label: 'Semua Laporan' },
    { id: 'lost', label: 'Barang Hilang' },
    { id: 'found', label: 'Barang Ditemukan' },
    { id: 'resolved', label: 'Selesai' }
  ];

  return (
    <div className="space-y-4 mb-6">
      {/* Search and Category Filter */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Cari nama barang, deskripsi, atau lokasi (contoh: KTM, Vario, RKB)..."
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all shadow-sm"
          />
        </div>

        <div className="relative sm:w-64">
          <Filter className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full pl-10 pr-8 py-2.5 bg-white border border-slate-200 rounded-xl text-sm appearance-none focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all shadow-sm text-slate-700 cursor-pointer"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c === 'Semua Kategori' ? '' : c}>
                {c}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <div className="flex space-x-2 overflow-x-auto no-scrollbar">
          {tabs.map((tab) => {
            const isActive = activeType === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveType(tab.id)}
                className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
                  isActive
                    ? 'bg-sky-50 text-sky-700 font-semibold border border-sky-200/60 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        <span className="text-xs text-slate-400 font-medium pl-3 whitespace-nowrap">
          {totalCount} laporan
        </span>
      </div>
    </div>
  );
}
