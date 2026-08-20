"use client";

import React from "react";
import { motion } from "framer-motion";
import { AlertTriangle, UserPlus, Clock } from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";
import { StatusBadge } from "@/components/shared/status-badge";
import type { Alert } from "@/lib/mock-data";
import { formatRelativeTime } from "@/lib/mock-data";

interface AlertsFeedProps {
  alerts: Alert[];
  maxItems?: number;
}

export function AlertsFeed({ alerts, maxItems = 8 }: AlertsFeedProps) {
  const sorted = [...alerts]
    .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
    .slice(0, maxItems);

  return (
    <GlassCard hover={false} padding="lg">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-sentinel-warning" />
          <h3 className="text-base font-semibold text-foreground">Recent Alerts</h3>
        </div>
        <span className="text-xs text-muted-foreground">
          {alerts.filter((a) => a.status === "open").length} open
        </span>
      </div>

      <div className="space-y-2">
        {sorted.map((alert, i) => (
          <motion.div
            key={alert.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
            className="group flex items-start gap-3 rounded-lg border border-transparent p-3 transition-all duration-200 hover:border-sentinel-glass-border hover:bg-sentinel-glass"
          >
            {/* Severity dot */}
            <div className="mt-1.5 flex-shrink-0">
              <div
                className="h-2 w-2 rounded-full"
                style={{
                  background:
                    alert.severity === "critical"
                      ? "var(--sentinel-critical)"
                      : alert.severity === "high"
                      ? "var(--sentinel-warning)"
                      : alert.severity === "medium"
                      ? "var(--sentinel-blue)"
                      : "var(--sentinel-healthy)",
                  boxShadow:
                    alert.severity === "critical"
                      ? "0 0 8px var(--sentinel-critical)"
                      : "none",
                }}
              />
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-medium text-foreground truncate">
                  {alert.equipmentName}
                </span>
                <StatusBadge variant={alert.severity}>
                  {alert.severity}
                </StatusBadge>
              </div>
              <p className="text-xs text-muted-foreground line-clamp-1">
                {alert.riskDriver}
              </p>
              <div className="mt-1.5 flex items-center gap-3">
                <span suppressHydrationWarning className="flex items-center gap-1 text-[0.65rem] text-muted-foreground">
                  <Clock className="h-3 w-3" />
                  {formatRelativeTime(alert.timestamp)}
                </span>
                {alert.assignedTo && (
                  <span className="text-[0.65rem] text-sentinel-blue-light">
                    → {alert.assignedTo}
                  </span>
                )}
              </div>
            </div>

            {!alert.assignedTo && (
              <button
                type="button"
                className="flex-shrink-0 rounded-md border border-sentinel-glass-border p-1.5 text-muted-foreground opacity-0 transition-all hover:border-sentinel-blue/30 hover:text-sentinel-blue-light group-hover:opacity-100"
                title="Assign Technician"
              >
                <UserPlus className="h-3.5 w-3.5" />
              </button>
            )}
          </motion.div>
        ))}
      </div>
    </GlassCard>
  );
}
