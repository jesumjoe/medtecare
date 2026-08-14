"use client";

import React from "react";
import { KPICard } from "@/components/dashboard/kpi-card";
import { RiskTrendChart } from "@/components/dashboard/risk-trend-chart";
import { FleetGrid } from "@/components/dashboard/fleet-grid";
import { AlertsFeed } from "@/components/dashboard/alerts-feed";
import {
  kpiData,
  riskTrendData,
  equipmentList,
  alertsList,
} from "@/lib/mock-data";

export default function DashboardOverview() {
  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">
          Fleet Overview
        </h1>
        <p className="text-sm text-muted-foreground">
          Real-time monitoring across all plants and equipment
        </p>
      </div>

      {/* KPI row */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {kpiData.map((kpi, i) => (
          <KPICard key={kpi.label} data={kpi} index={i} />
        ))}
      </div>

      {/* Main content: chart + alerts */}
      <div className="grid gap-6 lg:grid-cols-3">
        <RiskTrendChart data={riskTrendData} />
        <AlertsFeed alerts={alertsList} />
      </div>

      {/* Fleet grid */}
      <FleetGrid equipment={equipmentList} />
    </div>
  );
}
