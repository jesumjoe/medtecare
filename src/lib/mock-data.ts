// ============================================
// SENTINELOPS — STRONGLY TYPED MOCK DATA
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
  d.setMinutes(d.getMinutes() - Math.floor(Math.random() * daysBack * 24 * 60));
  return d.toISOString();
}

// ---- EQUIPMENT ----

export const equipmentList: Equipment[] = [
  {
    id: "EQ-001",
    name: "CNC Mill Alpha-7",
    type: "CNC Milling Machine",
    location: "Plant A — Bay 3",
    riskScore: 87,
    status: "critical",
    lastUpdated: randomDate(0.1),
    confidencePercent: 94,
    sensorReadings: [
      { name: "Bearing Temp", value: 112, unit: "°C", normalRange: [40, 85] },
      { name: "Vibration RMS", value: 8.7, unit: "mm/s", normalRange: [0, 4.5] },
      { name: "Spindle Load", value: 91, unit: "%", normalRange: [0, 80] },
    ],
  },
  {
    id: "EQ-002",
    name: "Hydraulic Press B-12",
    type: "Hydraulic Press",
    location: "Plant A — Bay 1",
    riskScore: 72,
    status: "warning",
    lastUpdated: randomDate(0.2),
    confidencePercent: 88,
    sensorReadings: [
      { name: "Oil Viscosity", value: 28, unit: "cSt", normalRange: [32, 68] },
      { name: "Cylinder Pressure", value: 3200, unit: "PSI", normalRange: [1000, 3000] },
      { name: "Oil Temp", value: 78, unit: "°C", normalRange: [30, 70] },
    ],
  },
  {
    id: "EQ-003",
    name: "Conveyor Line C-04",
    type: "Belt Conveyor",
    location: "Plant B — Zone 2",
    riskScore: 15,
    status: "healthy",
    lastUpdated: randomDate(0.5),
    confidencePercent: 96,
    sensorReadings: [
      { name: "Belt Tension", value: 450, unit: "N", normalRange: [400, 600] },
      { name: "Motor Temp", value: 52, unit: "°C", normalRange: [30, 75] },
      { name: "Speed", value: 1.8, unit: "m/s", normalRange: [1.5, 2.5] },
    ],
  },
  {
    id: "EQ-004",
    name: "Welding Robot WR-09",
    type: "Robotic Welder",
    location: "Plant A — Bay 5",
    riskScore: 45,
    status: "warning",
    lastUpdated: randomDate(0.3),
    confidencePercent: 82,
    sensorReadings: [
      { name: "Joint Torque", value: 78, unit: "Nm", normalRange: [20, 70] },
      { name: "Wire Feed Rate", value: 6.2, unit: "m/min", normalRange: [5, 8] },
      { name: "Arc Voltage", value: 24.5, unit: "V", normalRange: [22, 28] },
    ],
  },
  {
    id: "EQ-005",
    name: "Compressor Unit D-01",
    type: "Air Compressor",
    location: "Plant B — Utility Room",
    riskScore: 8,
    status: "healthy",
    lastUpdated: randomDate(1),
    confidencePercent: 98,
    sensorReadings: [
      { name: "Discharge Pressure", value: 125, unit: "PSI", normalRange: [100, 150] },
      { name: "Motor Current", value: 42, unit: "A", normalRange: [30, 55] },
      { name: "Intake Temp", value: 28, unit: "°C", normalRange: [15, 35] },
    ],
  },
  {
    id: "EQ-006",
    name: "Lathe Machine L-03",
    type: "CNC Lathe",
    location: "Plant A — Bay 2",
    riskScore: 91,
    status: "critical",
    lastUpdated: randomDate(0.05),
    confidencePercent: 97,
    sensorReadings: [
      { name: "Spindle Vibration", value: 12.3, unit: "mm/s", normalRange: [0, 5] },
      { name: "Coolant Flow", value: 1.2, unit: "L/min", normalRange: [3, 8] },
      { name: "Chuck Pressure", value: 18, unit: "bar", normalRange: [20, 35] },
    ],
  },
  {
    id: "EQ-007",
    name: "Injection Molder IM-15",
    type: "Injection Molding",
    location: "Plant C — Hall 1",
    riskScore: 22,
    status: "healthy",
    lastUpdated: randomDate(0.8),
    confidencePercent: 91,
    sensorReadings: [
      { name: "Barrel Temp", value: 215, unit: "°C", normalRange: [200, 240] },
      { name: "Clamping Force", value: 850, unit: "kN", normalRange: [700, 1000] },
      { name: "Cycle Time", value: 32, unit: "s", normalRange: [28, 38] },
    ],
  },
  {
    id: "EQ-008",
    name: "Packaging Robot PR-06",
    type: "Pick-and-Place Robot",
    location: "Plant B — Zone 4",
    riskScore: 58,
    status: "warning",
    lastUpdated: randomDate(0.4),
    confidencePercent: 79,
    sensorReadings: [
      { name: "Gripper Force", value: 42, unit: "N", normalRange: [30, 50] },
      { name: "Arm Position Error", value: 2.1, unit: "mm", normalRange: [0, 1] },
      { name: "Cycle Count", value: 487000, unit: "cycles", normalRange: [0, 500000] },
    ],
  },
  {
    id: "EQ-009",
    name: "Furnace Unit F-02",
    type: "Industrial Furnace",
    location: "Plant C — Heat Treatment",
    riskScore: 34,
    status: "healthy",
    lastUpdated: randomDate(0.6),
    confidencePercent: 93,
    sensorReadings: [
      { name: "Chamber Temp", value: 850, unit: "°C", normalRange: [800, 900] },
      { name: "Gas Flow", value: 12.5, unit: "m³/h", normalRange: [10, 15] },
      { name: "Exhaust Temp", value: 310, unit: "°C", normalRange: [250, 350] },
    ],
  },
  {
    id: "EQ-010",
    name: "Cooling Tower CT-01",
    type: "Cooling System",
    location: "Plant A — Rooftop",
    riskScore: 12,
    status: "healthy",
    lastUpdated: randomDate(2),
    confidencePercent: 95,
    sensorReadings: [
      { name: "Water Temp Out", value: 28, unit: "°C", normalRange: [22, 32] },
      { name: "Fan Speed", value: 1200, unit: "RPM", normalRange: [800, 1500] },
      { name: "Water Level", value: 82, unit: "%", normalRange: [60, 100] },
    ],
  },
  {
    id: "EQ-011",
    name: "Generator GEN-04",
    type: "Diesel Generator",
    location: "Plant B — Power House",
    riskScore: 65,
    status: "warning",
    lastUpdated: randomDate(0.3),
    confidencePercent: 86,
    sensorReadings: [
      { name: "Engine Temp", value: 95, unit: "°C", normalRange: [60, 90] },
      { name: "Fuel Consumption", value: 45, unit: "L/h", normalRange: [30, 42] },
      { name: "Output Voltage", value: 398, unit: "V", normalRange: [395, 415] },
    ],
  },
  {
    id: "EQ-012",
    name: "AGV Transport T-08",
    type: "Automated Guided Vehicle",
    location: "Plant A — Warehouse",
    riskScore: 19,
    status: "healthy",
    lastUpdated: randomDate(0.7),
    confidencePercent: 92,
    sensorReadings: [
      { name: "Battery Level", value: 78, unit: "%", normalRange: [20, 100] },
      { name: "Motor Temp", value: 45, unit: "°C", normalRange: [25, 65] },
      { name: "Navigation Accuracy", value: 0.3, unit: "cm", normalRange: [0, 1] },
    ],
  },
];

