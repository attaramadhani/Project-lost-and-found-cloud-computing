import React from 'react';
import { Search, X } from 'lucide-react';

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
    <section aria-label="Filter dan pencarian laporan" className="space-y-4 mb-6">
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1 min-w-0">
          <label htmlFor="search-items" className="sr-only">
            Cari nama barang, deskripsi, atau lokasi
          </label>
          <Search
            className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-paper-slate dark:text-night-slate pointer-events-none"
            aria-hidden="true"
          />
          <input
            id="search-items"
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Cari nama barang, ciri, atau lokasi (mis. KTM, Vario, RKB)..."
            className="w-full min-h-[44px] pl-10 pr-11 py-2 bg-paper-surface dark:bg-night-surface border border-paper-border dark:border-night-border rounded-md text-sm text-paper-ink dark:text-night-ink placeholder:text-paper-slate dark:placeholder:text-night-slate"
          />
          {search && (
            <button
              type="button"
              onClick={() => setSearch('')}
              aria-label="Bersihkan kata kunci pencarian"
              className="absolute right-0.5 top-1/2 -translate-y-1/2 min-h-[40px] min-w-[40px] inline-flex items-center justify-center text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink rounded-md"
            >
              <X className="w-4 h-4" aria-hidden="true" />
            </button>
          )}
        </div>

        <div className="sm:w-64">
          <label htmlFor="category-filter" className="sr-only">
            Filter berdasarkan kategori barang
          </label>
          <select
            id="category-filter"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full min-h-[44px] px-3.5 py-2 bg-paper-surface dark:bg-night-surface border border-paper-border dark:border-night-border rounded-md text-sm text-paper-ink dark:text-night-ink"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c === 'Semua Kategori' ? '' : c}>
                {c}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-3 border-b border-paper-divider dark:border-night-divider pb-1 sm:pb-0">
        <div role="tablist" aria-label="Status laporan" className="grid grid-cols-2 sm:flex sm:flex-wrap items-center gap-1.5 sm:gap-2">
          {tabs.map((tab) => {
            const isActive = activeType === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={isActive}
                onClick={() => setActiveType(tab.id)}
                className={`min-h-[44px] px-3 py-2 text-sm text-left sm:text-center whitespace-nowrap border-b-2 transition-colors ${
                  isActive
                    ? 'border-cobalt dark:border-cobalt-light text-cobalt dark:text-cobalt-light font-semibold'
                    : 'border-transparent text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink font-medium'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        <p className="text-xs font-mono text-paper-slate dark:text-night-slate py-1.5 sm:py-2 whitespace-nowrap">
          {totalCount} laporan ditampilkan
        </p>
      </div>
    </section>
  );
}
