"use client";

import React from "react";
import { cn } from "@/lib/utils";
import type { EquipmentStatus, AlertSeverity, TicketPriority } from "@/lib/mock-data";

type BadgeVariant = EquipmentStatus | AlertSeverity | TicketPriority;

interface StatusBadgeProps {
  variant: BadgeVariant;
  children: React.ReactNode;
  className?: string;
  pulse?: boolean;
  size?: "sm" | "md";
}

const variantClasses: Record<string, string> = {
  healthy: "bg-sentinel-healthy/15 text-sentinel-healthy border-sentinel-healthy/30",
  low: "bg-sentinel-healthy/15 text-sentinel-healthy border-sentinel-healthy/30",
  warning: "bg-sentinel-warning/15 text-sentinel-warning border-sentinel-warning/30",
  medium: "bg-sentinel-blue/15 text-sentinel-blue-light border-sentinel-blue/30",
  high: "bg-sentinel-warning/15 text-sentinel-warning border-sentinel-warning/30",
  critical: "bg-sentinel-critical/15 text-sentinel-critical border-sentinel-critical/30",
};

const pulseColors: Record<string, string> = {
  healthy: "bg-sentinel-healthy",
  low: "bg-sentinel-healthy",
  warning: "bg-sentinel-warning",
  medium: "bg-sentinel-blue",
  high: "bg-sentinel-warning",
  critical: "bg-sentinel-critical",
};

export function StatusBadge({
  variant,
  children,
  className,
  pulse = false,
  size = "sm",
}: StatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border font-semibold uppercase tracking-wider",
        size === "sm" ? "px-2.5 py-0.5 text-[0.65rem]" : "px-3 py-1 text-xs",
        variantClasses[variant] || variantClasses.healthy,
        className
      )}
    >
      {pulse && (
        <span className="relative flex h-1.5 w-1.5">
          <span
            className={cn(
              "absolute inline-flex h-full w-full animate-ping rounded-full opacity-75",
              pulseColors[variant]
            )}
          />
          <span
            className={cn(
              "relative inline-flex h-1.5 w-1.5 rounded-full",
              pulseColors[variant]
            )}
          />
        </span>
      )}
      {children}
    </span>
  );
}
