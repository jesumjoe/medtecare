"use client";

import React, { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { PerspectiveCamera } from "@react-three/drei";
import * as THREE from "three";
import { cn } from "@/lib/utils";

// ---- Node Network (equipment fleet visualization) ----

interface NetworkNode {
  position: THREE.Vector3;
  status: "healthy" | "warning" | "critical";
  speed: number;
}

function generateNodes(count: number, radius: number): NetworkNode[] {
  const nodes: NetworkNode[] = [];
  const phi = (1 + Math.sqrt(5)) / 2; // golden ratio for even distribution

  for (let i = 0; i < count; i++) {
    const y = 1 - (i / (count - 1)) * 2;
    const radiusAtY = Math.sqrt(1 - y * y);
    const theta = ((2 * Math.PI * i) / phi) * phi;

    nodes.push({
      position: new THREE.Vector3(
        Math.cos(theta) * radiusAtY * radius,
        y * radius,
        Math.sin(theta) * radiusAtY * radius
      ),
      status: Math.random() > 0.85 ? "critical" : Math.random() > 0.7 ? "warning" : "healthy",
      speed: 0.5 + Math.random() * 1.5,
    });
  }
  return nodes;
}

function NodeNetwork({
  rotationSpeed,
  radius,
}: {
  rotationSpeed: number;
  radius: number;
}) {
  const groupRef = useRef<THREE.Group>(null!);
  const nodes = useMemo(() => generateNodes(80, radius), [radius]);

  // Pre-compute connections (connect nearby nodes)
  const connections = useMemo(() => {
    const lines: [THREE.Vector3, THREE.Vector3][] = [];
    const maxDist = radius * 0.6;
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dist = nodes[i].position.distanceTo(nodes[j].position);
        if (dist < maxDist) {
          lines.push([nodes[i].position, nodes[j].position]);
        }
      }
    }
    return lines;
  }, [nodes, radius]);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += rotationSpeed;
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.05;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Wireframe sphere */}
      <mesh>
        <sphereGeometry args={[radius, 48, 48]} />
        <meshBasicMaterial
          color="#3B82F6"
          transparent
          opacity={0.04}
          wireframe
        />
      </mesh>

      {/* Connection lines */}
      {connections.map((pair, i) => {
        const geometry = new THREE.BufferGeometry().setFromPoints(pair);
        const line = new THREE.Line(
          geometry,
          new THREE.LineBasicMaterial({ color: "#3B82F6", transparent: true, opacity: 0.08 })
        );
        return <primitive key={`conn-${i}`} object={line} />;
      })}

      {/* Nodes */}
      {nodes.map((node, i) => (
        <mesh key={`node-${i}`} position={node.position}>
          <sphereGeometry args={[0.018, 8, 8]} />
          <meshBasicMaterial
            color={
              node.status === "critical"
                ? "#EF4444"
                : node.status === "warning"
                ? "#F59E0B"
                : "#3B82F6"
            }
            transparent
            opacity={node.status === "critical" ? 0.9 : 0.6}
          />
        </mesh>
      ))}
    </group>
  );
}

// ---- Main Globe Hero ----

interface GlobeHeroProps {
  rotationSpeed?: number;
  globeRadius?: number;
  className?: string;
  children?: React.ReactNode;
}

export function GlobeHero({
  rotationSpeed = 0.003,
  globeRadius = 1.6,
  className,
  children,
}: GlobeHeroProps) {
  return (
    <div
      className={cn(
        "relative w-full min-h-screen overflow-hidden",
        className
      )}
    >
      {/* Content layer */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen">
        {children}
      </div>

      {/* 3D Canvas layer */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <Canvas
          dpr={[1, 1.5]}
          gl={{ antialias: true, alpha: true }}
          style={{ background: "transparent" }}
        >
          <PerspectiveCamera makeDefault position={[0, 0, 3.5]} fov={60} />
          <ambientLight intensity={0.3} />
          <pointLight position={[5, 5, 5]} intensity={0.5} color="#3B82F6" />
          <pointLight position={[-5, -3, 3]} intensity={0.3} color="#60A5FA" />

          <NodeNetwork rotationSpeed={rotationSpeed} radius={globeRadius} />
        </Canvas>
      </div>
    </div>
  );
}
