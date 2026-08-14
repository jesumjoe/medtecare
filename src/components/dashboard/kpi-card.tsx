"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { cn } from "@/lib/utils";
import { GlassCard } from "@/components/shared/glass-card";
import type { KPIData } from "@/lib/mock-data";

interface KPICardProps {
  data: KPIData;
  index?: number;
}

function MiniSparkline({ data, className }: { data: number[]; className?: string }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const height = 32;
  const width = 80;
  const points = data
    .map((v, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((v - min) / range) * height;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg
      width={width}
      height={height}
      className={cn("overflow-visible", className)}
      viewBox={`0 0 ${width} ${height}`}
    >
      <defs>
        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="var(--sentinel-blue)" stopOpacity="0.3" />
          <stop offset="100%" stopColor="var(--sentinel-blue)" stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon
        points={`0,${height} ${points} ${width},${height}`}
        fill="url(#sparkGrad)"
      />
      <polyline
        points={points}
        fill="none"
        stroke="var(--sentinel-blue)"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function AnimatedNumber({ value, suffix }: { value: number; suffix?: string }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    const duration = 1500;
    const steps = 60;
    const increment = value / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = Math.min(value, increment * step);
      setDisplay(
        Number.isInteger(value)
          ? Math.round(current)
          : parseFloat(current.toFixed(1))
      );
      if (step >= steps) clearInterval(timer);
    }, duration / steps);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <span>
      {display}
      {suffix}
    </span>
  );
}

export function KPICard({ data, index = 0 }: KPICardProps) {
  const isPositiveChange = data.change > 0;
  const isNeutral = data.change === 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <GlassCard className="relative overflow-hidden">
        {/* Subtle top accent line */}
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sentinel-blue/40 to-transparent" />

        <div className="flex items-start justify-between">
          <div className="space-y-2">
            <p className="eyebrow">{data.label}</p>
            <p className="text-3xl font-bold tracking-tight text-foreground">
              {data.prefix}
              <AnimatedNumber value={data.value} suffix={data.suffix} />
            </p>
            <div className="flex items-center gap-1.5">
              {isNeutral ? (
                <Minus className="h-3.5 w-3.5 text-muted-foreground" />
              ) : isPositiveChange ? (
                <TrendingUp className="h-3.5 w-3.5 text-sentinel-warning" />
              ) : (
                <TrendingDown className="h-3.5 w-3.5 text-sentinel-healthy" />
              )}
              <span
                className={cn(
                  "text-xs font-medium",
                  isNeutral
                    ? "text-muted-foreground"
                    : isPositiveChange
                    ? "text-sentinel-warning"
                    : "text-sentinel-healthy"
                )}
              >
                {isPositiveChange ? "+" : ""}
                {data.change}% {data.changeLabel}
              </span>
            </div>
          </div>

          <MiniSparkline data={data.sparkline} className="mt-2 opacity-60" />
        </div>
      </GlassCard>
    </motion.div>
  );
}