// ---- ALERTS ----

export const alertsList: Alert[] = [
  {
    id: "ALT-001",
    equipmentId: "EQ-001",
    equipmentName: "CNC Mill Alpha-7",
    riskDriver: "Bearing temperature anomaly — exceeded 110°C threshold",
    severity: "critical",
    timestamp: randomDate(0.01),
    status: "open",
  },
  {
    id: "ALT-002",
    equipmentId: "EQ-006",
    equipmentName: "Lathe Machine L-03",
    riskDriver: "Coolant flow critically low — potential spindle damage",
    severity: "critical",
    timestamp: randomDate(0.02),
    status: "open",
  },
  {
    id: "ALT-003",
    equipmentId: "EQ-002",
    equipmentName: "Hydraulic Press B-12",
    riskDriver: "Oil viscosity degradation detected — recommend replacement",
    severity: "high",
    timestamp: randomDate(0.08),
    status: "open",
  },
  {
    id: "ALT-004",
    equipmentId: "EQ-008",
    equipmentName: "Packaging Robot PR-06",
    riskDriver: "Arm position error exceeding tolerance (2.1mm vs 1mm limit)",
    severity: "high",
    timestamp: randomDate(0.1),
    status: "acknowledged",
    assignedTo: "Marcus Chen",
  },
  {
    id: "ALT-005",
    equipmentId: "EQ-011",
    equipmentName: "Generator GEN-04",
    riskDriver: "Fuel consumption 7% above baseline — possible injector issue",
    severity: "medium",
    timestamp: randomDate(0.2),
    status: "acknowledged",
    assignedTo: "Sarah Lopez",
  },
  {
    id: "ALT-006",
    equipmentId: "EQ-004",
    equipmentName: "Welding Robot WR-09",
    riskDriver: "Joint torque drift detected — recalibration recommended",
    severity: "medium",
    timestamp: randomDate(0.3),
    status: "open",
  },
  {
    id: "ALT-007",
    equipmentId: "EQ-001",
    equipmentName: "CNC Mill Alpha-7",
    riskDriver: "Vibration RMS trending upward — bearing wear pattern",
    severity: "high",
    timestamp: randomDate(0.5),
    status: "acknowledged",
    assignedTo: "James Park",
  },
  {
    id: "ALT-008",
    equipmentId: "EQ-006",
    equipmentName: "Lathe Machine L-03",
    riskDriver: "Chuck pressure below minimum — workpiece ejection risk",
    severity: "critical",
    timestamp: randomDate(0.04),
    status: "open",
  },
  {
    id: "ALT-009",
    equipmentId: "EQ-009",
    equipmentName: "Furnace Unit F-02",
    riskDriver: "Minor thermocouple drift — scheduled recalibration",
    severity: "low",
    timestamp: randomDate(1),
    status: "resolved",
    assignedTo: "Emily Zhao",
  },
  {
    id: "ALT-010",
    equipmentId: "EQ-003",
    equipmentName: "Conveyor Line C-04",
    riskDriver: "Routine belt tension adjustment completed",
    severity: "low",
    timestamp: randomDate(2),
    status: "resolved",
    assignedTo: "Marcus Chen",
  },
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
  { id: "TECH-001", name: "Marcus Chen", avatar: "MC", assignedTickets: 3, location: "Plant A", specialty: "CNC & Robotics" },
  { id: "TECH-002", name: "Sarah Lopez", avatar: "SL", assignedTickets: 2, location: "Plant B", specialty: "Hydraulics" },
  { id: "TECH-003", name: "James Park", avatar: "JP", assignedTickets: 4, location: "Plant A", specialty: "Electrical Systems" },
  { id: "TECH-004", name: "Emily Zhao", avatar: "EZ", assignedTickets: 1, location: "Plant C", specialty: "Heat Treatment" },
  { id: "TECH-005", name: "David Okoye", avatar: "DO", assignedTickets: 2, location: "Plant B", specialty: "Automation" },
];

