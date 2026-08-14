"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/shared/navbar";
import { Sidebar } from "@/components/shared/sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-gradient-to-b from-sentinel-bg-from to-sentinel-bg-to">
      <Navbar onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <main className="flex-1 overflow-y-auto px-4 py-6 md:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </div>
  );
}
