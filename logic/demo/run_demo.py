"""
Squad B Standalone Demo Runner.
Demonstrates:
  Squad A CatBoost Output -> Squad A Adapter -> MLPrediction Contract ->
  LangGraph Diagnostic Graph -> BGE+BM25 RAG -> Text-to-SQL Maintenance History ->
  LLM Reasoning & Evidence Categorization -> DiagnosticResult JSON Output.

Usage:
  python logic/demo/run_demo.py
"""

import os
import sys
import json

# Ensure repository root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from logic.integration import adapt_squad_a_prediction
from logic.agents.graph import DiagnosticEngine


def main():
    print("=" * 70)
    print("  MEDTECARE — SQUAD B DIAGNOSTIC ENGINE DEMO (MEDICAL EQUIPMENT DOMAIN)")
    print("=" * 70)

    # 1. Load raw Squad A CatBoost prediction JSON payload
    mock_file = os.path.join(os.path.dirname(__file__), "mock_prediction.json")
    print(f"\n[1] Ingesting Squad A CatBoost Prediction payload from '{mock_file}'...")
    with open(mock_file, "r") as f:
        squad_a_payload = json.load(f)

    # 2. Adapt Squad A Output via Integration Adapter
    print("\n[2] Executing Squad A -> Squad B Adapter (logic/integration/squad_a_adapter.py)...")
    prediction = adapt_squad_a_prediction(squad_a_payload)

    print(f"    [OK] Device ID: {prediction.equipment_id} ({prediction.equipment_type})")
    print(f"    [OK] Classification: {prediction.classification} | Risk Class: {prediction.risk_class}")
    print(f"    [OK] Manufacturer: {prediction.manufacturer} ({prediction.country})")
    print(f"    [OK] CatBoost Probability: {prediction.future_event_probability:.2f} | Risk Score: {prediction.risk_score:.1f}/100")
    print(f"    [OK] Model Confidence: {prediction.model_confidence * 100:.0f}% | Predicted Risk: {prediction.predicted_failure}")
    print(f"    [OK] SHAP Feature Drivers: {', '.join(prediction.important_features)}")

    # 3. Instantiate Squad B Diagnostic Engine
    print("\n[3] Instantiating Squad B DiagnosticEngine & LangGraph Agent...")
    engine = DiagnosticEngine()

    # 4. Execute LangGraph Diagnostic Workflow
    print("\n[4] Executing LangGraph 9-Node Diagnostic Workflow...")
    print("    -> Step 1: Validate ML Input (Squad A Medical Device Contract)")
    print("    -> Step 2: Assemble Medical Device & SHAP Context")
    print("    -> Step 3: Hybrid RAG Search (BGE Dense + BM25 Lexical + Cohere Rerank)")
    print("    -> Step 4: Text-to-SQL Historical Maintenance Log Retrieval")
    print("    -> Step 5: Probable Medical Equipment Risk Factor Analysis")
    print("    -> Step 6: LLM Evidence Categorization (Model/Doc/Historical/Inference)")
    print("    -> Step 7: Medical Safety & Inspection Action Recommendations")
    print("    -> Step 8: Priority Assignment (Consider Probability, Risk Class & History)")
    print("    -> Step 9: Flag Human Review Decision (Defaults to True)")

    result = engine.analyze(prediction)

    # 5. Output Structured Result
    print("\n" + "=" * 70)
    print("                     SQUAD B DIAGNOSTIC RESULT")
    print("=" * 70)
    print(json.dumps(result.model_dump(), indent=2))

    print("\n" + "=" * 70)
    print("[OK] Squad B Standalone Medical Equipment Pipeline Complete!")
    print("[OK] DiagnosticResult ready for Squad C FastAPI Backend Integration.")
    print("=" * 70)


if __name__ == "__main__":
    main()
