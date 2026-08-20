// ============================================
// MEDTECARE — STRONGLY TYPED MOCK DATA
// Backend team: swap this file's exports with
// API calls without touching component props.
// ============================================

// ---- TYPE DEFINITIONS ----

export type EquipmentStatus = "healthy" | "warning" | "critical";
export type AlertSeverity = "low" | "medium" | "high" | "critical";
export type AlertStatus = "open" | "acknowledged" | "resolved";
export type TicketStatus = "open" | "in-progress" | "resolved";
export type TicketPriority = "low" | "medium" | "high" | "critical";

export interface SensorReading {
  name: string;
  value: number;
  unit: string;
  normalRange: [number, number];
}

export interface Equipment {
  id: string;
  name: string;
  type: string;
  location: string;
  riskScore: number;
  status: EquipmentStatus;
  lastUpdated: string;
  confidencePercent: number;
  sensorReadings: SensorReading[];
  imageUrl?: string;
}

export interface Alert {
  id: string;
  equipmentId: string;
  equipmentName: string;
  riskDriver: string;
  severity: AlertSeverity;
  timestamp: string;
  status: AlertStatus;
  assignedTo?: string;
}

export interface RiskDataPoint {
  date: string;
  score: number;
  predicted: number;
}

export interface Technician {
  id: string;
  name: string;
  avatar: string;
  assignedTickets: number;
  location: string;
  specialty: string;
}

export interface MaintenanceTicket {
  id: string;
  equipmentId: string;
  equipmentName: string;
  title: string;
  description: string;
  priority: TicketPriority;
  status: TicketStatus;
  assignedTechnician?: string;
  createdAt: string;
  updatedAt: string;
}

export interface FeatureImportance {
  feature: string;
  importance: number;
  direction: "positive" | "negative";
}

export interface DiagnosticMessage {
  role: "agent" | "system";
  content: string;
  timestamp: string;
}

export interface ManualReference {
  id: string;
  title: string;
  section: string;
  excerpt: string;
  relevance: number;
}

export interface KPIData {
  label: string;
  value: number;
  change: number;
  changeLabel: string;
  sparkline: number[];
  prefix?: string;
  suffix?: string;
}

// ---- HELPER ----

function randomDate(daysBack: number): string {
  const d = new Date();
  d.setMinutes(d.getMinutes() - Math.floor(daysBack * 24 * 60));
  return d.toISOString();
}

// ---- EQUIPMENT ----

export const equipmentList: Equipment[] = [
  {
    id: "DEV-88401",
    name: "Smart Infusion Pump System",
    type: "Infusion Pump",
    location: "Cardiology Ward",
    riskScore: 87,
    status: "critical",
    lastUpdated: randomDate(0.1),
    confidencePercent: 94,
    sensorReadings: [
      { name: "Occlusion Pressure", value: 3.2, unit: "psi", normalRange: [0.5, 2.0] },
      { name: "Flow Rate Deviation", value: 4.5, unit: "%", normalRange: [0, 2] },
      { name: "Battery Health", value: 72, unit: "%", normalRange: [80, 100] },
    ],
  },
  {
    id: "DEV-99213",
    name: "Advanced Defibrillator",
    type: "Defibrillator",
    location: "Emergency Room",
    riskScore: 72,
    status: "warning",
    lastUpdated: randomDate(0.2),
    confidencePercent: 88,
    sensorReadings: [
      { name: "Capacitor Charge Time", value: 7.8, unit: "sec", normalRange: [3, 6] },
      { name: "Electrode Impedance", value: 110, unit: "ohms", normalRange: [50, 100] },
      { name: "Battery Temp", value: 42, unit: "°C", normalRange: [20, 35] },
    ],
  },
  {
    id: "DEV-44122",
    name: "Robotic Surgical Manipulator",
    type: "Surgical Robot",
    location: "Operating Room 3",
    riskScore: 15,
    status: "healthy",
    lastUpdated: randomDate(0.5),
    confidencePercent: 96,
    sensorReadings: [
      { name: "Cable Tension", value: 145, unit: "N", normalRange: [140, 150] },
      { name: "Joint Torque Error", value: 0.2, unit: "Nm", normalRange: [0, 0.5] },
      { name: "Motor Temp", value: 38, unit: "°C", normalRange: [30, 45] },
    ],
  },
  {
    id: "DEV-55341",
    name: "Mechanical Ventilator",
    type: "Ventilator",
    location: "ICU-2",
    riskScore: 45,
    status: "warning",
    lastUpdated: randomDate(0.3),
    confidencePercent: 82,
    sensorReadings: [
      { name: "Airway Pressure", value: 32, unit: "cmH2O", normalRange: [20, 30] },
      { name: "O2 Concentration Drift", value: 2.1, unit: "%", normalRange: [0, 1] },
      { name: "Exhalation Valve Temp", value: 36, unit: "°C", normalRange: [22, 35] },
    ],
  },
  {
    id: "DEV-77291",
    name: "MRI Scanner 3T",
    type: "MRI Machine",
    location: "Radiology",
    riskScore: 8,
    status: "healthy",
    lastUpdated: randomDate(1),
    confidencePercent: 98,
    sensorReadings: [
      { name: "Helium Level", value: 85, unit: "%", normalRange: [70, 100] },
      { name: "Magnet Temp", value: 4.2, unit: "K", normalRange: [4.1, 4.3] },
      { name: "Gradient Coil Voltage", value: 120, unit: "V", normalRange: [110, 130] },
    ],
  },
  {
    id: "DEV-11932",
    name: "Patient Monitor Vitals",
    type: "Vital Signs Monitor",
    location: "Ward 4",
    riskScore: 91,
    status: "critical",
    lastUpdated: randomDate(0.05),
    confidencePercent: 97,
    sensorReadings: [
      { name: "ECG Noise Level", value: 12.3, unit: "mV", normalRange: [0, 5] },
      { name: "SpO2 Sensor Drift", value: 4.5, unit: "%", normalRange: [0, 2] },
      { name: "Battery Level", value: 15, unit: "%", normalRange: [20, 100] },
    ],
  }
];

