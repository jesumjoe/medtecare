"use client";

import dynamic from "next/dynamic";
import { LandingNav, HeroContent, FeatureCards } from "@/components/hero/hero-section";

// Lazy-load the 3D globe to avoid SSR issues with Three.js
const GlobeHero = dynamic(
  () => import("@/components/hero/globe-scene").then((mod) => ({ default: mod.GlobeHero })),
  { ssr: false }
);

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-sentinel-bg-from to-sentinel-bg-to">
      <LandingNav />

      {/* Hero with 3D globe background */}
      <GlobeHero rotationSpeed={0.003} globeRadius={1.6}>
        <HeroContent />
      </GlobeHero>

      {/* Feature highlights */}
      <FeatureCards />

      {/* Footer */}
      <footer className="border-t border-sentinel-glass-border px-6 py-8">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded bg-sentinel-blue text-xs font-bold text-white">
              S
            </div>
            <span className="text-sm font-semibold">
              Sentinel<span className="text-sentinel-blue">Ops</span>
            </span>
          </div>
          <p className="text-xs text-muted-foreground">
            © 2025 SentinelOps — Cognizant Hackathon Submission. Built with Next.js, React Three Fiber & AI.
          </p>
        </div>
      </footer>
    </main>
  );
}
