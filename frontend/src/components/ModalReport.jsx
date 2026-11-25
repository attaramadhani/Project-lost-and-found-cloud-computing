import React, { useState, useEffect, useRef } from 'react';
import { X, Check, AlertCircle } from 'lucide-react';

const CATEGORIES = [
  'Dokumen/KTM',
  'Kendaraan/Kunci',
  'Elektronik',
  'Pakaian/Aksesoris',
  'Lain-lain'
];

const INITIAL_FORM = () => ({
  title: '',
  type: 'lost',
  category: 'Dokumen/KTM',
  description: '',
  location: '',
  date_event: new Date().toISOString().split('T')[0],
  contact_name: '',
  contact_phone: ''
});

export default function ModalReport({ isOpen, onClose, onSubmit }) {
  const [formData, setFormData] = useState(INITIAL_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const titleInputRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;
    setSubmitError(null);
    const timer = setTimeout(() => {
      titleInputRef.current?.focus();
    }, 30);

    const onKeyDown = (e) => {
      if (e.key === 'Escape' && !submitting) {
        onClose();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('keydown', onKeyDown);
    };
  }, [isOpen, onClose, submitting]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitError(null);
    try {
      await onSubmit(formData);
      setFormData(INITIAL_FORM());
      onClose();
    } catch (err) {
      setSubmitError(err.message || 'Gagal mengirim laporan ke server.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 overflow-y-auto bg-black/60 flex items-center justify-center p-4"
      onClick={(e) => {
        if (e.target === e.currentTarget && !submitting) onClose();
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-report-title"
        className="relative bg-paper-surface dark:bg-night-surface border border-paper-border dark:border-night-border rounded-md max-w-lg w-full p-5 sm:p-6 my-8"
      >
        <div className="flex items-start justify-between gap-3 pb-3 border-b border-paper-divider dark:border-night-divider mb-4">
          <div>
            <h2
              id="modal-report-title"
              className="font-display text-xl font-bold text-paper-ink dark:text-night-ink"
            >
              Buat Laporan Barang
            </h2>
            <p className="text-xs text-paper-slate dark:text-night-slate mt-0.5">
              Isi detail barang yang hilang atau Anda temukan di area kampus.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={submitting}
            aria-label="Tutup dialog laporan"
            className="min-h-[44px] min-w-[44px] -mt-2 -mr-2 inline-flex items-center justify-center rounded-md text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink hover:bg-paper-stone dark:hover:bg-night-elevated transition-colors"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>

        {submitError && (
          <div
            role="alert"
            className="mb-4 p-3 rounded-md bg-red-50 dark:bg-red-950 border border-red-300 dark:border-red-800 text-red-700 dark:text-red-300 text-xs flex items-start gap-2"
          >
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" aria-hidden="true" />
            <span>{submitError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Report Type */}
          <fieldset>
            <legend className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1.5">
              Jenis Laporan
            </legend>
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                aria-pressed={formData.type === 'lost'}
                onClick={() => setFormData({ ...formData, type: 'lost' })}
                className={`min-h-[44px] px-3 py-2 text-xs sm:text-sm font-semibold rounded-md border inline-flex items-center justify-center gap-1.5 transition-colors ${
                  formData.type === 'lost'
                    ? 'bg-red-50 dark:bg-red-950 border-red-700 dark:border-red-400 text-red-700 dark:text-red-300'
                    : 'bg-paper-bg dark:bg-night-bg border-paper-border dark:border-night-border text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink'
                }`}
              >
                {formData.type === 'lost' && <Check className="w-4 h-4" aria-hidden="true" />}
                <span>Barang Hilang</span>
              </button>

              <button
                type="button"
                aria-pressed={formData.type === 'found'}
                onClick={() => setFormData({ ...formData, type: 'found' })}
                className={`min-h-[44px] px-3 py-2 text-xs sm:text-sm font-semibold rounded-md border inline-flex items-center justify-center gap-1.5 transition-colors ${
                  formData.type === 'found'
                    ? 'bg-green-50 dark:bg-green-950 border-green-700 dark:border-green-400 text-green-700 dark:text-green-300'
                    : 'bg-paper-bg dark:bg-night-bg border-paper-border dark:border-night-border text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink'
                }`}
              >
                {formData.type === 'found' && <Check className="w-4 h-4" aria-hidden="true" />}
                <span>Barang Ditemukan</span>
              </button>
            </div>
          </fieldset>

          {/* Title */}
          <div>
            <label
              htmlFor="report-title"
              className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
            >
              Nama / Judul Barang <span aria-hidden="true">*</span>
            </label>
            <input
              ref={titleInputRef}
              id="report-title"
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="Contoh: KTM An. Dimas Prasetyo, Kunci Vario Hitam"
              className="w-full min-h-[44px] px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink placeholder:text-paper-slate dark:placeholder:text-night-slate"
            />
          </div>

          {/* Category & Date */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label
                htmlFor="report-category"
                className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
              >
                Kategori
              </label>
              <select
                id="report-category"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full min-h-[44px] px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label
                htmlFor="report-date"
                className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
              >
                Perkiraan Tanggal <span aria-hidden="true">*</span>
              </label>
              <input
                id="report-date"
                type="date"
                required
                value={formData.date_event}
                onChange={(e) => setFormData({ ...formData, date_event: e.target.value })}
                className="w-full min-h-[44px] px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink"
              />
            </div>
          </div>

          {/* Location */}
          <div>
            <label
              htmlFor="report-location"
              className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
            >
              Lokasi Kejadian <span aria-hidden="true">*</span>
            </label>
            <input
              id="report-location"
              type="text"
              required
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              placeholder="Contoh: Parkiran Fakultas Teknik, Gazebo Perpustakaan"
              className="w-full min-h-[44px] px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink placeholder:text-paper-slate dark:placeholder:text-night-slate"
            />
          </div>

          {/* Description */}
          <div>
            <label
              htmlFor="report-description"
              className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
            >
              Deskripsi &amp; Ciri Fisik <span aria-hidden="true">*</span>
            </label>
            <textarea
              id="report-description"
              required
              rows={3}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Tuliskan warna, merek, stiker, atau ciri khusus lainnya..."
              className="w-full px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink placeholder:text-paper-slate dark:placeholder:text-night-slate"
            />
          </div>

          {/* Contact */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label
                htmlFor="report-contact-name"
                className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
              >
                Nama Pelapor <span aria-hidden="true">*</span>
              </label>
              <input
                id="report-contact-name"
                type="text"
                required
                value={formData.contact_name}
                onChange={(e) => setFormData({ ...formData, contact_name: e.target.value })}
                placeholder="Nama lengkap atau panggilan"
                className="w-full min-h-[44px] px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink placeholder:text-paper-slate dark:placeholder:text-night-slate"
              />
            </div>

            <div>
              <label
                htmlFor="report-contact-phone"
                className="block text-xs font-semibold text-paper-ink dark:text-night-ink mb-1"
              >
                Nomor WhatsApp <span aria-hidden="true">*</span>
              </label>
              <input
                id="report-contact-phone"
                type="tel"
                required
                value={formData.contact_phone}
                onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                placeholder="Contoh: 081234567890"
                className="w-full min-h-[44px] px-3 py-2 text-sm bg-paper-surface dark:bg-night-bg border border-paper-border dark:border-night-border rounded-md text-paper-ink dark:text-night-ink placeholder:text-paper-slate dark:placeholder:text-night-slate"
              />
            </div>
          </div>

          {/* Submit Row */}
          <div className="pt-4 flex flex-wrap justify-end gap-2.5 border-t border-paper-divider dark:border-night-divider">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="min-h-[44px] px-4 py-2 text-sm font-semibold text-paper-ink dark:text-night-ink bg-paper-stone dark:bg-night-elevated hover:bg-paper-divider dark:hover:bg-night-divider border border-paper-border dark:border-night-border rounded-md transition-colors"
            >
              Batal
            </button>

            <button
              type="submit"
              disabled={submitting}
              className="min-h-[44px] px-5 py-2 bg-cobalt hover:bg-cobalt-hover text-white text-sm font-semibold rounded-md transition-colors disabled:opacity-50"
            >
              {submitting ? 'Menyimpan Laporan...' : 'Kirim Laporan'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
