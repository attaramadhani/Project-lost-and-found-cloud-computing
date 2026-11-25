import React, { useState, useEffect, useCallback, useRef } from 'react';
import Navbar from './components/Navbar';
import FilterBar from './components/FilterBar';
import ItemCard from './components/ItemCard';
import ModalReport from './components/ModalReport';
import FooterInspector from './components/FooterInspector';
import { AlertCircle, X } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function getInitialTheme() {
  if (typeof window === 'undefined') return 'light';
  const saved = window.localStorage.getItem('clf-theme');
  if (saved === 'dark' || saved === 'light') return saved;
  return 'light';
}

export default function App() {
  const [theme, setTheme] = useState(getInitialTheme);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionFeedback, setActionFeedback] = useState(null);

  const params =
    typeof window !== 'undefined'
      ? new URLSearchParams(window.location.search)
      : new URLSearchParams();

  const [activeType, setActiveType] = useState(params.get('type') || 'all');
  const [category, setCategory] = useState(params.get('category') || '');
  const [search, setSearch] = useState(params.get('search') || '');
  const [isModalOpen, setIsModalOpen] = useState(params.get('modal') === 'true');

  const [serverMeta, setServerMeta] = useState(null);
  const [healthError, setHealthError] = useState(false);
  const [pinging, setPinging] = useState(false);
  const [pingHistory, setPingHistory] = useState([]);
  const pingSeqRef = useRef(0);

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    window.localStorage.setItem('clf-theme', theme);
  }, [theme]);

  const recordPing = useCallback((nodeName) => {
    if (!nodeName) return;
    pingSeqRef.current += 1;
    const seq = pingSeqRef.current;
    const time = new Date().toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
    setPingHistory((prev) => [{ seq, node: nodeName, time }, ...prev].slice(0, 5));
  }, []);

  const fetchHealth = useCallback(async (isManualPing = false) => {
    try {
      setPinging(true);
      setHealthError(false);
      const res = await fetch(`${API_BASE}/health?_t=${Date.now()}`);
      if (!res.ok) throw new Error('Health endpoint error');
      const data = await res.json();
      setServerMeta(data);
      if (isManualPing) {
        recordPing(data.served_by || 'unknown-node');
      }
    } catch {
      setHealthError(true);
    } finally {
      setPinging(false);
    }
  }, [recordPing]);

  const fetchItems = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const query = new URLSearchParams();
      if (activeType === 'lost' || activeType === 'found') {
        query.append('type', activeType);
      } else if (activeType === 'resolved') {
        query.append('status', 'resolved');
      }
      if (category) query.append('category', category);
      if (search) query.append('search', search);

      const res = await fetch(`${API_BASE}/items?${query.toString()}&_t=${Date.now()}`);
      if (!res.ok) throw new Error('Gagal mengambil daftar laporan dari server backend.');

      const json = await res.json();
      setItems(json.data || []);

      if (json.served_by) {
        setServerMeta((prev) => ({
          ...prev,
          served_by: json.served_by
        }));
      }
    } catch (err) {
      setError(err.message || 'Server backend tidak dapat dijangkau.');
    } finally {
      setLoading(false);
    }
  }, [activeType, category, search]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  useEffect(() => {
    fetchHealth(false);
  }, [fetchHealth]);

  const handleCreate = async (formData) => {
    const res = await fetch(`${API_BASE}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || 'Gagal mengirim laporan.');
    }
    setActionFeedback({ type: 'success', text: 'Laporan baru berhasil disimpan.' });
    await Promise.all([fetchItems(), fetchHealth(false)]);
  };

  const handleResolve = async (id) => {
    try {
      setActionFeedback(null);
      const res = await fetch(`${API_BASE}/items/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'resolved' })
      });
      if (!res.ok) throw new Error('Gagal memperbarui status laporan.');
      setActionFeedback({ type: 'success', text: 'Laporan ditandai selesai.' });
      await fetchItems();
    } catch (err) {
      setActionFeedback({ type: 'error', text: err.message });
    }
  };

  const handleDelete = async (id) => {
    try {
      setActionFeedback(null);
      const res = await fetch(`${API_BASE}/items/${id}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error('Gagal menghapus laporan.');
      setActionFeedback({ type: 'success', text: 'Laporan berhasil dihapus.' });
      await fetchItems();
    } catch (err) {
      setActionFeedback({ type: 'error', text: err.message });
    }
  };

  const hasActiveFilters = activeType !== 'all' || Boolean(category) || Boolean(search);
  const openLostCount = items.filter((i) => i.status !== 'resolved' && i.type === 'lost').length;
  const openFoundCount = items.filter((i) => i.status !== 'resolved' && i.type === 'found').length;
  const resolvedCount = items.filter((i) => i.status === 'resolved').length;

  return (
    <div className="min-h-screen flex flex-col justify-between bg-paper-bg dark:bg-night-bg text-paper-ink dark:text-night-ink">
      <a
        href="#daftar-laporan"
        className="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:px-4 focus:py-2 focus:bg-cobalt focus:text-white focus:rounded-md focus:text-sm focus:font-semibold"
      >
        Lewati ke daftar laporan
      </a>

      <div>
        <Navbar
          onOpenModal={() => setIsModalOpen(true)}
          onRefresh={() => {
            fetchItems();
            fetchHealth(false);
          }}
          loading={loading}
          theme={theme}
          onToggleTheme={() => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))}
        />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
          {/* Asymmetric Editorial Masthead */}
          <section
            aria-labelledby="page-heading"
            className="mb-8 pb-6 border-b border-paper-divider dark:border-night-divider grid grid-cols-1 lg:grid-cols-12 gap-6 items-end"
          >
            <div className="lg:col-span-7">
              <div className="w-10 h-1 bg-cobalt dark:bg-cobalt-light mb-3" aria-hidden="true" />
              <h1
                id="page-heading"
                className="font-display text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-paper-ink dark:text-night-ink leading-tight mb-2.5"
              >
                Pusat Pelaporan Barang Hilang &amp; Ditemukan
              </h1>
              <p className="text-sm sm:text-base text-paper-slate dark:text-night-slate leading-relaxed max-w-2xl">
                Laporkan kehilangan KTM, dompet, kunci kendaraan, atau barang temuan di lingkungan kampus agar pemilik dan penemu dapat terhubung langsung.
              </p>
            </div>

            {/* Live Ledger Summary from actual fetched records */}
            <div className="lg:col-span-5 bg-paper-surface dark:bg-night-surface border border-paper-divider dark:border-night-divider rounded-md p-4">
              <div className="flex items-center justify-between gap-2 pb-2.5 mb-3 border-b border-paper-divider dark:border-night-divider">
                <span className="text-xs font-semibold text-paper-slate dark:text-night-slate">
                  Ringkasan Tampilan Saat Ini
                </span>
                <span className="text-xs font-mono text-paper-ink dark:text-night-ink font-semibold">
                  {loading ? 'Memuat...' : `${items.length} total`}
                </span>
              </div>
              <dl className="grid grid-cols-3 gap-3 text-left">
                <div>
                  <dt className="text-xs text-paper-slate dark:text-night-slate">Hilang</dt>
                  <dd className="font-display text-xl font-bold text-red-700 dark:text-red-300 mt-0.5">
                    {loading ? '-' : openLostCount}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-paper-slate dark:text-night-slate">Ditemukan</dt>
                  <dd className="font-display text-xl font-bold text-green-700 dark:text-green-300 mt-0.5">
                    {loading ? '-' : openFoundCount}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-paper-slate dark:text-night-slate">Selesai</dt>
                  <dd className="font-display text-xl font-bold text-paper-ink dark:text-night-ink mt-0.5">
                    {loading ? '-' : resolvedCount}
                  </dd>
                </div>
              </dl>
            </div>
          </section>

          {/* Action Feedback Banner (replaces window.alert) */}
          {actionFeedback && (
            <div
              role="status"
              className={`mb-6 p-3.5 rounded-md border flex items-center justify-between gap-3 text-sm ${
                actionFeedback.type === 'error'
                  ? 'bg-red-50 dark:bg-red-950 border-red-300 dark:border-red-800 text-red-700 dark:text-red-300'
                  : 'bg-green-50 dark:bg-green-950 border-green-300 dark:border-green-800 text-green-700 dark:text-green-300'
              }`}
            >
              <span>{actionFeedback.text}</span>
              <button
                type="button"
                onClick={() => setActionFeedback(null)}
                aria-label="Tutup notifikasi"
                className="min-h-[44px] min-w-[44px] inline-flex items-center justify-center rounded-md hover:bg-black/5 dark:hover:bg-white/10"
              >
                <X className="w-4 h-4" aria-hidden="true" />
              </button>
            </div>
          )}

          {/* Filter Bar */}
          <FilterBar
            activeType={activeType}
            setActiveType={setActiveType}
            category={category}
            setCategory={setCategory}
            search={search}
            setSearch={setSearch}
            totalCount={items.length}
          />

          {/* Data View: Loading / Error / Empty / List */}
          <section id="daftar-laporan" aria-label="Daftar laporan barang">
            {error ? (
              <div
                role="alert"
                className="p-5 bg-red-50 dark:bg-red-950 border border-red-300 dark:border-red-800 rounded-md flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-700 dark:text-red-300 shrink-0 mt-0.5" aria-hidden="true" />
                  <div>
                    <h2 className="text-sm font-bold text-red-700 dark:text-red-300">
                      Koneksi ke Server Backend Gagal
                    </h2>
                    <p className="text-xs text-red-700 dark:text-red-300 mt-1">
                      {error} Pastikan API berjalan di <span className="font-mono">{API_BASE}</span>.
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={fetchItems}
                  className="min-h-[44px] px-4 py-2 bg-red-700 hover:bg-red-800 text-white text-xs sm:text-sm font-semibold rounded-md transition-colors shrink-0"
                >
                  Coba Muat Ulang
                </button>
              </div>
            ) : loading ? (
              <div role="status" aria-live="polite" className="space-y-4">
                <p className="text-sm text-paper-slate dark:text-night-slate font-medium">
                  Memuat daftar laporan barang dari server...
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  {[1, 2, 3].map((n) => (
                    <div
                      key={n}
                      className="bg-paper-surface dark:bg-night-surface rounded-md p-5 border border-paper-divider dark:border-night-divider space-y-3"
                    >
                      <div className="h-5 bg-paper-stone dark:bg-night-elevated rounded-sm w-1/3" />
                      <div className="h-6 bg-paper-stone dark:bg-night-elevated rounded-sm w-3/4" />
                      <div className="h-16 bg-paper-stone dark:bg-night-elevated rounded-sm" />
                      <div className="h-4 bg-paper-stone dark:bg-night-elevated rounded-sm w-1/2" />
                    </div>
                  ))}
                </div>
              </div>
            ) : items.length === 0 ? (
              <div className="py-12 px-6 bg-paper-surface dark:bg-night-surface rounded-md border border-dashed border-paper-border dark:border-night-border text-center space-y-3">
                <h2 className="font-display text-lg font-bold text-paper-ink dark:text-night-ink">
                  {hasActiveFilters
                    ? 'Tidak ada laporan yang cocok dengan filter ini'
                    : 'Belum ada laporan barang'}
                </h2>
                <p className="text-sm text-paper-slate dark:text-night-slate max-w-md mx-auto">
                  {hasActiveFilters
                    ? 'Ubah kata kunci pencarian, kategori, atau pilih tab Semua Laporan untuk melihat seluruh data.'
                    : 'Jadilah yang pertama melaporkan barang hilang atau temuan di lingkungan kampus.'}
                </p>
                <div className="pt-2 flex justify-center">
                  {hasActiveFilters ? (
                    <button
                      type="button"
                      onClick={() => {
                        setActiveType('all');
                        setCategory('');
                        setSearch('');
                      }}
                      className="min-h-[44px] px-4 py-2 bg-paper-stone dark:bg-night-elevated hover:bg-paper-divider dark:hover:bg-night-divider border border-paper-border dark:border-night-border text-sm font-semibold text-paper-ink dark:text-night-ink rounded-md transition-colors"
                    >
                      Reset Semua Filter
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={() => setIsModalOpen(true)}
                      className="min-h-[44px] px-5 py-2 bg-cobalt hover:bg-cobalt-hover text-white text-sm font-semibold rounded-md transition-colors"
                    >
                      Buat Laporan Pertama
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {items.map((item, idx) => (
                  <ItemCard
                    key={item.id}
                    item={item}
                    featured={
                      idx === 0 &&
                      activeType === 'all' &&
                      !category &&
                      !search &&
                      items.length >= 3 &&
                      item.status !== 'resolved'
                    }
                    onResolve={handleResolve}
                    onDelete={handleDelete}
                  />
                ))}
              </div>
            )}
          </section>
        </main>
      </div>

      <FooterInspector
        serverMeta={serverMeta}
        pingHistory={pingHistory}
        onPing={() => fetchHealth(true)}
        pinging={pinging}
        healthError={healthError}
      />

      <ModalReport
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreate}
      />
    </div>
  );
}
