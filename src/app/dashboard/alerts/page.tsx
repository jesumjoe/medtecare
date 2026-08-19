"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  GripVertical,
  Clock,
  User,
  ListFilter,
  LayoutGrid,
  ChevronDown,
} from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";
import { StatusBadge } from "@/components/shared/status-badge";
import { ticketsList as mockTicketsList, formatRelativeTime } from "@/lib/mock-data";
import type { MaintenanceTicket, TicketStatus } from "@/lib/mock-data";
import { fetchTickets, updateTicketStatus } from "@/lib/api";

type ViewMode = "table" | "kanban";

// ---- Status change handler ----

function StatusChanger({
  ticket,
  onStatusChange,
}: {
  ticket: MaintenanceTicket;
  onStatusChange: (id: string, status: TicketStatus) => void;
}) {
  const [open, setOpen] = useState(false);
  const nextStatuses: Record<TicketStatus, TicketStatus[]> = {
    "open": ["in-progress"],
    "in-progress": ["resolved", "open"],
    "resolved": ["open"],
  };
  const options = nextStatuses[ticket.status] || [];

  if (options.length === 0) return null;

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 rounded-md border border-sentinel-glass-border px-2 py-1 text-[0.65rem] font-medium text-muted-foreground transition-all hover:border-sentinel-blue/30 hover:text-foreground"
      >
        Move
        <ChevronDown className="h-3 w-3" />
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="absolute right-0 top-full z-50 mt-1 w-36 rounded-lg border border-sentinel-glass-border bg-sentinel-bg-to/95 p-1 shadow-xl backdrop-blur-xl">
            {options.map((status) => (
              <button
                key={status}
                type="button"
                className="flex w-full items-center gap-2 rounded-md px-3 py-1.5 text-left text-xs text-foreground transition-colors hover:bg-sentinel-glass"
                onClick={() => {
                  onStatusChange(ticket.id, status);
                  setOpen(false);
                }}
              >
                <span
                  className={`h-1.5 w-1.5 rounded-full ${
                    status === "open"
                      ? "bg-sentinel-blue"
                      : status === "in-progress"
                      ? "bg-sentinel-warning"
                      : "bg-sentinel-healthy"
                  }`}
                />
                {status}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

// ---- Table View ----

function AlertsTable({
  tickets,
  onStatusChange,
}: {
  tickets: MaintenanceTicket[];
  onStatusChange: (id: string, status: TicketStatus) => void;
}) {
  return (
    <GlassCard hover={false} padding="none" className="overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-sentinel-glass-border">
              {["Equipment", "Issue", "Priority", "Status", "Assigned To", "Created", ""].map(
                (h) => (
                  <th
                    key={h}
                    className="px-4 py-3 text-left text-[0.65rem] font-semibold uppercase tracking-wider text-muted-foreground"
                  >
                    {h}
                  </th>
                )
              )}
            </tr>
          </thead>
          <tbody>
            {tickets.map((ticket, i) => (
              <motion.tr
                key={ticket.id}
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="border-b border-sentinel-glass-border/50 transition-colors hover:bg-sentinel-glass"
              >
                <td className="px-4 py-3 font-medium text-foreground">
                  {ticket.equipmentName}
                </td>
                <td className="px-4 py-3 text-muted-foreground max-w-xs truncate">
                  {ticket.title}
                </td>
                <td className="px-4 py-3">
                  <StatusBadge variant={ticket.priority} pulse={ticket.priority === "critical"}>
                    {ticket.priority}
                  </StatusBadge>
                </td>
                <td className="px-4 py-3">
                  <span
                    className={`inline-flex items-center gap-1.5 text-xs font-medium ${
                      ticket.status === "open"
                        ? "text-sentinel-blue-light"
                        : ticket.status === "in-progress"
                        ? "text-sentinel-warning"
                        : "text-sentinel-healthy"
                    }`}
                  >
                    <span
                      className={`h-1.5 w-1.5 rounded-full ${
                        ticket.status === "open"
                          ? "bg-sentinel-blue"
                          : ticket.status === "in-progress"
                          ? "bg-sentinel-warning"
                          : "bg-sentinel-healthy"
                      }`}
                    />
                    {ticket.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {ticket.assignedTechnician || (
                    <span className="text-xs italic text-muted-foreground/50">Unassigned</span>
                  )}
                </td>
                <td className="px-4 py-3 text-xs text-muted-foreground">
                  {formatRelativeTime(ticket.createdAt)}
                </td>
                <td className="px-4 py-3">
                  <StatusChanger ticket={ticket} onStatusChange={onStatusChange} />
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassCard>
  );
}

// ---- Kanban View ----

const kanbanColumns: { status: TicketStatus; label: string; color: string }[] = [
  { status: "open", label: "Open", color: "var(--sentinel-blue)" },
  { status: "in-progress", label: "In Progress", color: "var(--sentinel-warning)" },
  { status: "resolved", label: "Resolved", color: "var(--sentinel-healthy)" },
];

function KanbanView({
  tickets,
  onStatusChange,
}: {
  tickets: MaintenanceTicket[];
  onStatusChange: (id: string, status: TicketStatus) => void;
}) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {kanbanColumns.map((col) => {
        const colTickets = tickets.filter((t) => t.status === col.status);
        return (
          <div key={col.status} className="space-y-3">
            {/* Column header */}
            <div className="flex items-center gap-2 px-1">
              <div
                className="h-2.5 w-2.5 rounded-full"
                style={{ background: col.color }}
              />
              <span className="text-sm font-semibold text-foreground">
                {col.label}
              </span>
              <span className="ml-auto rounded-full bg-sentinel-glass px-2 py-0.5 text-[0.6rem] font-bold text-muted-foreground">
                {colTickets.length}
              </span>
            </div>

            {/* Cards */}
            <div className="space-y-2">
              {colTickets.map((ticket, i) => (
                <motion.div
                  key={ticket.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <GlassCard padding="sm" className="group relative">
                    {/* Drag handle */}
                    <div className="absolute left-1 top-1/2 -translate-y-1/2 cursor-grab text-muted-foreground/30 opacity-0 transition-opacity group-hover:opacity-100">
                      <GripVertical className="h-4 w-4" />
                    </div>

                    <div className="pl-4">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="text-xs font-semibold text-foreground line-clamp-2">
                          {ticket.title}
                        </span>
                        <StatusBadge variant={ticket.priority}>
                          {ticket.priority}
                        </StatusBadge>
                      </div>

                      <p className="text-[0.65rem] text-muted-foreground mb-2">
                        {ticket.equipmentName}
                      </p>

                      <div className="flex items-center gap-3 text-[0.6rem] text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {formatRelativeTime(ticket.createdAt)}
                        </span>
                        {ticket.assignedTechnician && (
                          <span className="flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {ticket.assignedTechnician}
                          </span>
                        )}
                      </div>

                      <div className="mt-2">
                        <StatusChanger ticket={ticket} onStatusChange={onStatusChange} />
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              ))}

              {colTickets.length === 0 && (
                <div className="rounded-lg border-2 border-dashed border-sentinel-glass-border p-8 text-center">
                  <p className="text-xs text-muted-foreground/50">No tickets</p>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ---- Main Page ----

export default function AlertsPage() {
  const [viewMode, setViewMode] = useState<ViewMode>("table");
  const [tickets, setTickets] = useState<MaintenanceTicket[]>(mockTicketsList);

  useEffect(() => {
    fetchTickets().then((data) => {
      if (data.length > 0) {
        setTickets(data);
      }
    });
  }, []);

  const handleStatusChange = async (ticketId: string, newStatus: TicketStatus) => {
    const success = await updateTicketStatus(ticketId, newStatus as "open" | "in-progress" | "resolved");
    if (success) {
      setTickets((prev) =>
        prev.map((t) =>
          t.id === ticketId
            ? { ...t, status: newStatus, updatedAt: new Date().toISOString() }
            : t
        )
      );
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Maintenance Queue
          </h1>
          <p className="text-sm text-muted-foreground">
            {tickets.filter((t) => t.status === "open").length} open •{" "}
            {tickets.filter((t) => t.status === "in-progress").length} in progress •{" "}
            {tickets.filter((t) => t.status === "resolved").length} resolved
          </p>
        </div>

        {/* View toggle */}
        <div className="flex items-center rounded-lg border border-sentinel-glass-border bg-sentinel-glass p-1">
          <button
            type="button"
            onClick={() => setViewMode("table")}
            className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-all ${
              viewMode === "table"
                ? "bg-sentinel-blue/15 text-sentinel-blue-light"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <ListFilter className="h-3.5 w-3.5" />
            Table
          </button>
          <button
            type="button"
            onClick={() => setViewMode("kanban")}
            className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-all ${
              viewMode === "kanban"
                ? "bg-sentinel-blue/15 text-sentinel-blue-light"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <LayoutGrid className="h-3.5 w-3.5" />
            Kanban
          </button>
        </div>
      </div>

      {/* Content */}
      {viewMode === "table" ? (
        <AlertsTable tickets={tickets} onStatusChange={handleStatusChange} />
      ) : (
        <KanbanView tickets={tickets} onStatusChange={handleStatusChange} />
      )}
    </div>
  );
}

