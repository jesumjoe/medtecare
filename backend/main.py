import sys
import os
import random
import math
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

# Ensure the parent directory is in the sys.path so we can import `logic`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from logic.integration.squad_a_adapter import adapt_squad_a_prediction
    from logic.agents.graph import DiagnosticEngine
    from logic.schemas.diagnostic import DiagnosticResult
    from backend.ml_service import ml_service
    import logging
    
    logger = logging.getLogger(__name__)
except ImportError as e:
    raise ImportError(f"Failed to import Squad B logic modules. Make sure you run this from the project root. Error: {e}")

app = FastAPI(
    title="MedTeCare Squad C API",
    description="Backend API integrating Squad A predictions with Squad B diagnostic engine.",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the diagnostic engine lazily or globally
# Instantiating globally for reuse
try:
    engine = DiagnosticEngine()
except Exception as e:
    logger.error(f"Failed to initialize DiagnosticEngine: {e}")
    engine = None

# ---- In-memory state for ticket status tracking (hackathon demo) ----
ticket_status_store: Dict[str, str] = {}
# Cache for generated alerts/tickets so they're stable across requests
_alerts_cache: Optional[List[Dict]] = None
_tickets_cache: Optional[List[Dict]] = None
_devices_cache: Optional[List[Dict]] = None

def _get_cached_devices(limit: int = 20) -> List[Dict]:
    """Get or generate cached devices for stable data across endpoints."""
    global _devices_cache
    if _devices_cache is None or len(_devices_cache) < limit:
        _devices_cache = ml_service.get_frontend_devices(limit=limit)
    return _devices_cache[:limit]

def _generate_alerts(devices: List[Dict]) -> List[Dict]:
    """Generate alerts from devices with elevated risk scores."""
    global _alerts_cache
    if _alerts_cache is not None:
        return _alerts_cache
    
    alerts = []
    risk_driver_templates = {
        "critical": [
            "Failure probability exceeds safety threshold — immediate review required",
            "Multiple prior adverse events detected — elevated future-event risk",
            "Recall history combined with high service age — critical risk profile",
        ],
        "warning": [
            "Risk score trending upward — preventative maintenance recommended",
            "Prior safety notices detected — monitoring escalation advised",
            "Service age approaching replacement threshold",
        ],
    }
    
    technicians = ["Biomed Marcus Chen", "Biomed Sarah Lopez", "Biomed James Park"]
    
    for i, device in enumerate(devices):
        if device.get("riskScore", 0) <= 40:
            continue
        
        severity = "critical" if device["riskScore"] > 75 else "high" if device["riskScore"] > 60 else "medium"
        category = "critical" if severity in ("critical", "high") else "warning"
        drivers = risk_driver_templates.get(category, risk_driver_templates["warning"])
        
        now = datetime.utcnow()
        alert = {
            "id": f"ALT-{1000 + i}",
            "equipmentId": device["id"],
            "equipmentName": device["name"],
            "riskDriver": drivers[i % len(drivers)],
            "severity": severity,
            "timestamp": (now - timedelta(minutes=random.randint(5, 720))).isoformat(),
            "status": "open",
        }
        # Assign some alerts to technicians
        if i % 3 == 0 and severity != "critical":
            alert["assignedTo"] = technicians[i % len(technicians)]
            alert["status"] = "acknowledged"
        
        alerts.append(alert)
    
    _alerts_cache = alerts
    return alerts

def _generate_tickets(devices: List[Dict]) -> List[Dict]:
    """Generate maintenance tickets from high-risk devices."""
    global _tickets_cache
    if _tickets_cache is not None:
        # Apply any status updates from the in-memory store
        for ticket in _tickets_cache:
            if ticket["id"] in ticket_status_store:
                ticket["status"] = ticket_status_store[ticket["id"]]
        return _tickets_cache
    
    tickets = []
    title_templates = [
        ("Emergency safety inspection", "Device flagged as high future-event risk by CatBoost ML model. Immediate inspection required per regulatory protocol."),
        ("Preventative maintenance review", "ML prediction indicates elevated risk. Schedule preventative maintenance and document findings."),
        ("Recall history audit", "Device has prior recall history contributing to high risk score. Verify all recall actions were completed."),
        ("Sensor calibration check", "Risk model identifies equipment age and event history as key drivers. Validate sensor accuracy."),
        ("Safety notice compliance verification", "Multiple prior safety notices on record. Verify compliance with all issued notices."),
    ]
    
    technicians = ["Biomed Marcus Chen", "Biomed Sarah Lopez", "Biomed James Park"]
    
    for i, device in enumerate(devices):
        if device.get("riskScore", 0) <= 40:
            continue
        
        priority = "critical" if device["riskScore"] > 75 else "high" if device["riskScore"] > 60 else "medium"
        title, description = title_templates[i % len(title_templates)]
        
        now = datetime.utcnow()
        ticket_id = f"TKT-{2000 + i}"
        
        # Check in-memory status store first
        status = ticket_status_store.get(ticket_id, "open")
        if status == "open" and i % 4 == 1:
            status = "in-progress"
        
        ticket = {
            "id": ticket_id,
            "equipmentId": device["id"],
            "equipmentName": device["name"],
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
            "createdAt": (now - timedelta(hours=random.randint(1, 48))).isoformat(),
            "updatedAt": (now - timedelta(minutes=random.randint(5, 300))).isoformat(),
        }
        
        # Assign some tickets to technicians
        if status == "in-progress" or (i % 3 == 0):
            ticket["assignedTechnician"] = technicians[i % len(technicians)]
        
        tickets.append(ticket)
    
    _tickets_cache = tickets
    return tickets


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/health")
async def health_check():
    """Health endpoint to verify backend status."""
    return {
        "status": "ok",
        "service": "MedTeCare Squad C Backend",
        "engine_ready": engine is not None
    }

@app.get("/api/v1/devices")
async def get_devices(limit: int = Query(default=20, ge=1, le=100)):
    """Returns a list of real medical devices from the dataset for the dashboard."""
    devices = _get_cached_devices(limit=limit)
    return {"devices": devices}

@app.get("/api/v1/devices/stats")
async def get_device_stats():
    """Returns KPI aggregate statistics computed from the full dataset."""
    stats = ml_service.get_dataset_stats()
    return stats

@app.get("/api/v1/alerts")
async def get_alerts():
    """Returns auto-generated alerts derived from ML risk predictions."""
    devices = _get_cached_devices(limit=20)
    alerts = _generate_alerts(devices)
    return {"alerts": alerts}

@app.get("/api/v1/tickets")
async def get_tickets():
    """Returns maintenance tickets derived from high-risk ML predictions."""
    devices = _get_cached_devices(limit=20)
    tickets = _generate_tickets(devices)
    return {"tickets": tickets}

@app.post("/api/v1/tickets/{ticket_id}/status")
async def update_ticket_status(ticket_id: str, request: Request):
    """Updates the status of a maintenance ticket (in-memory, demo only)."""
    try:
        req_json = await request.json()
        new_status = req_json.get("status")
        if new_status not in ("open", "in-progress", "resolved"):
            raise ValueError("status must be one of: open, in-progress, resolved")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}")
    
    ticket_status_store[ticket_id] = new_status
    
    # Update cached tickets if they exist
    global _tickets_cache
    if _tickets_cache:
        for ticket in _tickets_cache:
            if ticket["id"] == ticket_id:
                ticket["status"] = new_status
                ticket["updatedAt"] = datetime.utcnow().isoformat()
                break
    
    return {"id": ticket_id, "status": new_status, "updated": True}

