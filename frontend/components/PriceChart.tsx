"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { OhlcvBar } from "@/lib/types";

type Point = { label: string; close: number };

function toChartData(bars: OhlcvBar[]): Point[] {
  return bars.map((b) => ({
    label: new Date(b.time * 1000).toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    }),
    close: b.close,
  }));
}

export function PriceChart({ bars }: { bars: OhlcvBar[] }) {
  const data = toChartData(bars);
  if (data.length === 0) {
    return (
      <p className="rounded-lg border border-surface-border bg-surface-raised/60 px-4 py-8 text-center text-sm text-gray-400">
        No candle data returned for this range.
      </p>
    );
  }

  return (
    <div className="h-72 w-full min-w-0">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis
            dataKey="label"
            tick={{ fill: "#9ca3af", fontSize: 11 }}
            interval="preserveStartEnd"
            minTickGap={24}
          />
          <YAxis
            domain={["auto", "auto"]}
            tick={{ fill: "#9ca3af", fontSize: 11 }}
            width={56}
            tickFormatter={(v) =>
              typeof v === "number" ? v.toFixed(2) : String(v)
            }
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#111827",
              border: "1px solid #374151",
              borderRadius: "8px",
            }}
            labelStyle={{ color: "#e5e7eb" }}
            formatter={(value) => [
              typeof value === "number" ? value.toFixed(2) : value,
              "Close",
            ]}
          />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#22d3ee"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
