"use client";

import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface RiskGaugeProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
  showLabel?: boolean;
  animate?: boolean;
}

function getScoreColor(score: number): string {
  if (score >= 70) return "var(--sentinel-critical)";
  if (score >= 40) return "var(--sentinel-warning)";
  return "var(--sentinel-healthy)";
}

function getScoreLabel(score: number): string {
  if (score >= 70) return "Critical";
  if (score >= 40) return "Warning";
  return "Healthy";
}

export function RiskGauge({
  score,
  size = 160,
  strokeWidth = 10,
  className,
  showLabel = true,
  animate = true,
}: RiskGaugeProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
  const color = getScoreColor(score);

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      <svg width={size} height={size} className="-rotate-90">
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={strokeWidth}
        />
        {/* Progress arc */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={animate ? { strokeDashoffset: circumference } : { strokeDashoffset: circumference - progress }}
          animate={{ strokeDashoffset: circumference - progress }}
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
          style={{
            filter: `drop-shadow(0 0 8px ${color})`,
          }}
        />
      </svg>
      {/* Center text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          className="text-3xl font-bold tracking-tight"
          style={{ color }}
          initial={animate ? { opacity: 0 } : { opacity: 1 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          {score}
        </motion.span>
        {showLabel && (
          <span className="text-[0.65rem] font-semibold uppercase tracking-widest text-muted-foreground mt-1">
            {getScoreLabel(score)}
          </span>
        )}
      </div>
    </div>
  );
}

/* Small inline confidence ring */
interface ConfidenceRingProps {
  percent: number;
  size?: number;
  className?: string;
}

export function ConfidenceRing({ percent, size = 36, className }: ConfidenceRingProps) {
  const sw = 3;
  const r = (size - sw) / 2;
  const c = 2 * Math.PI * r;
  const p = (percent / 100) * c;

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={sw} />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="var(--sentinel-blue)"
          strokeWidth={sw}
          strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: c - p }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.5 }}
        />
      </svg>
      <span className="absolute text-[0.6rem] font-bold text-sentinel-blue-light">
        {percent}%
      </span>
    </div>
  );
}
