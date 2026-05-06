import type {
  RagResponse,
  RecommendationResponse,
  StockHistory,
  StockQuote,
} from "./types";

function apiBase(): string {
  const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
  return base.replace(/\/$/, "");
}

function apiV1Base(): string {
  return `${apiBase()}/api/v1`;
}

async function parseJson<T>(res: Response): Promise<T> {
  const text = await res.text();
  if (!text) {
    throw new Error(`Empty response (${res.status})`);
  }
  try {
    return JSON.parse(text) as T;
  } catch {
    throw new Error(text.slice(0, 200) || `Invalid JSON (${res.status})`);
  }
}

export async function getStockQuote(ticker: string): Promise<StockQuote> {
  const res = await fetch(
    `${apiV1Base()}/stocks/${encodeURIComponent(ticker.trim())}/quote`,
    { cache: "no-store" },
  );
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `Quote failed (${res.status})`);
  }
  return parseJson<StockQuote>(res);
}

export async function getStockHistory(
  ticker: string,
  days = 90,
): Promise<StockHistory> {
  const q = new URLSearchParams({ days: String(days), resolution: "D" });
  const res = await fetch(
    `${apiV1Base()}/stocks/${encodeURIComponent(ticker.trim())}/history?${q}`,
    { cache: "no-store" },
  );
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `History failed (${res.status})`);
  }
  return parseJson<StockHistory>(res);
}

export async function getRagAnswer(query: string): Promise<RagResponse> {
  const q = new URLSearchParams({ q: query });
  const res = await fetch(`${apiV1Base()}/rag?${q}`, { cache: "no-store" });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `RAG failed (${res.status})`);
  }
  return parseJson<RagResponse>(res);
}

export async function postRecommendation(
  userId: number,
): Promise<RecommendationResponse> {
  const q = new URLSearchParams({ user_id: String(userId) });
  const res = await fetch(`${apiV1Base()}/ai/recommendation?${q}`, {
    method: "POST",
    cache: "no-store",
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `Recommendation failed (${res.status})`);
  }
  return parseJson<RecommendationResponse>(res);
}
