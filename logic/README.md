# Squad B — The Logic Engine (Medical Equipment Failure Risk & AI Reasoning)

Welcome to **Squad B (The Logic)** module for the **MedTecCare Medical Device Failure Prediction Platform**.

Squad B provides autonomous AI agent orchestration via **LangGraph**, **Squad A CatBoost model integration**, BGE+BM25 Hybrid RAG knowledge retrieval, read-only Text-to-SQL historical log analysis, multi-source evidence categorization, probabilistic risk synthesis, and human-in-the-loop safety enforcement.

---

## 📌 Domain & Machine Learning Context

- **Organizer Dataset**: Kaggle *Faulty Medical Devices - Global Dataset*
- **Refined Dataset**: `DATA/medical_device_ml_dataset.csv` (118,517 rows × 12 columns)
- **Dataset Features**: `device_id`, `device_name`, `classification`, `risk_class`, `country`, `manufacturer`, `parent_company`, `previous_events`, `previous_recalls`, `previous_safety_notices`, `future_event`, `years_in_service`
- **Predictive Model**: Squad A `CatBoostClassifier` (iterations=500, depth=7, learning_rate=0.05, loss_function="Logloss", eval_metric="AUC", auto_class_weights="Balanced", random_seed=42) with SHAP for explainability (`DATA/medical_device_catboost.pkl`).
- **Squad B Responsibility**: Consumes Squad A prediction payload via `squad_a_adapter.py`, categorizes evidence, performs probabilistic risk interpretation (`medical-device future-event risk`), synthesizes recommendations, assigns priority, and flags human review requirements.

---

## 📁 Folder Structure

```
logic/
├── __init__.py                # Top-level exports (DiagnosticEngine, MLPrediction, DiagnosticResult)
├── requirements.txt           # Squad B isolated dependencies
├── .env.example               # Environment configuration template
├── README.md                  # Squad B technical documentation & integration guide
│
├── integration/               # Squad A Integration Layer
│   ├── __init__.py
│   └── squad_a_adapter.py     # Adapts Squad A CatBoost prediction payload to MLPrediction contract
│
├── schemas/                   # Strongly typed Pydantic contracts
│   ├── __init__.py
│   ├── prediction.py          # Squad A Input Contract (MLPrediction & Medical Device Attributes)
│   └── diagnostic.py          # Squad C Output Contract (DiagnosticResult)
│
├── agents/                    # LangGraph State Graph Agent Engine
│   ├── __init__.py
│   ├── state.py               # AgentState schema (Medical device fields & diagnostic findings)
│   ├── graph.py               # DiagnosticEngine class & compiled 9-node LangGraph StateGraph
│   └── nodes/                 # Explicit diagnostic pipeline nodes
│       ├── prediction.py      # Node 1: ML prediction validation (Squad A medical contract)
│       ├── context.py         # Node 2: Medical device & SHAP context builder
│       ├── retrieval.py       # Node 3: Hybrid RAG search execution
│       ├── historical.py      # Node 4: Text-to-SQL maintenance log query
│       ├── diagnosis.py       # Node 5 & 6: Risk factor analysis & LLM explanation
│       ├── recommendation.py # Node 7: Medical safety & inspection recommendation generator
│       ├── priority.py        # Node 8: Priority assignment (LOW, MEDIUM, HIGH, CRITICAL)
│       └── human_review.py    # Node 9: Human review decision flag (defaults to True)
│
├── rag/                       # Retrieval Augmented Generation Engine
│   ├── __init__.py
│   ├── embeddings.py          # BGE Embeddings (BAAI/bge-small-en-v1.5 + fallback)
│   ├── bm25.py                # Okapi BM25 Lexical Keyword Search
│   ├── vector_store.py        # Dense Vector Store Cosine Index
│   ├── hybrid_search.py       # Dense + Lexical Hybrid Search Orchestrator
│   └── reranker.py            # Cohere Reranker API with Reciprocal Rank Fusion (RRF) fallback
│
├── knowledge_base/            # Regulatory & Technical Documentation Ingestion
│   ├── __init__.py
│   ├── chunking.py            # Overlapping text chunker utility
│   ├── metadata.py            # Document metadata schema
│   ├── ingestion.py           # Document ingestion manager
│   └── documents/             # Technical & OEM Reference Manuals
│
├── llm/                       # Diagnostic Reasoning & Evidence Synthesis
│   ├── __init__.py
│   ├── provider.py            # Configurable LLM Provider (OpenAI/Groq/Fallback)
│   ├── prompts.py             # System prompts for medical risk evidence categorizer
│   └── diagnostic.py          # Evidence categorizer (MODEL_EVIDENCE, DOCUMENT_EVIDENCE, HISTORICAL_EVIDENCE, AI_INFERENCE)
│
├── text_to_sql/               # Standalone Read-Only Text-to-SQL Service
│   ├── __init__.py
│   ├── validator.py           # Strict SQL Security Validator (allows ONLY SELECT, blocks write operations)
│   └── generator.py           # Natural language translator & SQLite execution engine
│
├── demo/                      # Standalone Demonstration Module
│   ├── mock_prediction.json   # Sample Squad A input payload (Infusion Pump System)
│   └── run_demo.py            # Executable demo runner script
│
└── tests/                     # Isolated Test Suite (16/16 PASSED)
    ├── test_agents.py         # DiagnosticEngine & LangGraph state tests
    ├── test_integration.py    # Squad A adapter, evidence preservation & risk tests
    ├── test_rag.py            # Hybrid search, BM25, and BGE vector tests
    ├── test_sql.py            # SQL injection validator & read-only execution tests
    └── test_end_to_end.py     # Squad A -> Squad B full vertical slice end-to-end test
```

