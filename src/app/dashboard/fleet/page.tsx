"use client";

import { GlassCard } from "@/components/shared/glass-card";
import { Server } from "lucide-react";
import { FleetGrid } from "@/components/dashboard/fleet-grid";
import { equipmentList } from "@/lib/mock-data";

export default function FleetPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Fleet</h1>
        <p className="text-sm text-muted-foreground">
          All monitored equipment across your plants
        </p>
      </div>
      <FleetGrid equipment={equipmentList} />
    </div>
  );
}
