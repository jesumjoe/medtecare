"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  ClipboardList,
  Camera,
  Clock,
  CheckCircle2,
  ScanLine,
  History,
  UserCircle,
  Wrench,
} from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";
import { StatusBadge } from "@/components/shared/status-badge";
import {
  ticketsList,
  techniciansList,
  formatRelativeTime,
} from "@/lib/mock-data";

const currentTechnician = techniciansList[0]; // Marcus Chen
const assignedTickets = ticketsList.filter(
  (t) => t.assignedTechnician === currentTechnician.name && t.status !== "resolved"
);

type MobileTab = "tasks" | "scan" | "history" | "profile";

function TaskCard({
  ticket,
  index,
}: {
  ticket: (typeof ticketsList)[0];
  index: number;
}) {
  const [completed, setCompleted] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <GlassCard
        className={`transition-all ${completed ? "opacity-50" : ""}`}
      >
        {/* Equipment photo placeholder */}
        <div className="mb-3 flex h-32 items-center justify-center rounded-lg bg-gradient-to-br from-sentinel-glass to-sentinel-bg-to border border-sentinel-glass-border overflow-hidden">
          <div className="text-center">
            <Wrench className="mx-auto h-8 w-8 text-muted-foreground/30 mb-1" />
            <span className="text-[0.6rem] text-muted-foreground/40">Equipment Photo</span>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-start justify-between gap-2">
            <h3 className="text-sm font-semibold text-foreground line-clamp-1">
              {ticket.title}
            </h3>
            <StatusBadge variant={ticket.priority} pulse={ticket.priority === "critical"}>
              {ticket.priority}
            </StatusBadge>
          </div>

          <p className="text-xs text-muted-foreground">{ticket.equipmentName}</p>
          <p className="text-xs text-muted-foreground/80 line-clamp-2">
            {ticket.description}
          </p>

          <div className="flex items-center gap-2 text-[0.65rem] text-muted-foreground">
            <Clock className="h-3 w-3" />
            Assigned {formatRelativeTime(ticket.createdAt)}
          </div>

          {/* Action buttons */}
          <div className="flex gap-2 pt-2">
            <button
              type="button"
              onClick={() => setCompleted(!completed)}
              className={`flex flex-1 items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-xs font-semibold transition-all ${
                completed
                  ? "bg-sentinel-healthy/20 text-sentinel-healthy border border-sentinel-healthy/30"
                  : "bg-sentinel-blue/15 text-sentinel-blue-light border border-sentinel-blue/30 hover:bg-sentinel-blue/25"
              }`}
            >
              <CheckCircle2 className="h-4 w-4" />
              {completed ? "Completed ✓" : "Mark Complete"}
            </button>

            <button
              type="button"
              className="flex items-center justify-center gap-2 rounded-lg border border-sentinel-glass-border bg-sentinel-glass px-3 py-2.5 text-xs font-medium text-muted-foreground transition-all hover:border-sentinel-blue/30 hover:text-foreground"
            >
              <Camera className="h-4 w-4" />
              Scan Log
            </button>
          </div>
        </div>
      </GlassCard>
    </motion.div>
  );
}

function TasksFeed() {
  return (
    <div className="space-y-4">
      {assignedTickets.length > 0 ? (
        assignedTickets.map((ticket, i) => (
          <TaskCard key={ticket.id} ticket={ticket} index={i} />
        ))
      ) : (
        <GlassCard className="text-center py-12">
          <CheckCircle2 className="mx-auto h-10 w-10 text-sentinel-healthy/40 mb-3" />
          <p className="text-sm text-muted-foreground">All tasks completed!</p>
        </GlassCard>
      )}
    </div>
  );
}

function ScanView() {
  return (
    <GlassCard className="flex flex-col items-center justify-center py-16 text-center">
      <div className="mb-4 flex h-20 w-20 items-center justify-center rounded-2xl bg-sentinel-blue/10 border border-sentinel-blue/20">
        <ScanLine className="h-10 w-10 text-sentinel-blue-light" />
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">
        Scan Maintenance Log
      </h3>
      <p className="text-sm text-muted-foreground mb-6 max-w-xs">
        Use your device camera to scan and digitize paper maintenance logs via OCR
      </p>
      <button
        type="button"
        className="inline-flex items-center gap-2 rounded-lg bg-sentinel-blue px-6 py-3 text-sm font-semibold text-white transition-all hover:bg-sentinel-blue-light hover:shadow-[0_0_20px_rgba(59,130,246,0.3)]"
      >
        <Camera className="h-4 w-4" />
        Open Camera
      </button>
    </GlassCard>
  );
}