// ---- MAINTENANCE TICKETS ----

export const ticketsList: MaintenanceTicket[] = [
  {
    id: "TKT-001",
    equipmentId: "EQ-001",
    equipmentName: "CNC Mill Alpha-7",
    title: "Emergency bearing replacement",
    description: "Bearing temperature exceeded critical threshold. Immediate replacement required to prevent spindle seizure.",
    priority: "critical",
    status: "open",
    createdAt: randomDate(0.01),
    updatedAt: randomDate(0.01),
  },
  {
    id: "TKT-002",
    equipmentId: "EQ-006",
    equipmentName: "Lathe Machine L-03",
    title: "Coolant system overhaul",
    description: "Coolant flow rate critically low. Inspect pump, filters, and distribution lines.",
    priority: "critical",
    status: "open",
    createdAt: randomDate(0.02),
    updatedAt: randomDate(0.02),
  },
  {
    id: "TKT-003",
    equipmentId: "EQ-002",
    equipmentName: "Hydraulic Press B-12",
    title: "Hydraulic oil replacement",
    description: "Oil viscosity below operational range. Schedule full fluid change and filter replacement.",
    priority: "high",
    status: "in-progress",
    assignedTechnician: "Sarah Lopez",
    createdAt: randomDate(0.1),
    updatedAt: randomDate(0.05),
  },
  {
    id: "TKT-004",
    equipmentId: "EQ-008",
    equipmentName: "Packaging Robot PR-06",
    title: "Arm calibration & servo check",
    description: "Position error exceeding tolerance. Recalibrate arm and inspect servo motors.",
    priority: "high",
    status: "in-progress",
    assignedTechnician: "Marcus Chen",
    createdAt: randomDate(0.15),
    updatedAt: randomDate(0.08),
  },
  {
    id: "TKT-005",
    equipmentId: "EQ-011",
    equipmentName: "Generator GEN-04",
    title: "Fuel injector inspection",
    description: "Above-baseline fuel consumption suggests injector degradation. Inspect and clean or replace.",
    priority: "medium",
    status: "in-progress",
    assignedTechnician: "Sarah Lopez",
    createdAt: randomDate(0.2),
    updatedAt: randomDate(0.1),
  },
  {
    id: "TKT-006",
    equipmentId: "EQ-004",
    equipmentName: "Welding Robot WR-09",
    title: "Joint recalibration",
    description: "Torque drift on axis 3. Perform full joint recalibration per manufacturer spec.",
    priority: "medium",
    status: "open",
    createdAt: randomDate(0.3),
    updatedAt: randomDate(0.3),
  },
  {
    id: "TKT-007",
    equipmentId: "EQ-009",
    equipmentName: "Furnace Unit F-02",
    title: "Thermocouple recalibration",
    description: "Minor drift detected in zone 2 thermocouple. Scheduled recalibration completed.",
    priority: "low",
    status: "resolved",
    assignedTechnician: "Emily Zhao",
    createdAt: randomDate(3),
    updatedAt: randomDate(1),
  },
  {
    id: "TKT-008",
    equipmentId: "EQ-003",
    equipmentName: "Conveyor Line C-04",
    title: "Belt tension adjustment",
    description: "Routine preventive maintenance — belt tension adjusted to specification.",
    priority: "low",
    status: "resolved",
    assignedTechnician: "Marcus Chen",
    createdAt: randomDate(5),
    updatedAt: randomDate(2),
  },
  {
    id: "TKT-009",
    equipmentId: "EQ-010",
    equipmentName: "Cooling Tower CT-01",
    title: "Water treatment chemical refill",
    description: "Biocide and scale inhibitor levels low. Refill chemical dosing system.",
    priority: "low",
    status: "resolved",
    assignedTechnician: "David Okoye",
    createdAt: randomDate(7),
    updatedAt: randomDate(3),
  },
  {
    id: "TKT-010",
    equipmentId: "EQ-001",
    equipmentName: "CNC Mill Alpha-7",
    title: "Vibration analysis follow-up",
    description: "Follow-up inspection after vibration RMS alert. Monitor bearing degradation pattern.",
    priority: "high",
    status: "in-progress",
    assignedTechnician: "James Park",
    createdAt: randomDate(0.5),
    updatedAt: randomDate(0.2),
  },
];

