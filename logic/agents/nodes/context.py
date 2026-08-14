"""
Node 2: Build Diagnostic Telemetry Context.
"""

from typing import Dict, Any

def build_context_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Assembles telemetry metrics and key anomaly feature drivers."""
    telemetry = state.get("telemetry", [])
    important_features = state.get("important_features", [])

    context = (
        f"Equipment {state['equipment_id']} ({state['equipment_type']}) - "
        f"Predicted Failure: {state['predicted_failure']}. "
        f"Key Feature Drivers: {', '.join(important_features)}. Telemetry Count: {len(telemetry)}"
    )
    state["diagnostic_findings"] = context
    return state