function HistoryView() {
  const resolved = ticketsList.filter(
    (t) => t.assignedTechnician === currentTechnician.name && t.status === "resolved"
  );

  return (
    <div className="space-y-3">
      {resolved.length > 0 ? (
        resolved.map((ticket, i) => (
          <motion.div
            key={ticket.id}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: i * 0.1 }}
          >
            <GlassCard padding="sm" className="opacity-70">
              <div className="flex items-center justify-between">
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-foreground truncate">
                    {ticket.title}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {ticket.equipmentName} • Resolved {formatRelativeTime(ticket.updatedAt)}
                  </p>
                </div>
                <CheckCircle2 className="ml-2 h-5 w-5 shrink-0 text-sentinel-healthy" />
              </div>
            </GlassCard>
          </motion.div>
        ))
      ) : (
        <GlassCard className="text-center py-12">
          <p className="text-sm text-muted-foreground">No completed tasks yet</p>
        </GlassCard>
      )}
    </div>
  );
}

function ProfileView() {
  return (
    <GlassCard className="text-center">
      <div className="mb-4 flex h-20 w-20 mx-auto items-center justify-center rounded-full bg-sentinel-blue/20 text-2xl font-bold text-sentinel-blue-light">
        {currentTechnician.avatar}
      </div>
      <h3 className="text-lg font-semibold text-foreground">
        {currentTechnician.name}
      </h3>
      <p className="text-sm text-muted-foreground">{currentTechnician.specialty}</p>
      <p className="text-xs text-muted-foreground mt-1">{currentTechnician.location}</p>

      <div className="mt-6 grid grid-cols-2 gap-3">
        <div className="rounded-lg border border-sentinel-glass-border bg-sentinel-glass p-3">
          <p className="text-2xl font-bold text-foreground">
            {currentTechnician.assignedTickets}
          </p>
          <p className="text-[0.65rem] text-muted-foreground uppercase tracking-wider">
            Active Tasks
          </p>
        </div>
        <div className="rounded-lg border border-sentinel-glass-border bg-sentinel-glass p-3">
          <p className="text-2xl font-bold text-sentinel-healthy">12</p>
          <p className="text-[0.65rem] text-muted-foreground uppercase tracking-wider">
            Completed
          </p>
        </div>
      </div>
    </GlassCard>
  );
}

export default function TechnicianPage() {
  const [activeTab, setActiveTab] = useState<MobileTab>("tasks");

  const tabs: { id: MobileTab; icon: typeof ClipboardList; label: string }[] = [
    { id: "tasks", icon: ClipboardList, label: "Tasks" },
    { id: "scan", icon: ScanLine, label: "Scan" },
    { id: "history", icon: History, label: "History" },
    { id: "profile", icon: UserCircle, label: "Profile" },
  ];

  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col bg-gradient-to-b from-sentinel-bg-from to-sentinel-bg-to">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-sentinel-glass-border bg-sentinel-bg-from/80 px-4 py-4 backdrop-blur-xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-foreground">
              Sentinel<span className="text-sentinel-blue">Ops</span>
            </h1>
            <p className="text-xs text-muted-foreground">
              Welcome, {currentTechnician.name}
            </p>
          </div>
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-sentinel-blue/20 text-sm font-bold text-sentinel-blue-light">
            {currentTechnician.avatar}
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 overflow-y-auto px-4 py-4">
        {activeTab === "tasks" && <TasksFeed />}
        {activeTab === "scan" && <ScanView />}
        {activeTab === "history" && <HistoryView />}
        {activeTab === "profile" && <ProfileView />}
      </main>

      {/* Bottom nav */}
      <nav className="sticky bottom-0 z-40 border-t border-sentinel-glass-border bg-sentinel-bg-from/90 backdrop-blur-xl">
        <div className="flex items-center justify-around py-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id)}
              className={`relative flex flex-col items-center gap-1 px-3 py-2 text-[0.6rem] font-semibold uppercase tracking-wider transition-all ${
                activeTab === tab.id
                  ? "text-sentinel-blue-light"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {activeTab === tab.id && (
                <motion.div
                  layoutId="mobile-tab"
                  className="absolute -top-0.5 left-1/2 h-0.5 w-8 -translate-x-1/2 rounded-full bg-sentinel-blue"
                  transition={{ type: "spring", bounce: 0.2, duration: 0.5 }}
                />
              )}
              <tab.icon className="h-5 w-5" />
              {tab.label}
            </button>
          ))}
        </div>
      </nav>
    </div>
  );
}
