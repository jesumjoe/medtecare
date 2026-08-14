"use client";

import { GlassCard } from "@/components/shared/glass-card";
import { FileBarChart } from "lucide-react";

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Reports</h1>
        <p className="text-sm text-muted-foreground">
          Generated maintenance reports and analytics exports
        </p>
      </div>
      <GlassCard className="flex flex-col items-center justify-center py-20 text-center">
        <FileBarChart className="h-12 w-12 text-muted-foreground/30 mb-4" />
        <h3 className="text-lg font-semibold text-foreground mb-2">Reports Dashboard</h3>
        <p className="text-sm text-muted-foreground max-w-sm">
          Report generation and export functionality will be wired to the backend analytics pipeline.
        </p>
      </GlassCard>
    </div>
  );
}
