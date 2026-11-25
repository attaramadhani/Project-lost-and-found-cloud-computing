import React from 'react';
import { Activity, CheckCircle2, AlertCircle } from 'lucide-react';

export default function FooterInspector({ serverMeta, pingHistory, onPing, pinging, healthError }) {
  const isConnected = Boolean(serverMeta?.served_by) && !healthError;
  const isMysql = serverMeta?.database?.mode === 'mysql-connected';

  return (
    <footer
      id="cloud-inspector"
      className="mt-14 bg-paper-stone dark:bg-night-surface border-t border-paper-divider dark:border-night-divider py-8 px-4 sm:px-6 lg:px-8"
    >
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left: Monitor Header + Live Ping Control + Real Ping History */}
          <div className="lg:col-span-5 space-y-4">
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <div>
                <p className="text-xs font-mono uppercase tracking-wider text-paper-slate dark:text-night-slate font-semibold">
                  Cloud Architecture Inspector
                </p>
                <h2 className="font-display text-lg font-bold text-paper-ink dark:text-night-ink mt-0.5">
                  Monitor Node &amp; Load Balancer
                </h2>
              </div>

              <span
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm text-xs font-semibold border ${
                  isConnected
                    ? 'bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 border-green-300 dark:border-green-800'
                    : 'bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300 border-red-300 dark:border-red-800'
                }`}
              >
                {isConnected ? (
                  <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
                ) : (
                  <AlertCircle className="w-3.5 h-3.5" aria-hidden="true" />
                )}
                <span>{pinging ? 'Memeriksa...' : isConnected ? 'Backend Terhubung' : 'Tidak Terjangkau'}</span>
              </span>
            </div>

            <button
              type="button"
              onClick={onPing}
              disabled={pinging}
              className="min-h-[44px] inline-flex items-center gap-2 px-4 py-2 bg-paper-surface dark:bg-night-elevated hover:bg-paper-bg dark:hover:bg-night-divider text-paper-ink dark:text-night-ink border border-paper-border dark:border-night-border text-sm font-semibold rounded-md transition-colors disabled:opacity-50"
            >
              <Activity
                className={`w-4 h-4 text-cobalt dark:text-cobalt-light ${pinging ? 'motion-safe:animate-spin' : ''}`}
                aria-hidden="true"
              />
              <span>{pinging ? 'Mengirim Ping...' : 'Tes Ping Load Balancer'}</span>
            </button>

            {pingHistory.length > 0 && (
              <div className="bg-paper-surface dark:bg-night-bg border border-paper-divider dark:border-night-divider rounded-md p-3">
                <p className="text-xs font-semibold text-paper-ink dark:text-night-ink mb-2">
                  Riwayat Ping Sesi Ini ({pingHistory.length} respons)
                </p>
                <ol className="space-y-1 text-xs font-mono">
                  {pingHistory.map((entry) => (
                    <li
                      key={entry.seq}
                      className="flex items-center justify-between gap-2 text-paper-slate dark:text-night-slate"
                    >
                      <span>#{String(entry.seq).padStart(2, '0')} · {entry.time}</span>
                      <span className="font-semibold text-cobalt dark:text-cobalt-light">
                        {entry.node}
                      </span>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>

          {/* Right: 4-Row Architectural Specification Table */}
          <div className="lg:col-span-7 bg-paper-surface dark:bg-night-bg border border-paper-divider dark:border-night-divider rounded-md overflow-hidden">
            <dl className="divide-y divide-paper-divider dark:divide-night-divider text-sm">
              <div className="px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                <dt className="text-xs font-semibold text-paper-slate dark:text-night-slate">
                  Backend Instance Aktif (VM 2)
                </dt>
                <dd className="font-mono font-bold text-cobalt dark:text-cobalt-light">
                  {serverMeta?.served_by || (healthError ? 'Tidak merespons' : 'Memuat...')}
                </dd>
              </div>

              <div className="px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                <dt className="text-xs font-semibold text-paper-slate dark:text-night-slate">
                  Container Hostname
                </dt>
                <dd className="font-mono text-paper-ink dark:text-night-ink">
                  {serverMeta?.hostname || '-'}
                </dd>
              </div>

              <div className="px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                <dt className="text-xs font-semibold text-paper-slate dark:text-night-slate">
                  Database Layer (VM 3)
                </dt>
                <dd className="font-mono text-paper-ink dark:text-night-ink">
                  {serverMeta
                    ? isMysql
                      ? `MySQL Container Connected (${serverMeta.database?.host || 'VM3'})`
                      : 'In-Memory Fallback (Mode Lokal)'
                    : '-'}
                </dd>
              </div>

              <div className="px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                <dt className="text-xs font-semibold text-paper-slate dark:text-night-slate">
                  Reverse Proxy / Routing
                </dt>
                <dd className="font-mono text-paper-ink dark:text-night-ink">
                  Nginx Round-Robin · /api/health
                </dd>
              </div>
            </dl>
          </div>
        </div>

        <div className="pt-4 border-t border-paper-divider dark:border-night-divider flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-xs text-paper-slate dark:text-night-slate">
          <p>
            Final Project Cloud Computing · S1 Sistem Informasi · Universitas Trunojoyo Madura
          </p>
          <p className="font-mono">
            3-Tier Architecture (VM1 SPA · VM2 LB+API · VM3 MySQL)
          </p>
        </div>
      </div>
    </footer>
  );
}
