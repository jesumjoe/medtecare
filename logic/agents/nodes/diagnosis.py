"""
Node 5 & 6: Root Cause Analysis & Explanation Generation.
"""

from typing import Dict, Any
from logic.llm.diagnostic import llm_diagnostic_reasoner

def analyze_failure_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes root causes and likelihoods."""
    risk_score = state.get("risk_score", 0.0)
    state["probable_root_causes"] = [
        {
            "cause": "Mechanical Friction & Bearing Micro-Flaking",
            "likelihood": 0.88 if risk_score > 75 else 0.65,
            "description": "Vibration velocity spikes indicate inner race degradation."
        },
        {
            "cause": "Thermal Viscosity Loss & Fluid Breakdown",
            "likelihood": 0.82,
            "description": "Operating temperature elevation causing lubricant breakdown."
        }
    ]
    return state

def generate_explanation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generates structured diagnostic explanation and evidence mapping."""
    diag_res = llm_diagnostic_reasoner.synthesize_diagnosis(
        equipment_id=state["equipment_id"],
        equipment_type=state.get("equipment_type", "Industrial Machine"),
        risk_score=state.get("risk_score", 0.0),
        predicted_failure=state.get("predicted_failure", "Anomaly"),
        model_confidence=state.get("model_confidence", 0.85),
        important_features=state.get("important_features", []),
        telemetry=state.get("telemetry", []),
        retrieved_documents=state.get("retrieved_documents", []),
        historical_context=state.get("historical_context", [])
    )

    state["explanation"] = diag_res.explanation
    state["evidence"] = [e.model_dump() for e in diag_res.evidence]
    state["agent_confidence"] = diag_res.confidence
    return state
