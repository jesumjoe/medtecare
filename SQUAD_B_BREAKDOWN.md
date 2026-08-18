# Complete Technical Breakdown — Squad B (Logic Engine) & Squad A Integration

**Project Repository:** `https://github.com/jesumjoe/medtecare.git`  
**Local Path:** `d:\medtecare`  
**Git Branch:** `squad-b-logic`  
**Status:** 100% Completed & Verified (16/16 Pytest Suite Passing & Standalone Demo Verified)

---

## 📌 1. Domain & Dataset Architecture

- **Domain**: Medical Equipment Failure Prediction Platform (MedTecCare).
- **Organizer Dataset**: Kaggle *Faulty Medical Devices - Global Dataset*.
- **Refined Squad A Dataset**: `DATA/medical_device_ml_dataset.csv` (118,517 rows × 12 columns).
  - Columns: `device_id`, `device_name`, `classification`, `risk_class`, `country`, `manufacturer`, `parent_company`, `previous_events`, `previous_recalls`, `previous_safety_notices`, `future_event`, `years_in_service`.
  - Target: `future_event`.
- **Squad A ML Model**: `CatBoostClassifier` trained with `iterations=500, depth=7, learning_rate=0.05, loss_function="Logloss", eval_metric="AUC", auto_class_weights="Balanced", random_seed=42`.
- **Explainability**: SHAP feature driver impacts.
- **Squad A Model Artifact**: `DATA/medical_device_catboost.pkl`.

---

## 🧠 2. Squad B Logic Engine Architecture (`logic/`)

```
d:\medtecare\logic\
├── __init__.py                # Package exports (DiagnosticEngine, MLPrediction, DiagnosticResult)
├── requirements.txt           # Squad B isolated dependencies
├── .env.example               # Configuration template (OpenAI / Groq / Cohere)
├── README.md                  # Detailed developer & integration documentation
│
├── integration/               # Squad A Integration Adapter Layer
│   ├── __init__.py
│   └── squad_a_adapter.py     # Converts raw Squad A CatBoost prediction outputs into MLPrediction contract
│
├── schemas/                   # Strongly Typed Pydantic Contracts
│   ├── __init__.py
│   ├── prediction.py          # Squad A Input Contract (MLPrediction, medical device attributes)
│   └── diagnostic.py          # Squad C Output Contract (DiagnosticResult, ProbableRootCause, EvidenceCategory, RecommendedAction)
│
├── agents/                    # LangGraph State Graph Workflow
│   ├── state.py               # AgentState schema (device context & findings)
│   ├── graph.py               # DiagnosticEngine & LangGraph StateGraph compiled workflow
│   └── nodes/                 # 9 explicit pipeline nodes
│       ├── prediction.py      # Node 1: ML prediction validation (Squad A medical contract)
│       ├── context.py         # Node 2: Device context & SHAP driver builder
│       ├── retrieval.py       # Node 3: Hybrid RAG search execution
│       ├── historical.py      # Node 4: Text-to-SQL maintenance log query
│       ├── diagnosis.py       # Node 5 & 6: Medical risk factor analysis & LLM explanation
│       ├── recommendation.py # Node 7: Medical safety review & inspection action generator
│       ├── priority.py        # Node 8: Priority assignment (LOW, MEDIUM, HIGH, CRITICAL)
│       └── human_review.py    # Node 9: Flag human review decision (defaults to True)
│
├── rag/                       # Hybrid RAG Retrieval Engine
│   ├── embeddings.py          # BGE Embeddings (BAAI/bge-small-en-v1.5 + fallback)
│   ├── bm25.py                # Okapi BM25 Lexical Keyword Search
│   ├── vector_store.py        # Dense Vector Cosine Similarity Store
│   ├── hybrid_search.py       # Dense + Lexical Hybrid Search Orchestrator
│   └── reranker.py            # Cohere Reranker API with Reciprocal Rank Fusion (RRF) fallback
│
├── knowledge_base/            # OEM & Regulatory Documentation
│   ├── chunking.py            # Overlapping text chunker utility
│   ├── metadata.py            # Document metadata schema
│   ├── ingestion.py           # Automatic document ingestion manager
│   └── documents/             # Technical reference manuals
│
├── llm/                       # Diagnostic Reasoning & Live LLM Service
│   ├── provider.py            # Live LLM Provider (Live OpenAI / Live Groq / Fallback)
│   ├── prompts.py             # System prompts enforcing probabilistic risk language & evidence categorization
│   └── diagnostic.py          # Evidence categorizer (MODEL_EVIDENCE, DOCUMENT_EVIDENCE, HISTORICAL_EVIDENCE, AI_INFERENCE)
│
├── text_to_sql/               # Standalone Read-Only Text-to-SQL Engine
│   ├── validator.py           # Strict SQL Security Validator (blocks non-SELECT queries)
│   └── generator.py           # Natural language to safe SELECT SQL engine & SQLite database
│
├── demo/                      # Standalone Demonstration Module
│   ├── mock_prediction.json   # Sample Squad A input payload (Infusion Pump System)
│   └── run_demo.py            # Executable demo script
│
└── tests/                     # Isolated Test Suite (16/16 PASSED)
    ├── test_agents.py         # Agent execution & graph state tests
    ├── test_integration.py    # Squad A adapter, evidence preservation & risk tests
    ├── test_rag.py            # Hybrid RAG tests
    ├── test_sql.py            # Text-to-SQL security tests
    └── test_end_to_end.py     # Squad A -> Squad B full vertical slice test
```

