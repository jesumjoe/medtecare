"""
Node 8: Assign Maintenance Priority based on Risk Score.
"""

from typing import Dict, Any

def assign_priority_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Assigns LOW, MEDIUM, HIGH, or CRITICAL maintenance priority."""
    score = state.get("risk_score", 0.0)
    # Standardize score to 0..100 scale if given as 0..1
    if 0.0 < score <= 1.0:
        score = score * 100.0

    if score >= 80:
        state["maintenance_priority"] = "CRITICAL"
    elif score >= 60:
        state["maintenance_priority"] = "HIGH"
    elif score >= 40:
        state["maintenance_priority"] = "MEDIUM"
    else:
        state["maintenance_priority"] = "LOW"
    return state
