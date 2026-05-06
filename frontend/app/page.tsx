"use client";

import dynamic from "next/dynamic";
import { useCallback, useMemo, useState, type ReactNode } from "react";
import {
  getRagAnswer,
  getStockHistory,
  getStockQuote,
  postRecommendation,
} from "@/lib/api";
import type { StockHistory, StockQuote } from "@/lib/types";

const PriceChart = dynamic(
  () => import("@/components/PriceChart").then((m) => m.PriceChart),
  { ssr: false, loading: () => chartSkeleton },
);

const chartSkeleton = (
  <div className="flex h-72 items-center justify-center rounded-lg border border-dashed border-surface-border bg-surface-raised/40 text-sm text-gray-500">
    Loading chart…
  </div>
);

function formatMoney(n: number | null | undefined): string {
  if (n == null || Number.isNaN(n)) return "—";
  return n.toLocaleString(undefined, {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  });
}

export default function Home() {
  const [ticker, setTicker] = useState("AAPL");
  const [historyDays, setHistoryDays] = useState(90);
  const [quote, setQuote] = useState<StockQuote | null>(null);
  const [history, setHistory] = useState<StockHistory | null>(null);
  const [quoteLoading, setQuoteLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [marketError, setMarketError] = useState<string | null>(null);

  const [ragQuery, setRagQuery] = useState("What drives Apple margin trends?");
  const [ragResult, setRagResult] = useState<string | null>(null);
  const [ragLoading, setRagLoading] = useState(false);
  const [ragError, setRagError] = useState<string | null>(null);

  const [userId, setUserId] = useState(1);
  const [advice, setAdvice] = useState<string[] | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  const apiHint = useMemo(
    () => process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000",
    [],
  );

  const loadMarket = useCallback(async () => {
    const sym = ticker.trim().toUpperCase();
    if (!sym) {
      setMarketError("Enter a ticker symbol.");
      return;
    }
    setMarketError(null);
    setQuoteLoading(true);
    setHistoryLoading(true);
    setQuote(null);
    setHistory(null);
    try {
      const [q, h] = await Promise.all([
        getStockQuote(sym),
        getStockHistory(sym, historyDays),
      ]);
      setQuote(q);
      setHistory(h);
    } catch (e) {
      setMarketError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setQuoteLoading(false);
      setHistoryLoading(false);
    }
  }, [ticker, historyDays]);

  const runRag = useCallback(async () => {
    const q = ragQuery.trim();
    if (!q) {
      setRagError("Enter a question.");
      return;
    }
    setRagError(null);
    setRagLoading(true);
    setRagResult(null);
    try {
      const data = await getRagAnswer(q);
      setRagResult(data.response);
    } catch (e) {
      setRagError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setRagLoading(false);
    }
  }, [ragQuery]);

  const runAi = useCallback(async () => {
    setAiError(null);
    setAiLoading(true);
    setAdvice(null);
    try {
      const data = await postRecommendation(userId);
      setAdvice(data.advice);
    } catch (e) {
      setAiError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setAiLoading(false);
    }
  }, [userId]);

  return (
    <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-10 px-4 py-10 sm:px-6 lg:px-8">
      <header className="flex flex-col gap-3 border-b border-surface-border pb-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-accent">
            FinAdvisor
          </p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Market desk
          </h1>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-gray-400">
            Next.js UI wired to your FastAPI service: live quotes and history
            from Finnhub, the RAG endpoint, and CrewAI recommendations.
          </p>
        </div>
        <div className="rounded-lg border border-surface-border bg-surface-raised/50 px-4 py-3 text-xs text-gray-400">
          <span className="text-gray-500">API base</span>
          <p className="mt-1 font-mono text-gray-200">{apiHint}</p>
        </div>
      </header>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6 rounded-2xl border border-surface-border bg-surface-raised/40 p-6 shadow-xl shadow-black/20 backdrop-blur">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-lg font-medium text-white">Equities</h2>
              <p className="text-sm text-gray-400">
                Quote and daily closes for the symbol you choose.
              </p>
            </div>
            <div className="flex flex-wrap items-end gap-3">
              <label className="flex flex-col gap-1 text-xs text-gray-500">
                Ticker
                <input
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  className="w-28 rounded-md border border-surface-border bg-surface px-3 py-2 text-sm text-white outline-none ring-accent/40 focus:ring-2"
                  placeholder="AAPL"
                  spellCheck={false}
                />
              </label>
              <label className="flex flex-col gap-1 text-xs text-gray-500">
                History (days)
                <input
                  type="number"
                  min={1}
                  max={3650}
                  value={historyDays}
                  onChange={(e) =>
                    setHistoryDays(Number(e.target.value) || 30)
                  }
                  className="w-24 rounded-md border border-surface-border bg-surface px-3 py-2 text-sm text-white outline-none ring-accent/40 focus:ring-2"
                />
              </label>
              <button
                type="button"
                onClick={() => void loadMarket()}
                disabled={quoteLoading || historyLoading}
                className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-surface transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {quoteLoading || historyLoading ? "Loading…" : "Load"}
              </button>
            </div>
          </div>

          {marketError && (
            <p className="rounded-md border border-red-900/60 bg-red-950/40 px-3 py-2 text-sm text-red-200">
              {marketError}
            </p>
          )}

          {quote && (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <Stat label="Last" value={formatMoney(quote.current_price)} />
              <Stat label="Open" value={formatMoney(quote.open)} />
              <Stat label="Day range" value={rangeLabel(quote.low, quote.high)} />
              <Stat
                label="Prev close"
                value={formatMoney(quote.previous_close)}
              />
            </div>
          )}

          {historyLoading ? chartSkeleton : history && <PriceChart bars={history.bars} />}
        </div>

        <div className="space-y-6">
          <Panel title="RAG" subtitle="GET /api/v1/rag">
            <textarea
              value={ragQuery}
              onChange={(e) => setRagQuery(e.target.value)}
              rows={4}
              className="w-full resize-none rounded-md border border-surface-border bg-surface px-3 py-2 text-sm text-white outline-none ring-accent/40 focus:ring-2"
            />
            {ragError && (
              <p className="text-xs text-red-300">{ragError}</p>
            )}
            <button
              type="button"
              onClick={() => void runRag()}
              disabled={ragLoading}
              className="w-full rounded-md border border-surface-border bg-surface-raised px-3 py-2 text-sm font-medium text-white transition hover:border-accent/50 hover:text-accent disabled:opacity-50"
            >
              {ragLoading ? "Running…" : "Run query"}
            </button>
            {ragResult != null && (
              <p className="rounded-md border border-surface-border bg-surface/80 p-3 text-sm leading-relaxed text-gray-200">
                {ragResult}
              </p>
            )}
          </Panel>

          <Panel
            title="AI recommendation"
            subtitle="POST /api/v1/ai/recommendation"
          >
            <label className="flex flex-col gap-1 text-xs text-gray-500">
              User id
              <input
                type="number"
                min={1}
                value={userId}
                onChange={(e) => setUserId(Number(e.target.value) || 1)}
                className="rounded-md border border-surface-border bg-surface px-3 py-2 text-sm text-white outline-none ring-accent/40 focus:ring-2"
              />
            </label>
            {aiError && <p className="text-xs text-red-300">{aiError}</p>}
            <button
              type="button"
              onClick={() => void runAi()}
              disabled={aiLoading}
              className="w-full rounded-md border border-surface-border bg-surface-raised px-3 py-2 text-sm font-medium text-white transition hover:border-accent/50 hover:text-accent disabled:opacity-50"
            >
              {aiLoading ? "Generating…" : "Get advice"}
            </button>
            {advice && advice.length > 0 && (
              <ul className="list-inside list-disc space-y-1 text-sm text-gray-200">
                {advice.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            )}
          </Panel>
        </div>
      </section>

      <footer className="border-t border-surface-border pt-6 text-center text-xs text-gray-500">
        Copy `.env.example` to `.env.local` and point{" "}
        <code className="text-gray-400">NEXT_PUBLIC_API_URL</code> at your API.
      </footer>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-surface-border bg-surface/60 px-4 py-3">
      <p className="text-xs uppercase tracking-wide text-gray-500">{label}</p>
      <p className="mt-1 text-lg font-semibold text-white">{value}</p>
    </div>
  );
}

function Panel({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-surface-border bg-surface-raised/40 p-5 shadow-lg shadow-black/15 backdrop-blur">
      <div className="mb-4">
        <h2 className="text-lg font-medium text-white">{title}</h2>
        <p className="font-mono text-xs text-gray-500">{subtitle}</p>
      </div>
      <div className="space-y-3">{children}</div>
    </div>
  );
}

function rangeLabel(low: number | null, high: number | null): string {
  if (low == null || high == null) return "—";
  return `${formatMoney(low)} – ${formatMoney(high)}`;
}
