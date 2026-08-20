"use client";

import React, { useState, useEffect } from "react";
import { FleetGrid } from "@/components/dashboard/fleet-grid";
import { equipmentList as mockEquipmentList } from "@/lib/mock-data";
import type { Equipment } from "@/lib/mock-data";
import { fetchDevices } from "@/lib/api";

export default function FleetPage() {
  const [equipmentList, setEquipmentList] = useState<Equipment[]>(mockEquipmentList);

  useEffect(() => {
    fetchDevices(50).then((devices) => {
      if (devices.length > 0) {
        setEquipmentList(devices);
      }
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Fleet</h1>
        <p className="text-sm text-muted-foreground">
          All monitored equipment across your plants
        </p>
      </div>
      <FleetGrid equipment={equipmentList} />
    </div>
  );
}

