"use client";

import React from "react";
import { motion } from "framer-motion";
import { MapPin, Clock } from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";
import { StatusBadge } from "@/components/shared/status-badge";
import { ConfidenceRing } from "@/components/shared/risk-gauge";
import type { Equipment } from "@/lib/mock-data";
import { formatRelativeTime } from "@/lib/mock-data";

interface EquipmentCardProps {
  equipment: Equipment;
  index?: number;
}

export function EquipmentCard({ equipment, index = 0 }: EquipmentCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.06 }}
    >
      <GlassCard className="relative overflow-hidden">
        {/* Risk score accent bar */}
        <div
          className="absolute top-0 left-0 h-full w-1 rounded-l-xl"
          style={{
            background:
              equipment.status === "critical"
                ? "var(--sentinel-critical)"
                : equipment.status === "warning"
                ? "var(--sentinel-warning)"
                : "var(--sentinel-healthy)",
          }}
        />

        <div className="flex items-start justify-between pl-2">
          <div className="min-w-0 flex-1 space-y-2">
            <div className="flex items-center gap-2">
              <h4 className="truncate text-sm font-semibold text-foreground">
                {equipment.name}
              </h4>
              <StatusBadge variant={equipment.status} pulse={equipment.status === "critical"}>
                {equipment.status}
              </StatusBadge>
            </div>

            <p className="text-xs text-muted-foreground">{equipment.type}</p>

            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <span className="flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                {equipment.location}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {formatRelativeTime(equipment.lastUpdated)}
              </span>
            </div>
          </div>

          <div className="flex flex-col items-center gap-1 ml-3">
            <ConfidenceRing percent={equipment.confidencePercent} />
            <span className="text-[0.55rem] text-muted-foreground">Confidence</span>
          </div>
        </div>
      </GlassCard>
    </motion.div>
  );
}

interface FleetGridProps {
  equipment: Equipment[];
}

export function FleetGrid({ equipment }: FleetGridProps) {
  return (
    <GlassCard hover={false} padding="lg">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-base font-semibold text-foreground">Fleet Risk Map</h3>
          <p className="text-xs text-muted-foreground">
            {equipment.length} monitored assets
          </p>
        </div>
        <div className="flex items-center gap-3">
          {(["critical", "warning", "healthy"] as const).map((status) => (
            <div key={status} className="flex items-center gap-1.5">
              <div
                className="h-2 w-2 rounded-full"
                style={{
                  background:
                    status === "critical"
                      ? "var(--sentinel-critical)"
                      : status === "warning"
                      ? "var(--sentinel-warning)"
                      : "var(--sentinel-healthy)",
                }}
              />
              <span className="text-xs capitalize text-muted-foreground">{status}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {equipment.map((eq, i) => (
          <EquipmentCard key={eq.id} equipment={eq} index={i} />
        ))}
      </div>
    </GlassCard>
  );
}