// ---- KPI DATA ----

export const kpiData: KPIData[] = [
  {
    label: "Total Assets",
    value: 127,
    change: 4,
    changeLabel: "new this month",
    sparkline: [110, 112, 115, 118, 120, 122, 124, 127],
  },
  {
    label: "Assets at Risk",
    value: 23,
    change: 12,
    changeLabel: "vs last month",
    sparkline: [18, 16, 19, 21, 20, 22, 24, 23],
    suffix: "",
  },
  {
    label: "Predicted Failures (30d)",
    value: 8,
    change: -25,
    changeLabel: "vs last month",
    sparkline: [12, 11, 10, 9, 11, 10, 9, 8],
  },
  {
    label: "Avg Risk Score",
    value: 34.2,
    change: 5.3,
    changeLabel: "vs last month",
    sparkline: [30, 29, 31, 32, 33, 31, 33, 34.2],
  },
];

// ---- FEATURE IMPORTANCE (SHAP-style) ----

export const featureImportanceData: FeatureImportance[] = [
  { feature: "Bearing Temperature", importance: 0.42, direction: "positive" },
  { feature: "Vibration RMS", importance: 0.28, direction: "positive" },
  { feature: "Operating Hours", importance: 0.15, direction: "positive" },
  { feature: "Oil Viscosity", importance: -0.12, direction: "negative" },
  { feature: "Ambient Temperature", importance: 0.08, direction: "positive" },
  { feature: "Load Percentage", importance: 0.06, direction: "positive" },
  { feature: "Last Maintenance", importance: -0.05, direction: "negative" },
  { feature: "Coolant Flow Rate", importance: -0.04, direction: "negative" },
];

