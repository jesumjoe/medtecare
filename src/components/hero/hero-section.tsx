"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Activity, Bot, Radar, Smartphone } from "lucide-react";
import { GlassCard } from "@/components/shared/glass-card";

// ---- Landing Navbar ----

export function LandingNav() {
  return (
    <header className="fixed top-0 w-full z-50 border-b border-sentinel-glass-border bg-sentinel-bg-from/70 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sentinel-blue font-bold text-white text-sm">
            S
          </div>
          <span className="text-lg font-bold tracking-tight text-foreground">
            Sentinel<span className="text-sentinel-blue">Ops</span>
          </span>
        </Link>

        <div className="hidden items-center gap-8 md:flex">
          <a href="#features" className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            Features
          </a>
          <a href="#platform" className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            Platform
          </a>
          <a href="#about" className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            About
          </a>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/dashboard"
            className="hidden rounded-lg border border-sentinel-glass-border px-4 py-2 text-sm font-medium text-muted-foreground transition-all hover:border-sentinel-blue/30 hover:text-foreground sm:inline-flex"
          >
            Sign In
          </Link>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 rounded-lg bg-sentinel-blue px-4 py-2 text-sm font-semibold text-white transition-all hover:bg-sentinel-blue-light hover:shadow-[0_0_20px_rgba(59,130,246,0.3)]"
          >
            Launch App
          </Link>
        </div>
      </nav>
    </header>
  );
}

// ---- Hero Content ----

