"""
Node 5 & 6: Root Cause Analysis & Explanation Generation.
"""

from typing import Dict, Any
from logic.llm.diagnostic import llm_diagnostic_reasoner

def analyze_failure_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes probable medical device future-event risk factors based on model probability and historical drivers."""
    risk_score = state.get("risk_score", 0.0)
    recalls = state.get("previous_recalls", 0)
    years = state.get("years_in_service", 0.0)
    prob = risk_score / 100.0

    root_causes = [
        {
            "cause": "Historical Safety Notice & Event Pattern Alignment",
            "likelihood": round(min(0.95, prob * 1.05), 2),
            "description": f"Predicted future-event probability ({prob:.2f}) indicates strong correlation with historical safety records and past event frequency."
        },
        {
            "cause": "Operational Service Longevity & Lifecycle Degradation Risk",
            "likelihood": round(min(0.90, 0.50 + (years * 0.05)), 2),
            "description": f"Device operational age of {years:.1f} years contributes to elevated cumulative future-event risk."
        }
    ]
    if recalls > 0:
        root_causes.append({
            "cause": "Manufacturer Recall Recurrence Susceptibility",
            "likelihood": 0.85,
            "description": f"Device has {recalls} previous recall record(s) on file, contributing to heightened risk score."
        })

    state["probable_root_causes"] = root_causes
    return state


def generate_explanation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generates structured diagnostic explanation and evidence mapping."""
    diag_res = llm_diagnostic_reasoner.synthesize_diagnosis(
        equipment_id=state.get("device_id") or state.get("equipment_id", "DEV-88401"),
        equipment_type=state.get("device_name") or state.get("equipment_type", "Medical Equipment"),
        risk_score=state.get("risk_score", 0.0),
        predicted_failure=state.get("predicted_failure", "medical-device future-event risk"),
        model_confidence=state.get("model_confidence", 0.85),
        important_features=state.get("important_features", []),
        telemetry=state.get("telemetry", []),
        retrieved_documents=state.get("retrieved_documents", []),
        historical_context=state.get("historical_context", []),
        device_context=state
    )

    state["explanation"] = diag_res.explanation
    state["evidence"] = [e.model_dump() for e in diag_res.evidence]
    state["agent_confidence"] = diag_res.confidence
    return state