// ---- DIAGNOSTIC MESSAGES ----

export const diagnosticMessages: DiagnosticMessage[] = [
  {
    role: "system",
    content: "Diagnostic analysis initiated for CNC Mill Alpha-7 (EQ-001)",
    timestamp: new Date(Date.now() - 120000).toISOString(),
  },
  {
    role: "agent",
    content: `## Diagnostic Summary — CNC Mill Alpha-7

**Risk Assessment: CRITICAL (87/100)**

I've analyzed the sensor telemetry data from the last 72 hours and identified a compound failure pattern:

1. **Primary concern — Bearing degradation**: Temperature readings have increased 34% over 48 hours (78°C → 112°C), following a classic exponential wear curve. Vibration RMS confirms this at 8.7 mm/s (threshold: 4.5 mm/s).

2. **Secondary concern — Spindle overload**: Load has been sustained above 90% for the past 6 production cycles. Combined with bearing degradation, this creates a cascading failure risk.

3. **Recommended actions**:
   - **Immediate**: Reduce spindle speed by 40% and cease heavy-cut operations
   - **Within 24h**: Replace main spindle bearings (SKF 7208 BECBP or equivalent)
   - **Within 48h**: Full spindle alignment check post-replacement

**Confidence**: 94% based on historical failure patterns from 12 similar units across your fleet.`,
    timestamp: new Date(Date.now() - 60000).toISOString(),
  },
];

// ---- MANUAL REFERENCES ----

export const manualReferences: ManualReference[] = [
  {
    id: "REF-001",
    title: "CNC Mill Maintenance Manual — Rev 4.2",
    section: "Section 7.3: Spindle Bearing Replacement Procedure",
    excerpt: "When bearing temperature exceeds 100°C during normal operation, immediate inspection is required. Follow lockout/tagout procedure (Sec 2.1) before disassembly...",
    relevance: 0.96,
  },
  {
    id: "REF-002",
    title: "SKF Bearing Technical Handbook",
    section: "Chapter 14: Vibration Analysis for Rolling Bearings",
    excerpt: "RMS velocity values above 7.1 mm/s indicate severe bearing damage (ISO 10816-3 Zone D). Immediate corrective action is recommended to prevent catastrophic failure...",
    relevance: 0.91,
  },
  {
    id: "REF-003",
    title: "Predictive Maintenance Best Practices — SMRP Guide",
    section: "Section 5.2: Thermal Analysis Decision Trees",
    excerpt: "A temperature rise rate exceeding 15°C/day in rotating equipment bearings indicates accelerated wear. Cross-reference with vibration spectrum data for confirmation...",
    relevance: 0.84,
  },
  {
    id: "REF-004",
    title: "OEM Service Bulletin SB-2024-017",
    section: "Spindle Load Derating Guidelines",
    excerpt: "Under sustained loads above 85% capacity, reduce continuous operation time by 30% and increase inspection frequency to every 200 operating hours...",
    relevance: 0.78,
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
