"use client";

import { GlassCard } from "@/components/shared/glass-card";
import { Settings as SettingsIcon } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Platform configuration and team management
        </p>
      </div>
      <GlassCard className="flex flex-col items-center justify-center py-20 text-center">
        <SettingsIcon className="h-12 w-12 text-muted-foreground/30 mb-4" />
        <h3 className="text-lg font-semibold text-foreground mb-2">Settings</h3>
        <p className="text-sm text-muted-foreground max-w-sm">
          Platform settings, notification preferences, and team management will be connected to Supabase auth.
        </p>
      </GlassCard>
    </div>
  );
}
