import React, { useState } from 'react';
import { X, Send } from 'lucide-react';

const CATEGORIES = [
  'Dokumen/KTM',
  'Kendaraan/Kunci',
  'Elektronik',
  'Pakaian/Aksesoris',
  'Lain-lain'
];

export default function ModalReport({ isOpen, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    title: '',
    type: 'lost',
    category: 'Dokumen/KTM',
    description: '',
    location: '',
    date_event: new Date().toISOString().split('T')[0],
    contact_name: '',
    contact_phone: ''
  });
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(formData);
      onClose();
      // Reset
      setFormData({
        title: '',
        type: 'lost',
        category: 'Dokumen/KTM',
        description: '',
        location: '',
        date_event: new Date().toISOString().split('T')[0],
        contact_name: '',
        contact_phone: ''
      });
    } catch (err) {
      alert('Gagal membuat laporan: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="relative bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Buat Laporan Baru</h2>
            <p className="text-xs text-slate-500">Laporkan barang hilang atau barang yang Anda temukan</p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Tipe Laporan (Hilang vs Ditemukan) */}
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => setFormData({ ...formData, type: 'lost' })}
              className={`py-2 px-3 text-xs font-semibold rounded-xl border text-center transition-all ${
                formData.type === 'lost'
                  ? 'bg-rose-50 border-rose-300 text-rose-700 ring-2 ring-rose-500/20'
                  : 'border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              🔍 Saya Kehilangan Barang
            </button>

            <button
              type="button"
              onClick={() => setFormData({ ...formData, type: 'found' })}
              className={`py-2 px-3 text-xs font-semibold rounded-xl border text-center transition-all ${
                formData.type === 'found'
                  ? 'bg-emerald-50 border-emerald-300 text-emerald-700 ring-2 ring-emerald-500/20'
                  : 'border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              🎁 Saya Menemukan Barang
            </button>
          </div>

          {/* Judul Barang */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Nama / Judul Barang *
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="Contoh: KTM An. Dimas Prasetyo, Kunci Vario Hitam..."
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none"
            />
          </div>

          {/* Kategori & Tanggal */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Kategori</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none bg-white"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Perkiraan Tanggal</label>
              <input
                type="date"
                required
                value={formData.date_event}
                onChange={(e) => setFormData({ ...formData, date_event: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none"
              />
            </div>
          </div>

          {/* Lokasi */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Lokasi Kejadian *</label>
            <input
              type="text"
              required
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              placeholder="Contoh: Parkiran Fakultas Teknik, Gazebo Perpustakaan..."
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none"
            />
          </div>

          {/* Deskripsi */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Deskripsi & Ciri-ciri *</label>
            <textarea
              required
              rows={3}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Tuliskan warna, stiker, isi dompet, atau detail unik lainnya..."
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none"
            />
          </div>

          {/* Kontak Pelapor */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Nama Anda *</label>
              <input
                type="text"
                required
                value={formData.contact_name}
                onChange={(e) => setFormData({ ...formData, contact_name: e.target.value })}
                placeholder="Nama lengkap/panggilan"
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">No. WhatsApp *</label>
              <input
                type="tel"
                required
                value={formData.contact_phone}
                onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                placeholder="Contoh: 08123456789"
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 outline-none"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-3 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors"
            >
              Batal
            </button>

            <button
              type="submit"
              disabled={submitting}
              className="inline-flex items-center gap-1.5 px-5 py-2 bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{submitting ? 'Menyimpan...' : 'Kirim Laporan'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
