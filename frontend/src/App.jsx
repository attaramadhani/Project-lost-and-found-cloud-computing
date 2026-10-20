import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import FilterBar from './components/FilterBar';
import ItemCard from './components/ItemCard';
import ModalReport from './components/ModalReport';
import FooterInspector from './components/FooterInspector';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export default function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [activeType, setActiveType] = useState('all');
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');

  // Modal
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Cloud Inspector Metadata
  const [serverMeta, setServerMeta] = useState(null);
  const [pinging, setPinging] = useState(false);

  // Fetch Health & Inspector info
  const fetchHealth = useCallback(async () => {
    try {
      setPinging(true);
      const res = await fetch(`${API_BASE}/health?_t=${Date.now()}`);
      if (res.ok) {
        const data = await res.json();
        setServerMeta(data);
      }
    } catch (err) {
      console.warn('Health check unreachable:', err);
    } finally {
      setPinging(false);
    }
  }, []);

  // Fetch Items
  const fetchItems = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      if (activeType === 'lost' || activeType === 'found') {
        params.append('type', activeType);
      } else if (activeType === 'resolved') {
        params.append('status', 'resolved');
      }
      if (category) params.append('category', category);
      if (search) params.append('search', search);

      const res = await fetch(`${API_BASE}/items?${params.toString()}&_t=${Date.now()}`);
      if (!res.ok) throw new Error('Gagal mengambil data dari backend');

      const json = await res.json();
      setItems(json.data || []);
      
      // Update inspector server node from headers or json
      if (json.served_by) {
        setServerMeta((prev) => ({
          ...prev,
          served_by: json.served_by
        }));
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [activeType, category, search]);

  useEffect(() => {
    fetchItems();
    fetchHealth();
  }, [fetchItems, fetchHealth]);

  // Actions
  const handleCreate = async (formData) => {
    const res = await fetch(`${API_BASE}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.message || 'Gagal mengirim laporan');
    }
    await fetchItems();
    await fetchHealth();
  };

  const handleResolve = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/items/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'resolved' })
      });
      if (!res.ok) throw new Error('Gagal mengupdate status');
      await fetchItems();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Apakah Anda yakin ingin menghapus laporan ini?')) return;
    try {
      const res = await fetch(`${API_BASE}/items/${id}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error('Gagal menghapus laporan');
      await fetchItems();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between bg-slate-50 selection:bg-sky-500 selection:text-white">
      <div>
        <Navbar
          onOpenModal={() => setIsModalOpen(true)}
          onRefresh={() => {
            fetchItems();
            fetchHealth();
          }}
          loading={loading}
        />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Hero Banner */}
          <div className="mb-8 p-6 sm:p-8 bg-gradient-to-r from-sky-600 via-indigo-600 to-indigo-700 rounded-3xl text-white shadow-xl shadow-sky-600/10">
            <div className="max-w-2xl">
              <span className="inline-block px-3 py-1 bg-white/20 backdrop-blur-md text-xs font-semibold rounded-full mb-3 uppercase tracking-wider">
                Portal Resmi Komunitas Kampus
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight mb-2">
                Pusat Pelaporan Barang Hilang & Ditemukan
              </h2>
              <p className="text-sky-100 text-sm sm:text-base leading-relaxed">
                Kehilangan KTM, dompet, kunci kendaraan, atau barang berharga di lingkungan kampus? Temukan kembali atau bantu sesama mahasiswa dengan melaporkannya di sini.
              </p>
            </div>
          </div>

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

          {/* Error Alert */}
          {error && (
            <div className="mb-6 p-4 bg-rose-50 border border-rose-200 text-rose-700 text-sm rounded-2xl flex items-center justify-between">
              <div>
                <p className="font-semibold">Koneksi Backend Terkendala</p>
                <p className="text-xs text-rose-600">{error} - Pastikan server backend di port 5000 aktif.</p>
              </div>
              <button
                onClick={fetchItems}
                className="px-3 py-1 bg-rose-600 text-white text-xs font-medium rounded-lg hover:bg-rose-700 transition"
              >
                Coba Lagi
              </button>
            </div>
          )}

          {/* Item Grid */}
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <div key={n} className="bg-white rounded-2xl p-5 border border-slate-100 animate-pulse space-y-3">
                  <div className="h-5 bg-slate-200 rounded w-1/3"></div>
                  <div className="h-6 bg-slate-200 rounded w-3/4"></div>
                  <div className="h-16 bg-slate-200 rounded"></div>
                  <div className="h-4 bg-slate-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : items.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-slate-200">
              <p className="text-slate-400 text-sm">Tidak ada laporan barang yang sesuai filter pencarian.</p>
              <button
                onClick={() => {
                  setActiveType('all');
                  setCategory('');
                  setSearch('');
                }}
                className="mt-3 text-xs font-semibold text-sky-600 hover:underline"
              >
                Reset Semua Filter
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {items.map((item) => (
                <ItemCard
                  key={item.id}
                  item={item}
                  onResolve={handleResolve}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </main>
      </div>

      <FooterInspector
        serverMeta={serverMeta}
        onPing={fetchHealth}
        pinging={pinging}
      />

      <ModalReport
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreate}
      />
    </div>
  );
}
