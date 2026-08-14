"""
Squad B Standalone Demo Runner.
Demonstrates:
  ML Prediction (Squad A Input) -> DiagnosticEngine -> LangGraph -> BGE+BM25 Hybrid RAG ->
  Text-to-SQL History -> LLM Reasoning -> DiagnosticResult JSON Output.

Usage:
  python logic/demo/run_demo.py
"""

import os
import sys
import json

# Ensure repository root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from logic.schemas.prediction import MLPrediction
from logic.agents.graph import DiagnosticEngine

def main():
    print("=" * 70)
    print("      SENTINELOPS — SQUAD B DEMO RUNNER (STANDALONE LOGIC ENGINE)")
    print("=" * 70)

    # 1. Load mock prediction
    mock_file = os.path.join(os.path.dirname(__file__), "mock_prediction.json")
    print(f"\n[1] Loading Squad A ML Prediction contract from '{mock_file}'...")
    with open(mock_file, "r") as f:
        data = json.load(f)

    prediction = MLPrediction(**data)
    print(f"    [OK] Equipment ID: {prediction.equipment_id} ({prediction.equipment_type})")
    print(f"    [OK] Predicted Failure: {prediction.predicted_failure}")
    print(f"    [OK] Risk Score: {prediction.risk_score}/100 | Confidence: {prediction.model_confidence*100:.0f}%")
    print(f"    [OK] Important Features: {', '.join(prediction.important_features)}")

    # 2. Instantiate Squad B Diagnostic Engine
    print("\n[2] Instantiating Squad B DiagnosticEngine & LangGraph Agent...")
    engine = DiagnosticEngine()

    # 3. Execute LangGraph Diagnostic Workflow
    print("\n[3] Executing Diagnostic Workflow...")
    print("    -> Step 1: Validate ML Input")
    print("    -> Step 2: Assemble Telemetry Context")
    print("    -> Step 3: Hybrid RAG Search (BGE Dense + BM25 Lexical + Rerank)")
    print("    -> Step 4: Text-to-SQL Historical Maintenance Log Retrieval")
    print("    -> Step 5: Root Cause Analysis")
    print("    -> Step 6: LLM Evidence Synthesis (Model/Doc/Historical/Inference)")
    print("    -> Step 7: Step-by-Step Maintenance Recommendations")
    print("    -> Step 8: Maintenance Priority Assignment")
    print("    -> Step 9: Flag Human Review Decision")

    result = engine.analyze(prediction)

    # 4. Output Structured Result
    print("\n" + "=" * 70)
    print("                     SQUAD B DIAGNOSTIC RESULT")
    print("=" * 70)
    print(json.dumps(result.model_dump(), indent=2))

    print("\n" + "=" * 70)
    print("[OK] Squad B Standalone Pipeline Execution Complete!")
    print("[OK] DiagnosticResult is ready to be consumed by Squad C FastAPI Backend.")
    print("=" * 70)

if __name__ == "__main__":
    main()
