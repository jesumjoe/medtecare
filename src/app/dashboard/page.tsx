"use client";

import React, { useState, useEffect } from "react";
import { KPICard } from "@/components/dashboard/kpi-card";
import { RiskTrendChart } from "@/components/dashboard/risk-trend-chart";
import { FleetGrid } from "@/components/dashboard/fleet-grid";
import { AlertsFeed } from "@/components/dashboard/alerts-feed";
import {
  kpiData as mockKpiData,
  riskTrendData as mockRiskTrendData,
  equipmentList as mockEquipmentList,
  alertsList as mockAlertsList,
} from "@/lib/mock-data";
import type { Equipment, Alert, KPIData, RiskDataPoint } from "@/lib/mock-data";
import { fetchDevices, fetchStats, fetchAlerts, fetchRiskTrend } from "@/lib/api";

export default function DashboardOverview() {
  const [kpiData, setKpiData] = useState<KPIData[]>(mockKpiData);
  const [riskTrendData, setRiskTrendData] = useState<RiskDataPoint[]>(mockRiskTrendData);
  const [equipmentList, setEquipmentList] = useState<Equipment[]>(mockEquipmentList);
  const [alertsList, setAlertsList] = useState<Alert[]>(mockAlertsList);

  useEffect(() => {
    // Fetch all dashboard data from backend in parallel
    Promise.allSettled([
      fetchDevices(20),
      fetchStats(),
      fetchAlerts(),
      fetchRiskTrend(),
    ]).then(([devicesResult, statsResult, alertsResult, trendResult]) => {
      // Devices
      if (devicesResult.status === "fulfilled" && devicesResult.value.length > 0) {
        setEquipmentList(devicesResult.value);
      }

      // KPI stats
      if (statsResult.status === "fulfilled" && statsResult.value) {
        const stats = statsResult.value;
        setKpiData([
          {
            label: "Total Medical Devices",
            value: stats.totalDevices,
            change: 0,
            changeLabel: "from dataset",
            sparkline: [stats.totalDevices * 0.95, stats.totalDevices * 0.96, stats.totalDevices * 0.97, stats.totalDevices * 0.98, stats.totalDevices * 0.99, stats.totalDevices],
          },
          {
            label: "Devices at Risk",
            value: stats.devicesAtRisk,
            change: 0,
            changeLabel: "risk score > 40",
            sparkline: [stats.devicesAtRisk + 5, stats.devicesAtRisk + 3, stats.devicesAtRisk + 2, stats.devicesAtRisk],
          },
          {
            label: "Predicted Failures (30d)",
            value: stats.predictedFailures30d,
            change: 0,
            changeLabel: "risk score > 70",
            sparkline: [stats.predictedFailures30d + 4, stats.predictedFailures30d + 3, stats.predictedFailures30d + 1, stats.predictedFailures30d],
          },
          {
            label: "Avg Risk Score",
            value: stats.avgRiskScore,
            change: 0,
            changeLabel: "across fleet",
            sparkline: [stats.avgRiskScore + 3, stats.avgRiskScore + 2, stats.avgRiskScore + 1, stats.avgRiskScore],
          },
        ]);
      }

      // Alerts
      if (alertsResult.status === "fulfilled" && alertsResult.value.length > 0) {
        setAlertsList(alertsResult.value);
      }

      // Risk trend
      if (trendResult.status === "fulfilled" && trendResult.value.length > 0) {
        setRiskTrendData(trendResult.value);
      }
    });
  }, []);

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