// ---- ALERTS ----

export const alertsList: Alert[] = [
  {
    id: "ALT-001",
    equipmentId: "DEV-88401",
    equipmentName: "Smart Infusion Pump System",
    riskDriver: "Occlusion pressure sensor drift — potential under-delivery",
    severity: "critical",
    timestamp: randomDate(0.01),
    status: "open",
  },
  {
    id: "ALT-002",
    equipmentId: "DEV-11932",
    equipmentName: "Patient Monitor Vitals",
    riskDriver: "High ECG noise detected — cable failure imminent",
    severity: "critical",
    timestamp: randomDate(0.02),
    status: "open",
  },
  {
    id: "ALT-003",
    equipmentId: "DEV-99213",
    equipmentName: "Advanced Defibrillator",
    riskDriver: "Capacitor charge time degradation detected",
    severity: "high",
    timestamp: randomDate(0.08),
    status: "open",
  },
  {
    id: "ALT-004",
    equipmentId: "DEV-55341",
    equipmentName: "Mechanical Ventilator",
    riskDriver: "O2 concentration sensor drift above 2%",
    severity: "medium",
    timestamp: randomDate(0.1),
    status: "acknowledged",
    assignedTo: "Dr. Marcus Chen",
  }
];

// ---- RISK TREND (30-day) ----

export const riskTrendData: RiskDataPoint[] = Array.from({ length: 30 }, (_, i) => {
  const d = new Date();
  d.setDate(d.getDate() - (29 - i));
  const base = 28 + Math.sin(i / 4) * 8 + (i > 20 ? (i - 20) * 1.5 : 0);
  return {
    date: d.toISOString().split("T")[0],
    score: Math.round(base + (Math.random() - 0.5) * 6),
    predicted: Math.round(base + 3 + (Math.random() - 0.5) * 4),
  };
});

// ---- TECHNICIANS ----

export const techniciansList: Technician[] = [
  { id: "TECH-001", name: "Biomed Marcus Chen", avatar: "MC", assignedTickets: 3, location: "Main Hospital", specialty: "Infusion & Vitals" },
  { id: "TECH-002", name: "Biomed Sarah Lopez", avatar: "SL", assignedTickets: 2, location: "Radiology", specialty: "Imaging" },
  { id: "TECH-003", name: "Biomed James Park", avatar: "JP", assignedTickets: 4, location: "OR & ICU", specialty: "Robotics & Vent" },
];

// ---- MAINTENANCE TICKETS ----

export const ticketsList: MaintenanceTicket[] = [
  {
    id: "TKT-001",
    equipmentId: "DEV-88401",
    equipmentName: "Smart Infusion Pump System",
    title: "Emergency sensor calibration",
    description: "Occlusion pressure sensor out of bounds. Recalibrate to prevent fatal dosing errors.",
    priority: "critical",
    status: "open",
    createdAt: randomDate(0.01),
    updatedAt: randomDate(0.01),
  },
  {
    id: "TKT-002",
    equipmentId: "DEV-11932",
    equipmentName: "Patient Monitor Vitals",
    title: "ECG module replacement",
    description: "Consistent high noise level in ECG readings. Replace trunk cable and module.",
    priority: "critical",
    status: "open",
    createdAt: randomDate(0.02),
    updatedAt: randomDate(0.02),
  },
  {
    id: "TKT-003",
    equipmentId: "DEV-99213",
    equipmentName: "Advanced Defibrillator",
    title: "Capacitor replacement",
    description: "Charge time exceeded 7s limit. Preventative maintenance required for capacitor bank.",
    priority: "high",
    status: "in-progress",
    assignedTechnician: "Biomed Sarah Lopez",
    createdAt: randomDate(0.1),
    updatedAt: randomDate(0.05),
  },
];

// ---- KPI DATA ----

