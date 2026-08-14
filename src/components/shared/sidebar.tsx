"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  Server,
  AlertTriangle,
  Stethoscope,
  FileBarChart,
  Settings,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/dashboard/fleet", label: "Fleet", icon: Server },
  { href: "/dashboard/alerts", label: "Alerts", icon: AlertTriangle },
  { href: "/dashboard/diagnostics", label: "Diagnostics", icon: Stethoscope },
  { href: "/dashboard/reports", label: "Reports", icon: FileBarChart },
  { href: "/dashboard/settings", label: "Settings", icon: Settings },
];

interface SidebarProps {
  open?: boolean;
  onClose?: () => void;
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();

  const content = (
    <nav className="flex flex-col gap-1 px-3 py-4">
      <div className="mb-4 px-3">
        <p className="eyebrow text-muted-foreground">Navigation</p>
      </div>

      {navItems.map((item) => {
        const isActive =
          item.href === "/dashboard"
            ? pathname === "/dashboard"
            : pathname.startsWith(item.href);

        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onClose}
            className={cn(
              "relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
              isActive
                ? "text-sentinel-blue-light"
                : "text-muted-foreground hover:bg-sentinel-glass hover:text-foreground"
            )}
          >
            {isActive && (
              <motion.div
                layoutId="sidebar-active"
                className="absolute inset-0 rounded-lg bg-sentinel-blue/10 border border-sentinel-blue/20"
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
              />
            )}
            <item.icon className="relative z-10 h-4.5 w-4.5" />
            <span className="relative z-10">{item.label}</span>

            {/* Alert count for Alerts nav item */}
            {item.label === "Alerts" && (
              <span className="relative z-10 ml-auto flex h-5 min-w-5 items-center justify-center rounded-full bg-sentinel-critical/20 px-1.5 text-[0.6rem] font-bold text-sentinel-critical">
                5
              </span>
            )}
          </Link>
        );
      })}
    </nav>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex lg:w-60 lg:flex-col lg:border-r lg:border-sentinel-glass-border lg:bg-sidebar">
        {content}
      </aside>

      {/* Mobile overlay */}
      {open && (
        <>
          <div
            className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
            onClick={onClose}
          />
          <aside className="fixed inset-y-0 left-0 z-50 w-64 border-r border-sentinel-glass-border bg-sidebar lg:hidden animate-slide-down">
            <div className="flex items-center justify-between border-b border-sentinel-glass-border px-4 py-4">
              <span className="text-lg font-bold tracking-tight">
                Sentinel<span className="text-sentinel-blue">Ops</span>
              </span>
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg p-1.5 text-muted-foreground hover:bg-sentinel-glass"
                aria-label="Close sidebar"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            {content}
          </aside>
        </>
      )}
    </>
  );
}