---

## 🔄 3. Squad A → Squad B Integration & Evidence Flow

```
[Squad A CatBoost Output] ──► [squad_a_adapter.py] ──► [MLPrediction Contract]
                                                                │
                                                                ▼
[DiagnosticResult Output] ◄── [LangGraph 9-Node Pipeline] ◄────┤
                                   │
                                   ├── MODEL_EVIDENCE (CatBoost probability, SHAP drivers, device attributes)
                                   ├── DOCUMENT_EVIDENCE (RAG technical excerpts)
                                   ├── HISTORICAL_EVIDENCE (Text-to-SQL maintenance logs)
                                   └── AI_INFERENCE (Probabilistic risk interpretation & recommendations)
```

1. **Squad A Integration Adapter**: `squad_a_adapter.py` ingests raw Squad A CatBoost dictionary outputs (`future_event_probability`, `prediction`, `risk_level`, `feature_drivers`, `classification`, `risk_class`, `manufacturer`, `previous_recalls`, etc.) and transforms them into Squad B's `MLPrediction` contract without modifying raw predictions.
2. **Model Evidence Preservation**: Preserves all Squad A prediction evidence into `MODEL_EVIDENCE` tags. The LLM is strictly prohibited from contradicting or overriding model probability.
3. **Probabilistic Risk Interpretation**: Interprets predictions probabilistically (e.g. 0.87 probability ➔ *"High predicted future-event risk"*). Never asserts deterministic device failure.
4. **Medical Equipment Action Items**: Focuses recommendations on safety review, maintenance prioritization, historical event audits, regulatory guidance checks, and escalation to biomedical engineering staff. Does NOT invent physical component replacements.
5. **Priority Assignment**: Evaluates predicted probability, model confidence, regulatory risk class (e.g. Class IIb/Class III), and recall history into `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.
6. **Human Review Safety Guarantee**: Always enforces `requires_human_review = True` as a safeguard for medical equipment decision support.

---

## 🤝 4. Squad C Integration Contract

Squad C (Central Backend) can invoke Squad B's entire logic engine in **3 lines of Python**:

```python
from logic.integration import adapt_squad_a_prediction
from logic.agents.graph import DiagnosticEngine

# 1. Instantiate engine
engine = DiagnosticEngine()

# 2. Adapt Squad A prediction payload
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

# 3. Analyze & receive structured DiagnosticResult
result = engine.analyze(prediction)
```

---

## 🧪 5. Verification Results

- **Pytest Suite (`python -m pytest logic/tests -v`)**: **16/16 tests PASSED in 0.87s**.
- **Standalone Demo (`python logic/demo/run_demo.py`)**: Successfully executes end-to-end medical equipment failure risk diagnostic workflow.