@app.get("/api/v1/risk-trend")
async def get_risk_trend():
    """Returns a synthetic 30-day risk trend generated from current device risk profiles."""
    devices = _get_cached_devices(limit=20)
    if not devices:
        return {"trend": []}
    
    avg_risk = sum(d.get("riskScore", 0) for d in devices) / len(devices)
    critical_count = sum(1 for d in devices if d.get("status") == "critical")
    
    trend = []
    now = datetime.utcnow()
    for i in range(30):
        day = now - timedelta(days=29 - i)
        # Simulate a gradual trend approaching current state
        base = max(5, avg_risk - 15 + (i / 29) * 15)
        noise = random.uniform(-3, 3)
        score = round(min(100, max(0, base + noise + math.sin(i / 4) * 4)), 1)
        predicted = round(min(100, score + random.uniform(1, 5)), 1)
        trend.append({
            "date": day.strftime("%Y-%m-%d"),
            "score": score,
            "predicted": predicted,
        })
    
    return {"trend": trend}

@app.post("/api/v1/diagnose", response_model=DiagnosticResult)
async def diagnose(request: Request):
    """
    Accepts a device_id, runs real CatBoost ML prediction, and triggers Squad B workflow.
    """
    if engine is None:
        raise HTTPException(status_code=503, detail="Diagnostic Engine is not available.")
        
    try:
        req_json = await request.json()
        device_id = req_json.get("device_id")
        if not device_id:
            raise ValueError("device_id is required")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload or missing device_id.")
        
    try:
        # 1. Run live ML Inference to get Squad A payload
        squad_a_payload = ml_service.run_inference(device_id)
        if not squad_a_payload:
            raise ValueError(f"Could not generate inference for device {device_id}")

        # 2. Adapt Squad A input
        prediction = adapt_squad_a_prediction(squad_a_payload)
        
        # 3. Run Diagnostic Engine
        result = engine.analyze(prediction)
        
        # 4. Return DiagnosticResult
        return result
        
    except Exception as e:
        logger.exception("Diagnostic pipeline failed.")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "DIAGNOSTIC_FAILED",
                    "message": "Medical device diagnostic could not be completed.",
                    "details": str(e)
                }
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