export function HeroContent() {
  return (
    <div className="relative z-10 flex flex-col items-center pt-32 pb-16 text-center px-6">
      {/* Ambient glow blobs */}
      <div className="pointer-events-none absolute top-1/4 left-1/4 h-96 w-96 rounded-full bg-sentinel-blue/5 blur-3xl" />
      <div className="pointer-events-none absolute bottom-1/3 right-1/4 h-64 w-64 rounded-full bg-sentinel-blue/3 blur-3xl" />

      {/* Badge */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="mb-8 inline-flex items-center gap-3 rounded-full border border-sentinel-blue/30 bg-sentinel-blue/10 px-5 py-2.5 backdrop-blur-xl"
      >
        <span className="relative flex h-2 w-2">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-sentinel-blue opacity-75" />
          <span className="relative inline-flex h-2 w-2 rounded-full bg-sentinel-blue" />
        </span>
        <span className="text-xs font-bold uppercase tracking-widest text-sentinel-blue-light">
          Built for Cognizant Hackathon 2025
        </span>
      </motion.div>

      {/* Headline */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.3 }}
        className="max-w-4xl space-y-4 mb-6"
      >
        <h1
          className="text-4xl font-bold leading-tight tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl"
        >
          <span className="text-gradient-hero block font-light text-3xl sm:text-4xl md:text-5xl mb-2">
            Predict Failure
          </span>
          <span className="text-gradient-blue relative inline-block font-black">
            Before It Happens
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "100%" }}
              transition={{ duration: 1.5, delay: 1.2, ease: "easeOut" }}
              className="absolute -bottom-3 left-0 h-1 rounded-full bg-gradient-to-r from-sentinel-blue via-sentinel-blue-light to-transparent shadow-[0_0_15px_rgba(59,130,246,0.5)]"
            />
          </span>
        </h1>
      </motion.div>

      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.8 }}
        className="mb-10 max-w-2xl text-base text-muted-foreground sm:text-lg md:text-xl leading-relaxed"
      >
        AI-powered predictive maintenance for industrial fleets.{" "}
        <span className="text-foreground font-medium">Real-time risk scoring</span>,{" "}
        <span className="text-foreground font-medium">autonomous diagnostic agents</span>, and{" "}
        <span className="text-foreground font-medium">proactive maintenance scheduling</span>.
      </motion.p>

      {/* CTA Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1 }}
        className="flex flex-col items-center gap-4 sm:flex-row"
      >
        <Link href="/dashboard">
          <motion.button
            type="button"
            whileHover={{
              scale: 1.05,
              boxShadow: "0 0 30px rgba(59,130,246,0.3)",
            }}
            whileTap={{ scale: 0.98 }}
            className="group inline-flex items-center gap-2.5 rounded-xl bg-gradient-to-r from-sentinel-blue to-sentinel-blue-light px-8 py-4 text-base font-semibold text-white shadow-xl transition-all"
          >
            Enter Command Center
            <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
          </motion.button>
        </Link>

        <motion.button
          type="button"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.98 }}
          className="inline-flex items-center gap-2.5 rounded-xl border border-sentinel-glass-border bg-sentinel-glass px-8 py-4 text-base font-semibold text-foreground backdrop-blur-xl transition-all hover:border-sentinel-blue/30 hover:bg-sentinel-glass-hover"
        >
          <Activity className="h-5 w-5 text-sentinel-blue" />
          Watch Demo
        </motion.button>
      </motion.div>

      {/* Dashboard Preview with glow frame */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 1.3 }}
        className="relative mx-auto mt-16 w-full max-w-5xl"
      >
        {/* Glow behind the preview */}
        <div className="pointer-events-none absolute -inset-4 rounded-2xl bg-gradient-to-b from-sentinel-blue/20 via-sentinel-blue/5 to-transparent blur-2xl" />

        {/* Dashboard mockup frame */}
        <div className="relative overflow-hidden rounded-xl border border-sentinel-glass-border bg-sentinel-bg-to/80 shadow-2xl shadow-sentinel-blue/5 backdrop-blur-xl">
          {/* Fake browser chrome */}
          <div className="flex items-center gap-2 border-b border-sentinel-glass-border px-4 py-3">
            <div className="h-3 w-3 rounded-full bg-sentinel-critical/60" />
            <div className="h-3 w-3 rounded-full bg-sentinel-warning/60" />
            <div className="h-3 w-3 rounded-full bg-sentinel-healthy/60" />
            <div className="ml-4 flex-1 rounded-md bg-sentinel-glass px-3 py-1">
              <span className="text-xs text-muted-foreground">
                app.sentinelops.io/dashboard
              </span>
            </div>
          </div>

          {/* Mini dashboard preview */}
          <div className="p-4 sm:p-6">
            {/* Mini KPI row */}
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 mb-4">
              {[
                { label: "Total Assets", value: "127", color: "text-foreground" },
                { label: "At Risk", value: "23", color: "text-sentinel-warning" },
                { label: "Failures (30d)", value: "8", color: "text-sentinel-critical" },
                { label: "Avg Risk", value: "34.2", color: "text-sentinel-blue-light" },
              ].map((kpi) => (
                <div
                  key={kpi.label}
                  className="rounded-lg border border-sentinel-glass-border bg-sentinel-glass p-3"
                >
                  <p className="text-[0.6rem] font-semibold uppercase tracking-wider text-muted-foreground">
                    {kpi.label}
                  </p>
                  <p className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</p>
                </div>
              ))}
            </div>

            {/* Mini chart placeholder */}
            <div className="rounded-lg border border-sentinel-glass-border bg-sentinel-glass p-4">
              <div className="mb-2 flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-sentinel-blue" />
                <span className="text-xs text-muted-foreground">Risk Trend — 30d</span>
              </div>
              <div className="flex h-16 items-end gap-1">
                {[28, 32, 30, 35, 33, 38, 36, 42, 40, 45, 43, 48].map((v, i) => (
                  <motion.div
                    key={i}
                    initial={{ height: 0 }}
                    animate={{ height: `${v}%` }}
                    transition={{ duration: 0.5, delay: 1.5 + i * 0.05 }}
                    className="flex-1 rounded-t bg-gradient-to-t from-sentinel-blue/30 to-sentinel-blue/60"
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

// ---- Feature Cards ----

const features = [
  {
    icon: Activity,
    title: "Real-time Risk Scoring",
    description:
      "Continuous monitoring with ML-driven risk scores that adapt to evolving equipment behavior patterns.",
  },
  {
    icon: Bot,
    title: "AI Diagnostic Agents",
    description:
      "Autonomous LangGraph agents that diagnose root causes, cross-reference manuals, and recommend actions.",
  },
  {
    icon: Radar,
    title: "Fleet-wide Monitoring",
    description:
      "Unified command center for your entire equipment fleet with predictive failure forecasting up to 30 days out.",
  },
  {
    icon: Smartphone,
    title: "Mobile Technician Sync",
    description:
      "Field technicians receive prioritized task queues with AI-generated repair instructions and OCR log scanning.",
  },
];

export function FeatureCards() {
  return (
    <section id="features" className="relative py-24 px-6">
      <div className="mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="mb-12 text-center"
        >
          <p className="eyebrow text-sentinel-blue-light mb-3">Platform Capabilities</p>
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything you need to prevent downtime
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-muted-foreground">
            From sensor ingestion to technician dispatch — SentinelOps covers the full predictive maintenance lifecycle.
          </p>
        </motion.div>

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 25 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <GlassCard className="h-full group">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-lg bg-sentinel-blue/10 text-sentinel-blue transition-all group-hover:bg-sentinel-blue/20 group-hover:shadow-[0_0_20px_rgba(59,130,246,0.15)]">
                  <feature.icon className="h-5 w-5" />
                </div>
                <h3 className="mb-2 text-sm font-semibold text-foreground">
                  {feature.title}
                </h3>
                <p className="text-xs leading-relaxed text-muted-foreground">
                  {feature.description}
                </p>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
