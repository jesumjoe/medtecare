"""
Node 8: Assign Maintenance Priority based on Risk Score.
"""

from typing import Dict, Any

def assign_priority_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Assigns LOW, MEDIUM, HIGH, or CRITICAL priority for medical equipment risk assessment."""
    score = state.get("risk_score", 0.0)
    if 0.0 < score <= 1.0:
        score = score * 100.0

    risk_class = str(state.get("risk_class", "")).upper()
    recalls = state.get("previous_recalls", 0)

    # Base priority from risk score
    if score >= 80.0:
        priority = "CRITICAL"
    elif score >= 60.0:
        priority = "HIGH"
    elif score >= 40.0:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    # Priority adjustments for high-risk regulatory class or recall history
    if ("CLASS III" in risk_class or "CLASS 3" in risk_class) and priority in ["MEDIUM", "HIGH"]:
        priority = "HIGH" if priority == "MEDIUM" else "CRITICAL"
    elif recalls > 0 and priority == "LOW":
        priority = "MEDIUM"

    state["maintenance_priority"] = priority
    return state

