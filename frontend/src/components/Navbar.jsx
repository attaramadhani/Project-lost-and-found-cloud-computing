import React from 'react';
import { Plus, RefreshCw, Sun, Moon } from 'lucide-react';

export default function Navbar({ onOpenModal, onRefresh, loading, theme, onToggleTheme }) {
  const isDark = theme === 'dark';

  return (
    <header className="sticky top-0 z-30 bg-paper-surface dark:bg-night-surface border-b border-paper-divider dark:border-night-divider">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          {/* Custom 3-Tier geometric identity mark representing Presentation / App / Data tiers */}
          <div className="w-10 h-10 shrink-0 rounded-md bg-paper-ink dark:bg-night-elevated border border-paper-divider dark:border-night-divider flex items-center justify-center">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              aria-hidden="true"
              className="text-white"
            >
              <rect x="3" y="4" width="18" height="4" rx="1" fill="currentColor" opacity="0.7" />
              <rect x="3" y="10" width="18" height="4" rx="1" fill="#60A5FA" />
              <rect x="3" y="16" width="18" height="4" rx="1" fill="currentColor" opacity="0.7" />
            </svg>
          </div>
          <div className="min-w-0">
            <p className="font-display text-base sm:text-lg font-bold tracking-tight text-paper-ink dark:text-night-ink leading-tight truncate">
              Campus Lost &amp; Found
            </p>
            <p className="text-xs text-paper-slate dark:text-night-slate hidden sm:block">
              SI UTM · Portal Barang Kampus
            </p>
          </div>
        </div>

        <nav aria-label="Navigasi utama" className="hidden md:flex items-center gap-1">
          <a
            href="#daftar-laporan"
            className="min-h-[44px] px-3 inline-flex items-center text-sm font-medium text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink hover:bg-paper-stone dark:hover:bg-night-elevated rounded-md transition-colors"
          >
            Daftar Laporan
          </a>
          <a
            href="#cloud-inspector"
            className="min-h-[44px] px-3 inline-flex items-center text-sm font-medium text-paper-slate dark:text-night-slate hover:text-paper-ink dark:hover:text-night-ink hover:bg-paper-stone dark:hover:bg-night-elevated rounded-md transition-colors"
          >
            Monitor Node
          </a>
        </nav>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onToggleTheme}
            aria-pressed={isDark}
            aria-label={isDark ? 'Ganti ke mode terang' : 'Ganti ke mode gelap'}
            title={isDark ? 'Mode Terang' : 'Mode Gelap'}
            className="min-h-[44px] min-w-[44px] inline-flex items-center justify-center rounded-md border border-paper-border dark:border-night-border text-paper-ink dark:text-night-ink bg-paper-surface dark:bg-night-elevated hover:bg-paper-stone dark:hover:bg-night-divider transition-colors"
          >
            {isDark ? (
              <Sun className="w-4 h-4" aria-hidden="true" />
            ) : (
              <Moon className="w-4 h-4" aria-hidden="true" />
            )}
          </button>

          <button
            type="button"
            onClick={onRefresh}
            disabled={loading}
            aria-label="Muat ulang daftar laporan"
            title="Muat ulang data"
            className="min-h-[44px] min-w-[44px] inline-flex items-center justify-center rounded-md border border-paper-border dark:border-night-border text-paper-ink dark:text-night-ink bg-paper-surface dark:bg-night-elevated hover:bg-paper-stone dark:hover:bg-night-divider transition-colors disabled:opacity-50"
          >
            <RefreshCw
              className={`w-4 h-4 ${loading ? 'motion-safe:animate-spin text-cobalt dark:text-cobalt-light' : ''}`}
              aria-hidden="true"
            />
          </button>

          <button
            type="button"
            onClick={onOpenModal}
            className="min-h-[44px] inline-flex items-center gap-2 px-4 py-2 bg-cobalt hover:bg-cobalt-hover active:bg-blue-900 text-white text-sm font-semibold rounded-md transition-colors"
          >
            <Plus className="w-4 h-4" aria-hidden="true" />
            <span>Buat Laporan</span>
          </button>
        </div>
      </div>
    </header>
  );
}
