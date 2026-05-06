export type StockQuote = {
  symbol: string;
  current_price: number;
  open: number | null;
  high: number | null;
  low: number | null;
  previous_close: number | null;
  timestamp: number | null;
};

export type OhlcvBar = {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type StockHistory = {
  symbol: string;
  resolution: string;
  status: string;
  bars: OhlcvBar[];
};

export type RagResponse = {
  response: string;
};

export type RecommendationResponse = {
  user_id: number;
  advice: string[];
};
