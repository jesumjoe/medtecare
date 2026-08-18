"""
LangGraph State Graph Workflow & DiagnosticEngine Integration Interface.

Squad C Integration Interface:
  from logic.agents.graph import DiagnosticEngine
  engine = DiagnosticEngine()
  result: DiagnosticResult = engine.analyze(prediction)
"""

from typing import Dict, Any, Union
import logging

from langgraph.graph import StateGraph, END, START
from logic.schemas.prediction import MLPrediction
from logic.schemas.diagnostic import (
    DiagnosticResult, ProbableRootCause, EvidenceCategory, RecommendedAction
)
from logic.agents.nodes.prediction import validate_prediction_node
from logic.agents.nodes.context import build_context_node
from logic.agents.nodes.retrieval import retrieve_knowledge_node
from logic.agents.nodes.historical import retrieve_historical_node
from logic.agents.nodes.diagnosis import analyze_failure_node, generate_explanation_node
from logic.agents.nodes.recommendation import generate_recommendations_node
from logic.agents.nodes.priority import assign_priority_node
from logic.agents.nodes.human_review import determine_human_review_node

logger = logging.getLogger(__name__)

def create_diagnostic_graph():
    """Constructs the explicit LangGraph diagnostic workflow graph."""
    builder = StateGraph(dict)

    # Add Nodes
    builder.add_node("validate_prediction", validate_prediction_node)
    builder.add_node("build_context", build_context_node)
    builder.add_node("retrieve_knowledge", retrieve_knowledge_node)
    builder.add_node("retrieve_history", retrieve_historical_node)
    builder.add_node("analyze_failure", analyze_failure_node)
    builder.add_node("generate_explanation", generate_explanation_node)
    builder.add_node("generate_recommendations", generate_recommendations_node)
    builder.add_node("assign_priority", assign_priority_node)
    builder.add_node("determine_human_review", determine_human_review_node)

    # Define Linear State Edges
    builder.add_edge(START, "validate_prediction")
    builder.add_edge("validate_prediction", "build_context")
    builder.add_edge("build_context", "retrieve_knowledge")
    builder.add_edge("retrieve_knowledge", "retrieve_history")
    builder.add_edge("retrieve_history", "analyze_failure")
    builder.add_edge("analyze_failure", "generate_explanation")
    builder.add_edge("generate_explanation", "generate_recommendations")
    builder.add_edge("generate_recommendations", "assign_priority")
    builder.add_edge("assign_priority", "determine_human_review")
    builder.add_edge("determine_human_review", END)

    return builder.compile()

diagnostic_graph = create_diagnostic_graph()


class DiagnosticEngine:
    """Squad C Primary Integration Interface for Squad B AI Logic."""

    def __init__(self):
        self.graph = diagnostic_graph

    def analyze(self, prediction: Union[MLPrediction, Dict[str, Any]]) -> DiagnosticResult:
        """Executes full Squad B LangGraph AI diagnostic workflow on an ML prediction object."""
        if isinstance(prediction, MLPrediction):
            initial_state = prediction.model_dump()
        else:
            initial_state = prediction.copy()

        initial_state["telemetry"] = [
            t.model_dump() if hasattr(t, "model_dump") else t
            for t in initial_state.get("telemetry", [])
        ]

        # Execute LangGraph workflow
        final_state = self.graph.invoke(initial_state)

        dev_id = final_state.get("device_id") or final_state.get("equipment_id", "DEV-88401")
        dev_name = final_state.get("device_name") or final_state.get("equipment_type", "Medical Equipment")
        risk_score = final_state.get("risk_score", 0.0)
        prob = final_state.get("future_event_probability")
        if prob is None:
            prob = (risk_score / 100.0) if risk_score is not None else 0.5
        pred_failure = final_state.get("predicted_failure", "medical-device future-event risk")

        # Build clean DiagnosticResult Pydantic output object
        return DiagnosticResult(
            equipment_id=dev_id,
            equipment_type=dev_name,
            risk_score=risk_score,
            predicted_failure=pred_failure,
            diagnosis=f"HIGH RISK: {pred_failure} (Probability: {prob:.2f})",

            probable_root_causes=[
                ProbableRootCause(**c) if isinstance(c, dict) else c
                for c in final_state.get("probable_root_causes", [])
            ],
            evidence=[
                EvidenceCategory(**e) if isinstance(e, dict) else e
                for e in final_state.get("evidence", [])
            ],
            historical_context=final_state.get("historical_context", []),
            explanation=final_state.get("explanation", ""),
            recommended_actions=[
                RecommendedAction(**a) if isinstance(a, dict) else a
                for a in final_state.get("recommended_actions", [])
            ],
            maintenance_priority=final_state.get("maintenance_priority", "MEDIUM"),
            confidence=final_state.get("agent_confidence", 0.91),
            citations=final_state.get("citations", []),
            requires_human_review=final_state.get("requires_human_review", True),
            errors=final_state.get("errors", [])
        )

