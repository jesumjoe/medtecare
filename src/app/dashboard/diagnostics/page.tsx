"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Cell,
  Tooltip,
} from "recharts";
import { Bot, BookOpen, ChevronDown, ExternalLink } from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";
import { StatusBadge } from "@/components/shared/status-badge";
import { RiskGauge } from "@/components/shared/risk-gauge";
import {
  equipmentList,
  featureImportanceData,
  diagnosticMessages,
  manualReferences,
} from "@/lib/mock-data";
import type { Equipment } from "@/lib/mock-data";

function SHAPChart() {
  const data = featureImportanceData.map((f) => ({
    ...f,
    absImportance: Math.abs(f.importance),
  }));

  return (
    <GlassCard hover={false}>
      <h3 className="mb-1 text-base font-semibold text-foreground">Key Risk Drivers</h3>
      <p className="mb-4 text-xs text-muted-foreground">
        SHAP-style feature importance — contribution to risk score
      </p>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 0, right: 10, bottom: 0, left: 110 }}
          >
            <XAxis
              type="number"
              tick={{ fill: "#94A3B8", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              domain={[0, 0.5]}
            />
            <YAxis
              type="category"
              dataKey="feature"
              tick={{ fill: "#CBD5E1", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              width={108}
            />
            <Tooltip
              contentStyle={{
                background: "#131825",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "8px",
                fontSize: "12px",
                color: "#E2E8F0",
              }}
              formatter={(value: any) => [
                `${(Number(value) * 100).toFixed(0)}%`,
                "Impact",
              ]}
            />
            <Bar dataKey="absImportance" radius={[0, 4, 4, 0]} barSize={20}>
              {data.map((entry, i) => (
                <Cell
                  key={i}
                  fill={
                    entry.direction === "positive"
                      ? "var(--sentinel-critical)"
                      : "var(--sentinel-healthy)"
                  }
                  fillOpacity={0.8}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <div className="h-2 w-2 rounded-full bg-sentinel-critical" />
          Increases risk
        </div>
        <div className="flex items-center gap-1.5">
          <div className="h-2 w-2 rounded-full bg-sentinel-healthy" />
          Decreases risk
        </div>
      </div>
    </GlassCard>
  );
}

function DiagnosticChat() {
  return (
    <GlassCard hover={false} className="flex flex-col">
      <div className="mb-4 flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sentinel-blue/15">
          <Bot className="h-4 w-4 text-sentinel-blue-light" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-foreground">
            Chief Diagnostician Agent
          </h3>
          <p className="text-[0.6rem] text-sentinel-blue-light uppercase tracking-wider font-semibold">
            AI-Powered Analysis
          </p>
        </div>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto max-h-96">
        {diagnosticMessages.map((msg, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.3 }}
            className={
              msg.role === "system"
                ? "rounded-lg bg-sentinel-glass px-3 py-2 text-xs text-muted-foreground"
                : "rounded-lg border border-sentinel-blue/15 bg-sentinel-blue/5 px-4 py-3"
            }
          >
            {msg.role === "agent" ? (
              <div className="prose prose-invert prose-sm max-w-none text-sm leading-relaxed text-foreground/90 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:text-foreground [&_h2]:mt-0 [&_h2]:mb-2 [&_strong]:text-foreground [&_li]:text-foreground/80 [&_ul]:my-2">
                {msg.content.split("\n").map((line, li) => {
                  if (line.startsWith("## "))
                    return (
                      <h2 key={li}>{line.replace("## ", "")}</h2>
                    );
                  if (line.startsWith("**") && line.endsWith("**"))
                    return (
                      <p key={li} className="font-semibold text-foreground">
                        {line.replace(/\*\*/g, "")}
                      </p>
                    );
                  if (line.startsWith("- "))
                    return (
                      <p key={li} className="ml-3 text-foreground/80">
                        • {line.replace("- ", "")}
                      </p>
                    );
                  if (line.match(/^\d+\./))
                    return (
                      <p key={li} className="text-foreground/80">
                        {line}
                      </p>
                    );
                  if (line.trim() === "") return <br key={li} />;
                  return <p key={li}>{line}</p>;
                })}
              </div>
            ) : (
              <span>{msg.content}</span>
            )}
          </motion.div>
        ))}
      </div>
    </GlassCard>
  );
}

function ManualReferences() {
  return (
    <GlassCard hover={false}>
      <div className="mb-4 flex items-center gap-2">
        <BookOpen className="h-4 w-4 text-sentinel-blue-light" />
        <h3 className="text-base font-semibold text-foreground">
          Maintenance Manual References
        </h3>
      </div>

      <div className="space-y-3">
        {manualReferences.map((ref, i) => (
          <motion.div
            key={ref.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 + i * 0.1 }}
            className="group rounded-lg border border-sentinel-glass-border p-3 transition-all hover:border-sentinel-blue/20 hover:bg-sentinel-glass"
          >
            <div className="flex items-start justify-between">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-xs font-semibold text-foreground truncate">
                    {ref.title}
                  </h4>
                  <span className="shrink-0 rounded bg-sentinel-blue/10 px-1.5 py-0.5 text-[0.55rem] font-bold text-sentinel-blue-light">
                    {(ref.relevance * 100).toFixed(0)}% match
                  </span>
                </div>
                <p className="text-[0.65rem] font-medium text-sentinel-blue-light mb-1">
                  {ref.section}
                </p>
                <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                  {ref.excerpt}
                </p>
              </div>
              <ExternalLink className="ml-2 h-3.5 w-3.5 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
            </div>
          </motion.div>
        ))}
      </div>
    </GlassCard>
  );
}

export default function DiagnosticsPage() {
  const [selectedEquipment, setSelectedEquipment] = useState<Equipment>(
    equipmentList.find((e) => e.status === "critical") || equipmentList[0]
  );
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <div className="space-y-6">
      {/* Header + Equipment selector */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Diagnostics
          </h1>
          <p className="text-sm text-muted-foreground">
            AI-powered root cause analysis and explainability
          </p>
        </div>

        {/* Equipment dropdown */}
        <div className="relative">
          <button
            type="button"
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="inline-flex items-center gap-2 rounded-lg border border-sentinel-glass-border bg-sentinel-glass px-4 py-2.5 text-sm font-medium text-foreground transition-all hover:border-sentinel-blue/30"
          >
            <div
              className="h-2 w-2 rounded-full"
              style={{
                background:
                  selectedEquipment.status === "critical"
                    ? "var(--sentinel-critical)"
                    : selectedEquipment.status === "warning"
                    ? "var(--sentinel-warning)"
                    : "var(--sentinel-healthy)",
              }}
            />
            {selectedEquipment.name}
            <ChevronDown className="h-4 w-4 text-muted-foreground" />
          </button>

          {dropdownOpen && (
            <>
              <div className="fixed inset-0 z-40" onClick={() => setDropdownOpen(false)} />
              <div className="absolute right-0 top-full z-50 mt-2 w-72 rounded-lg border border-sentinel-glass-border bg-sentinel-bg-to/95 p-2 shadow-xl backdrop-blur-xl">
                {equipmentList.map((eq) => (
                  <button
                    key={eq.id}
                    type="button"
                    className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm text-foreground transition-colors hover:bg-sentinel-glass"
                    onClick={() => {
                      setSelectedEquipment(eq);
                      setDropdownOpen(false);
                    }}
                  >
                    <div
                      className="h-2 w-2 rounded-full"
                      style={{
                        background:
                          eq.status === "critical"
                            ? "var(--sentinel-critical)"
                            : eq.status === "warning"
                            ? "var(--sentinel-warning)"
                            : "var(--sentinel-healthy)",
                      }}
                    />
                    <span className="truncate">{eq.name}</span>
                    <StatusBadge variant={eq.status} className="ml-auto">
                      {eq.riskScore}
                    </StatusBadge>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* Equipment overview bar */}
      <GlassCard hover={false} className="flex flex-col items-center gap-6 sm:flex-row">
        <RiskGauge score={selectedEquipment.riskScore} size={120} />

        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-foreground">
              {selectedEquipment.name}
            </h2>
            <StatusBadge variant={selectedEquipment.status} pulse size="md">
              {selectedEquipment.status}
            </StatusBadge>
          </div>
          <p className="text-sm text-muted-foreground">
            {selectedEquipment.type} — {selectedEquipment.location}
          </p>

          {/* Sensor readings */}
          <div className="flex flex-wrap gap-4 pt-2">
            {selectedEquipment.sensorReadings.map((sensor) => {
              const outOfRange =
                sensor.value < sensor.normalRange[0] ||
                sensor.value > sensor.normalRange[1];
              return (
                <div key={sensor.name} className="text-sm">
                  <span className="text-xs text-muted-foreground">
                    {sensor.name}
                  </span>
                  <p
                    className={`font-semibold ${
                      outOfRange ? "text-sentinel-critical" : "text-foreground"
                    }`}
                  >
                    {sensor.value}
                    <span className="text-xs text-muted-foreground ml-0.5">
                      {sensor.unit}
                    </span>
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </GlassCard>

      {/* Main content grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        <SHAPChart />
        <DiagnosticChat />
      </div>

      {/* Manual references */}
      <ManualReferences />
    </div>
  );
}
