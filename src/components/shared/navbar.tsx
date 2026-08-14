"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Bell, Search, Menu } from "lucide-react";
import { cn } from "@/lib/utils";

interface NavbarProps {
  onMenuToggle?: () => void;
  className?: string;
}

export function Navbar({ onMenuToggle, className }: NavbarProps) {
  const [searchFocused, setSearchFocused] = useState(false);

  return (
    <header
      className={cn(
        "sticky top-0 z-50 flex h-16 items-center justify-between border-b border-sentinel-glass-border bg-sentinel-bg-from/80 px-4 backdrop-blur-xl md:px-6",
        className
      )}
    >
      {/* Left: menu toggle + logo */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onMenuToggle}
          className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-sentinel-glass hover:text-foreground lg:hidden"
          aria-label="Toggle sidebar"
        >
          <Menu className="h-5 w-5" />
        </button>

        <Link href="/dashboard" className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sentinel-blue font-bold text-white text-sm">
            S
          </div>
          <span className="hidden text-lg font-bold tracking-tight text-foreground sm:inline">
            Sentinel<span className="text-sentinel-blue">Ops</span>
          </span>
        </Link>
      </div>

      {/* Center: search */}
      <div className="mx-4 hidden flex-1 max-w-md md:block">
        <div
          className={cn(
            "relative flex items-center rounded-lg border transition-all duration-300",
            searchFocused
              ? "border-sentinel-blue/40 bg-sentinel-glass shadow-[0_0_15px_rgba(59,130,246,0.1)]"
              : "border-sentinel-glass-border bg-sentinel-glass"
          )}
        >
          <Search className="ml-3 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search equipment, alerts, tickets..."
            className="w-full bg-transparent px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
            onFocus={() => setSearchFocused(true)}
            onBlur={() => setSearchFocused(false)}
          />
          <kbd className="mr-3 hidden rounded border border-sentinel-glass-border px-1.5 py-0.5 text-[0.6rem] text-muted-foreground lg:inline">
            ⌘K
          </kbd>
        </div>
      </div>

      {/* Right: notification + avatar */}
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="relative rounded-lg p-2 text-muted-foreground transition-colors hover:bg-sentinel-glass hover:text-foreground"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />
          {/* Unread badge */}
          <span className="absolute right-1.5 top-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-sentinel-critical text-[0.55rem] font-bold text-white">
            3
          </span>
        </button>

        <button
          type="button"
          className="flex h-9 w-9 items-center justify-center rounded-full bg-sentinel-blue/20 text-sm font-semibold text-sentinel-blue-light transition-all hover:bg-sentinel-blue/30"
          aria-label="Profile menu"
        >
          AD
        </button>
      </div>
    </header>
  );
}