export const kpiData: KPIData[] = [
  {
    label: "Total Medical Devices",
    value: 1270,
    change: 4,
    changeLabel: "new this month",
    sparkline: [1210, 1220, 1235, 1250, 1260, 1265, 1268, 1270],
  },
  {
    label: "Devices at Risk",
    value: 12,
    change: -3,
    changeLabel: "vs last month",
    sparkline: [18, 16, 19, 21, 20, 15, 14, 12],
    suffix: "",
  },
  {
    label: "Predicted Failures (30d)",
    value: 2,
    change: -5,
    changeLabel: "vs last month",
    sparkline: [12, 11, 10, 9, 7, 5, 4, 2],
  },
  {
    label: "Avg Risk Score",
    value: 14.2,
    change: -2.3,
    changeLabel: "vs last month",
    sparkline: [20, 19, 18, 17, 16, 15, 14, 14.2],
  },
];

// ---- FEATURE IMPORTANCE (SHAP-style) ----

export const featureImportanceData: FeatureImportance[] = [
  { feature: "Occlusion Pressure", importance: 0.42, direction: "positive" },
  { feature: "Battery Health", importance: 0.28, direction: "positive" },
  { feature: "Operating Hours", importance: 0.15, direction: "positive" },
  { feature: "Flow Rate Accuracy", importance: -0.12, direction: "negative" },
  { feature: "Last Maintenance", importance: -0.05, direction: "negative" },
];

// ---- DIAGNOSTIC MESSAGES ----

export const diagnosticMessages: DiagnosticMessage[] = [
  {
    role: "system",
    content: "Diagnostic analysis initiated for Smart Infusion Pump System (DEV-88401)",
    timestamp: new Date(Date.now() - 120000).toISOString(),
  },
  {
    role: "agent",
    content: `## Diagnostic Summary — Smart Infusion Pump System
    
**Risk Assessment: CRITICAL (87/100)**

I've analyzed the sensor telemetry data and identified a compound failure pattern:

1. **Primary concern — Pressure Sensor Drift**: Readings have deviated beyond acceptable safety margins (3.2 psi vs normal max of 2.0 psi).

2. **Secondary concern — Battery Health**: Battery capacity has dropped to 72%, risking sudden shutdown during patient transport.

3. **Recommended actions**:
   - **Immediate**: Remove device from clinical use.
   - **Within 24h**: Recalibrate occlusion sensors and replace main battery pack.

**Confidence**: 94% based on historical FDA MAUDE adverse event reports.`,
    timestamp: new Date(Date.now() - 60000).toISOString(),
  },
];

// ---- MANUAL REFERENCES ----

export const manualReferences: ManualReference[] = [
  {
    id: "REF-001",
    title: "Infusion Pump Service Manual",
    section: "Section 7.3: Sensor Recalibration",
    excerpt: "When occlusion pressure exceeds 2.5 psi without tubing blockages, sensor recalibration is required to prevent over-infusion...",
    relevance: 0.96,
  },
  {
    id: "REF-002",
    title: "FDA MAUDE Database",
    section: "Report 2024-001X",
    excerpt: "Battery degradation below 80% led to unexpected shutdown during patient transport. Preventative replacement advised...",
    relevance: 0.91,
  },
];

// ---- UTILITY FUNCTIONS ----

export function getStatusColor(status: EquipmentStatus): string {
  switch (status) {
    case "healthy":
      return "var(--sentinel-healthy)";
    case "warning":
      return "var(--sentinel-warning)";
    case "critical":
      return "var(--sentinel-critical)";
  }
}

export function getStatusColorClass(status: EquipmentStatus): string {
  switch (status) {
    case "healthy":
      return "text-sentinel-healthy";
    case "warning":
      return "text-sentinel-warning";
    case "critical":
      return "text-sentinel-critical";
  }
}

export function getStatusBgClass(status: EquipmentStatus): string {
  switch (status) {
    case "healthy":
      return "bg-sentinel-healthy/15 text-sentinel-healthy border-sentinel-healthy/30";
    case "warning":
      return "bg-sentinel-warning/15 text-sentinel-warning border-sentinel-warning/30";
    case "critical":
      return "bg-sentinel-critical/15 text-sentinel-critical border-sentinel-critical/30";
  }
}

export function getSeverityBgClass(severity: AlertSeverity): string {
  switch (severity) {
    case "low":
      return "bg-sentinel-healthy/15 text-sentinel-healthy border-sentinel-healthy/30";
    case "medium":
      return "bg-sentinel-blue/15 text-sentinel-blue-light border-sentinel-blue/30";
    case "high":
      return "bg-sentinel-warning/15 text-sentinel-warning border-sentinel-warning/30";
    case "critical":
      return "bg-sentinel-critical/15 text-sentinel-critical border-sentinel-critical/30";
  }
}

export function getPriorityBgClass(priority: TicketPriority): string {
  return getSeverityBgClass(priority as AlertSeverity);
}

export function formatRelativeTime(isoString: string): string {
  const now = Date.now();
  const diff = now - new Date(isoString).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}
