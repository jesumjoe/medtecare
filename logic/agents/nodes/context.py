"""
Node 2: Build Diagnostic Telemetry Context.
"""

from typing import Dict, Any

def build_context_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Assembles medical device context, historical event counts, and key SHAP feature drivers."""
    dev_id = state.get("device_id") or state.get("equipment_id", "DEV-88401")
    dev_name = state.get("device_name") or state.get("equipment_type", "Medical Equipment")
    classification = state.get("classification", "Medical Device")
    risk_class = state.get("risk_class", "Class II")
    manufacturer = state.get("manufacturer", "OEM Manufacturer")
    recalls = state.get("previous_recalls", 0)
    events = state.get("previous_events", 0)
    notices = state.get("previous_safety_notices", 0)
    years = state.get("years_in_service", 0.0)
    important_features = state.get("important_features", [])

    drivers_str = ", ".join(important_features) if important_features else "None reported"

    context = (
        f"Medical Device {dev_id} ({dev_name}) | Classification: {classification} | Risk Class: {risk_class} | "
        f"Manufacturer: {manufacturer} | Operational Age: {years:.1f} years. "
        f"Historical Metrics: Recalls: {recalls}, Adverse Events: {events}, Safety Notices: {notices}. "
        f"Squad A Model Assessment: {state.get('predicted_failure', 'medical-device future-event risk')} "
        f"(Probability: {state.get('risk_score', 0.0)/100.0:.2f}). "
        f"Key SHAP Feature Drivers: {drivers_str}."
    )
    state["diagnostic_findings"] = context
    return state

