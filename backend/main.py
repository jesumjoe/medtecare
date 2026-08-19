import sys
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

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

@app.get("/health")
async def health_check():
    """Health endpoint to verify backend status."""
    return {
        "status": "ok",
        "service": "MedTeCare Squad C Backend",
        "engine_ready": engine is not None
    }

@app.get("/api/v1/devices")
async def get_devices():
    """Returns a list of real medical devices from the dataset for the dashboard."""
    devices = ml_service.get_frontend_devices(limit=10)
    return {"devices": devices}

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