---

## ⚡ Quick Start & Installation

### 1. Install Dependencies
```bash
pip install -r logic/requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` in your project root or set environment variables:
```bash
cp logic/.env.example .env
```

Key environment variables:
- `LLM_PROVIDER`: `openai` or `groq` (or fallback for rule-based mode)
- `OPENAI_API_KEY`: OpenAI API Key
- `GROQ_API_KEY`: Groq API Key

---

## 🚀 Running the Standalone Demo

To verify Squad B logic independently:
```bash
python logic/demo/run_demo.py
```
This ingests `logic/demo/mock_prediction.json`, passes it through `adapt_squad_a_prediction()`, executes the 9-node LangGraph workflow, and prints the structured `DiagnosticResult` JSON payload.

---

## 🧪 Running Test Suite

Run all isolated unit and end-to-end tests:
```bash
python -m pytest logic/tests -v
```

---

## 🤝 Integration Guide for Squad C (Central Backend Team)

Squad C can seamlessly import and run Squad B's diagnostic engine in 3 lines of code:

```python
from logic.integration import adapt_squad_a_prediction
from logic.agents.graph import DiagnosticEngine

# 1. Instantiate engine
engine = DiagnosticEngine()

# 2. Adapt raw Squad A CatBoost prediction payload
prediction = adapt_squad_a_prediction({
    "device_id": "DEV-88401",
    "device_name": "Smart Infusion Pump System",
    "classification": "Active Infusion Equipment",
    "risk_class": "Class IIb",
    "manufacturer": "B. Braun Melsungen AG",
    "future_event_probability": 0.87,
    "prediction": 1,
    "risk_level": "HIGH",
    "model_confidence": 0.87,
    "previous_events": 3,
    "previous_recalls": 1,
    "previous_safety_notices": 2,
    "years_in_service": 4.5,
    "feature_drivers": [
        {"feature": "previous_recalls", "impact": 0.42},
        {"feature": "previous_safety_notices", "impact": 0.28}
    ]
})

# 3. Analyze and receive structured output
result = engine.analyze(prediction)

# Output ready for Squad C API endpoint!
print(result.model_dump())
```
