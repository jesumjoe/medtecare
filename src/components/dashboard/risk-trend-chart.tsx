"use client";

import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { GlassCard } from "@/components/shared/glass-card";
import type { RiskDataPoint } from "@/lib/mock-data";

interface RiskTrendChartProps {
  data: RiskDataPoint[];
}

function CustomTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number; dataKey: string; color: string }>; label?: string }) {
  if (!active || !payload) return null;

  return (
    <div className="rounded-lg border border-sentinel-glass-border bg-sentinel-bg-to/95 px-4 py-3 shadow-xl backdrop-blur-xl">
      <p className="mb-2 text-xs font-medium text-muted-foreground">{label}</p>
      {payload.map((entry) => (
        <div key={entry.dataKey} className="flex items-center gap-2 text-sm">
          <div
            className="h-2 w-2 rounded-full"
            style={{ background: entry.color }}
          />
          <span className="text-muted-foreground capitalize">{entry.dataKey}:</span>
          <span className="font-semibold text-foreground">{entry.value}</span>
        </div>
      ))}
    </div>
  );
}

export function RiskTrendChart({ data }: RiskTrendChartProps) {
  return (
    <GlassCard hover={false} className="col-span-full lg:col-span-2">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-base font-semibold text-foreground">Risk Trend</h3>
          <p className="text-xs text-muted-foreground">Fleet average risk score — 30 day window</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <div className="h-2 w-2 rounded-full bg-sentinel-blue" />
            <span className="text-xs text-muted-foreground">Actual</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="h-2 w-2 rounded-full bg-sentinel-warning" />
            <span className="text-xs text-muted-foreground">Predicted</span>
          </div>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="riskActual" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="riskPredicted" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.05)"
              vertical={false}
            />
            <XAxis
              dataKey="date"
              tick={{ fill: "#94A3B8", fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v: string) => {
                const d = new Date(v);
                return `${d.getMonth() + 1}/${d.getDate()}`;
              }}
            />
            <YAxis
              tick={{ fill: "#94A3B8", fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              domain={[0, 100]}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="score"
              stroke="#3B82F6"
              strokeWidth={2}
              fill="url(#riskActual)"
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0, fill: "#3B82F6" }}
            />
            <Area
              type="monotone"
              dataKey="predicted"
              stroke="#F59E0B"
              strokeWidth={2}
              strokeDasharray="6 3"
              fill="url(#riskPredicted)"
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0, fill: "#F59E0B" }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </GlassCard>
  );
}
