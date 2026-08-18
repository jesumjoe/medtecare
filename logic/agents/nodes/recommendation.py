"""
Node 7: Generate Step-by-Step Recommended Maintenance Actions.
"""

from typing import Dict, Any

def generate_recommendations_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generates prioritized medical equipment risk mitigation action items."""
    risk_score = state.get("risk_score", 0.0)
    priority = "CRITICAL" if risk_score >= 80 else ("HIGH" if risk_score >= 60 else "MEDIUM")

    state["recommended_actions"] = [
        {
            "step": 1,
            "title": "Safety & Operational Review",
            "description": "Perform immediate safety review and prioritize routine preventative maintenance inspection for this medical device.",
            "timeframe": "Immediate (< 4 hours)",
            "urgency": priority
        },
        {
            "step": 2,
            "title": "Historical Event & Safety Notice Audit",
            "description": "Cross-reference device serial/model against manufacturer safety notices, historical adverse event logs, and prior recall Bulletins.",
            "timeframe": "Within 24 Hours",
            "urgency": priority
        },
        {
            "step": 3,
            "title": "Increased Diagnostic Monitoring & Escalation",
            "description": "Increase clinical operational monitoring and escalate device assessment to certified biomedical engineering staff prior to high-acuity deployment.",
            "timeframe": "Within 48 Hours",
            "urgency": priority
        }
    ]
    return state

