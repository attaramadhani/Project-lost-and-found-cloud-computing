import React, { useState } from 'react';
import { MapPin, Calendar, Phone, Check, Trash2, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function ItemCard({ item, onResolve, onDelete, featured = false }) {
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [busyAction, setBusyAction] = useState(null);

  const isLost = item.type === 'lost';
  const isResolved = item.status === 'resolved';

  const formatWaNumber = (phone) => {
    let clean = String(phone || '').replace(/[^0-9]/g, '');
    if (clean.startsWith('0')) {
      clean = '62' + clean.slice(1);
    }
    return clean;
  };

  const waLink = `https://wa.me/${formatWaNumber(item.contact_phone)}?text=${encodeURIComponent(
    `Halo ${item.contact_name}, saya melihat informasi terkait "${item.title}" di portal Campus Lost & Found.`
  )}`;

  const formattedDate = new Date(item.date_event).toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });

  const handleResolveClick = async () => {
    setBusyAction('resolve');
    try {
      await onResolve(item.id);
    } finally {
      setBusyAction(null);
    }
  };

  const handleConfirmDelete = async () => {
    setBusyAction('delete');
    try {
      await onDelete(item.id);
    } finally {
      setBusyAction(null);
      setConfirmingDelete(false);
    }
  };

  const statusBadge = isResolved ? (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm text-xs font-semibold bg-paper-stone dark:bg-night-elevated text-paper-ink dark:text-night-ink border border-paper-divider dark:border-night-divider">
      <Check className="w-3.5 h-3.5" aria-hidden="true" />
      <span>Selesai</span>
    </span>
  ) : isLost ? (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm text-xs font-semibold bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300 border border-red-300 dark:border-red-800">
      <AlertCircle className="w-3.5 h-3.5" aria-hidden="true" />
      <span>Hilang</span>
    </span>
  ) : (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm text-xs font-semibold bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 border border-green-300 dark:border-green-800">
      <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
      <span>Ditemukan</span>
    </span>
  );

  return (
    <article
      className={`border rounded-md p-5 flex flex-col justify-between ${
        featured ? 'md:col-span-2 lg:col-span-2' : ''
      } ${
        isResolved
          ? 'bg-paper-stone/60 dark:bg-night-bg border-paper-divider dark:border-night-divider'
          : 'bg-paper-surface dark:bg-night-surface border-paper-border/70 dark:border-night-border'
      }`}
    >
      <div className={featured ? 'grid grid-cols-1 lg:grid-cols-12 gap-5' : ''}>
        <div className={featured ? 'lg:col-span-7' : ''}>
          {/* Header Row: Status + Category + Delete */}
          <div className="flex items-start justify-between gap-2 mb-3">
            <div className="flex items-center gap-2 flex-wrap">
              {statusBadge}
              <span className="text-xs font-mono px-2.5 py-1 rounded-sm bg-paper-bg dark:bg-night-bg text-paper-slate dark:text-night-slate border border-paper-divider dark:border-night-divider">
                {item.category}
              </span>
              {featured && (
                <span className="text-xs font-semibold text-cobalt dark:text-cobalt-light">
                  Laporan Terbaru
                </span>
              )}
            </div>

            {!confirmingDelete && (
              <button
                type="button"
                onClick={() => setConfirmingDelete(true)}
                aria-label={`Hapus laporan ${item.title}`}
                title="Hapus laporan"
                className="min-h-[44px] min-w-[44px] -mt-2 -mr-2 inline-flex items-center justify-center rounded-md text-paper-slate dark:text-night-slate hover:text-red-700 dark:hover:text-red-300 hover:bg-paper-stone dark:hover:bg-night-elevated transition-colors"
              >
                <Trash2 className="w-4 h-4" aria-hidden="true" />
              </button>
            )}
          </div>

          {/* Title & Description */}
          <h3
            className={`font-display text-base sm:text-lg font-bold leading-snug mb-2 ${
              isResolved
                ? 'line-through text-paper-slate dark:text-night-slate'
                : 'text-paper-ink dark:text-night-ink'
            }`}
          >
            {item.title}
          </h3>
          <p className={`text-sm text-paper-slate dark:text-night-slate leading-relaxed mb-4 ${featured ? '' : 'line-clamp-3'}`}>
            {item.description}
          </p>
        </div>

        {/* Metadata */}
        <div
          className={`space-y-2 text-xs text-paper-slate dark:text-night-slate ${
            featured
              ? 'lg:col-span-5 lg:border-l lg:border-paper-divider lg:dark:border-night-divider lg:pl-5 flex flex-col justify-center'
              : 'mb-4'
          }`}
        >
          <div className="flex items-start gap-2">
            <MapPin className="w-4 h-4 shrink-0 mt-0.5 text-paper-ink dark:text-night-ink" aria-hidden="true" />
            <span className="font-semibold text-paper-ink dark:text-night-ink break-words">{item.location}</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 shrink-0 text-paper-slate dark:text-night-slate" aria-hidden="true" />
            <span>Kejadian: {formattedDate}</span>
          </div>
          <div className="flex items-start gap-2">
            <Phone className="w-4 h-4 shrink-0 mt-0.5 text-paper-slate dark:text-night-slate" aria-hidden="true" />
            <span className="break-words">
              {item.contact_name} (<span className="font-mono">{item.contact_phone}</span>)
            </span>
          </div>
        </div>
      </div>

      {/* Inline Delete Confirmation or Primary Actions */}
      <div className="pt-4 mt-4 border-t border-paper-divider dark:border-night-divider">
        {confirmingDelete ? (
          <div
            role="region"
            aria-label="Konfirmasi penghapusan laporan"
            className="flex flex-wrap items-center justify-between gap-2 bg-red-50 dark:bg-red-950/60 border border-red-300 dark:border-red-800 rounded-md p-2.5"
          >
            <span className="text-xs font-semibold text-red-700 dark:text-red-300">
              Hapus laporan ini?
            </span>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setConfirmingDelete(false)}
                disabled={busyAction === 'delete'}
                className="min-h-[44px] px-3 py-1.5 text-xs font-semibold rounded-md bg-paper-surface dark:bg-night-elevated text-paper-ink dark:text-night-ink border border-paper-border dark:border-night-border hover:bg-paper-stone dark:hover:bg-night-divider transition-colors"
              >
                Batal
              </button>
              <button
                type="button"
                onClick={handleConfirmDelete}
                disabled={busyAction === 'delete'}
                className="min-h-[44px] px-3 py-1.5 text-xs font-semibold rounded-md bg-red-700 hover:bg-red-800 text-white transition-colors disabled:opacity-50"
              >
                {busyAction === 'delete' ? 'Menghapus...' : 'Ya, Hapus'}
              </button>
            </div>
          </div>
        ) : !isResolved ? (
          <div className="flex flex-wrap items-center gap-2">
            <a
              href={waLink}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 min-h-[44px] inline-flex items-center justify-center px-4 py-2 bg-cobalt hover:bg-cobalt-hover text-white text-xs sm:text-sm font-semibold rounded-md transition-colors text-center"
            >
              Hubungi via WhatsApp
            </a>

            <button
              type="button"
              onClick={handleResolveClick}
              disabled={busyAction === 'resolve'}
              className="min-h-[44px] inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-paper-stone dark:bg-night-elevated hover:bg-paper-divider dark:hover:bg-night-divider text-paper-ink dark:text-night-ink border border-paper-border dark:border-night-border text-xs sm:text-sm font-medium rounded-md transition-colors disabled:opacity-50"
            >
              <Check className="w-4 h-4" aria-hidden="true" />
              <span>{busyAction === 'resolve' ? 'Menyimpan...' : 'Tandai Selesai'}</span>
            </button>
          </div>
        ) : (
          <div className="min-h-[44px] flex items-center justify-center gap-2 text-xs font-semibold text-green-700 dark:text-green-300 bg-green-50 dark:bg-green-950 border border-green-300 dark:border-green-800 rounded-md px-3 py-2">
            <Check className="w-4 h-4" aria-hidden="true" />
            <span>Barang telah dikembalikan</span>
          </div>
        )}
      </div>
    </article>
  );
}
