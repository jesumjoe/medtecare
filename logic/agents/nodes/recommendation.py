"""
Node 7: Generate Step-by-Step Recommended Maintenance Actions.
"""

from typing import Dict, Any

def generate_recommendations_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generates prioritized step-by-step action items."""
    risk_score = state.get("risk_score", 0.0)
    priority = "CRITICAL" if risk_score >= 80 else ("HIGH" if risk_score >= 60 else "MEDIUM")

    state["recommended_actions"] = [
        {
            "step": 1,
            "title": "Immediate Operating Derating",
            "description": "Derate operational load by 35-50% immediately to halt thermal friction rise.",
            "timeframe": "Immediate (< 1 hour)",
            "urgency": priority
        },
        {
            "step": 2,
            "title": "Inspect & Replace Worn Components",
            "description": "Perform full inspection of raceways/seals, flush fluid line, and replace worn assembly.",
            "timeframe": "Within 24 Hours",
            "urgency": priority
        }
    ]
    return state
