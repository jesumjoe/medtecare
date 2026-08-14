"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { motion, type HTMLMotionProps } from "framer-motion";

interface GlassCardProps extends Omit<HTMLMotionProps<"div">, "children"> {
  children: React.ReactNode;
  hover?: boolean;
  glow?: "blue" | "healthy" | "warning" | "critical" | "none";
  className?: string;
  padding?: "sm" | "md" | "lg" | "none";
}

export function GlassCard({
  children,
  hover = true,
  glow = "none",
  className,
  padding = "md",
  ...props
}: GlassCardProps) {
  const glowClasses = {
    blue: "glow-blue",
    healthy: "glow-healthy",
    warning: "glow-warning",
    critical: "glow-critical",
    none: "",
  };

  const paddingClasses = {
    sm: "p-3",
    md: "p-5",
    lg: "p-7",
    none: "",
  };

  return (
    <motion.div
      className={cn(
        "rounded-xl border border-sentinel-glass-border bg-sentinel-glass backdrop-blur-xl",
        hover && "transition-all duration-300 hover:bg-sentinel-glass-hover hover:border-sentinel-blue/20 hover:-translate-y-0.5 hover:shadow-[0_8px_32px_rgba(0,0,0,0.3),0_0_0_1px_rgba(59,130,246,0.1)]",
        glowClasses[glow],
        paddingClasses[padding],
        className
      )}
      {...props}
    >
      {children}
    </motion.div>
  );
}
