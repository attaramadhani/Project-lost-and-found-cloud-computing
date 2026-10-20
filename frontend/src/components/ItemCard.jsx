import React from 'react';
import { MapPin, Calendar, Phone, CheckCircle, Trash2, ArrowUpRight } from 'lucide-react';

export default function ItemCard({ item, onResolve, onDelete }) {
  const isLost = item.type === 'lost';
  const isResolved = item.status === 'resolved';

  const formatWaNumber = (phone) => {
    let clean = phone.replace(/[^0-9]/g, '');
    if (clean.startsWith('0')) {
      clean = '62' + clean.slice(1);
    }
    return clean;
  };

  const waLink = `https://wa.me/${formatWaNumber(item.contact_phone)}?text=${encodeURIComponent(
    `Halo ${item.contact_name}, saya melihat informasi terkait "${item.title}" di portal Campus Lost & Found...`
  )}`;

  return (
    <div
      className={`bg-white rounded-2xl border transition-all p-5 flex flex-col justify-between shadow-sm hover:shadow-md ${
        isResolved
          ? 'border-slate-200 opacity-75 bg-slate-50/50'
          : isLost
          ? 'border-rose-100 hover:border-rose-300'
          : 'border-emerald-100 hover:border-emerald-300'
      }`}
    >
      <div>
        {/* Top Badges */}
        <div className="flex items-center justify-between mb-3 gap-2">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span
              className={`text-xs font-semibold px-2.5 py-1 rounded-full uppercase tracking-wider ${
                isResolved
                  ? 'bg-slate-200 text-slate-700'
                  : isLost
                  ? 'bg-rose-100 text-rose-700'
                  : 'bg-emerald-100 text-emerald-700'
              }`}
            >
              {isResolved ? 'Selesai' : isLost ? 'Hilang' : 'Ditemukan'}
            </span>

            <span className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full">
              {item.category}
            </span>
          </div>

          <button
            onClick={() => onDelete(item.id)}
            title="Hapus laporan"
            className="text-slate-400 hover:text-rose-600 p-1 rounded-lg transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>

        {/* Title & Description */}
        <h3 className={`font-bold text-base text-slate-900 mb-2 leading-snug ${isResolved ? 'line-through text-slate-500' : ''}`}>
          {item.title}
        </h3>
        <p className="text-sm text-slate-600 mb-4 line-clamp-3 leading-relaxed">
          {item.description}
        </p>

        {/* Meta Info */}
        <div className="space-y-1.5 text-xs text-slate-500 mb-4">
          <div className="flex items-center gap-2">
            <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span className="truncate font-medium text-slate-700">{item.location}</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span>Kejadian: {new Date(item.date_event).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>
          <div className="flex items-center gap-2">
            <Phone className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span>Kontak: {item.contact_name} ({item.contact_phone})</span>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="pt-3 border-t border-slate-100 flex items-center gap-2">
        {!isResolved ? (
          <>
            <a
              href={waLink}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl transition-colors shadow-sm"
            >
              <span>Hubungi via WA</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </a>

            <button
              onClick={() => onResolve(item.id)}
              className="inline-flex items-center gap-1 px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-xl transition-colors"
              title="Tandai sudah selesai / kembali"
            >
              <CheckCircle className="w-3.5 h-3.5 text-slate-500" />
              <span>Selesai</span>
            </button>
          </>
        ) : (
          <div className="w-full text-center py-1.5 text-xs text-emerald-700 font-medium bg-emerald-50 rounded-xl">
            ✓ Barang telah dikembalikan
          </div>
        )}
      </div>
    </div>
  );
}
