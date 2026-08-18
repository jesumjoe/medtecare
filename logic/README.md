# Squad B — The Logic Engine (AI Agents & Medical Device RAG Knowledge Base)

Welcome to **Squad B (The Logic)** module for **SentinelOps / MedTeCare Predictive Maintenance Platform**.

Squad B provides autonomous AI agent orchestration (LangGraph), **Medical Device Hybrid RAG** (BGE-small-en-v1.5 + Okapi BM25 + Reciprocal Rank Fusion + Optional Cohere Reranking), read-only Text-to-SQL historical log analysis, evidence synthesis, and structured maintenance diagnostic reasoning.

---

## 📁 Folder Structure

```
logic/
├── __init__.py                # Top-level exports (DiagnosticEngine, MLPrediction, DiagnosticResult)
├── requirements.txt           # Squad B isolated dependencies
├── .env.example               # Environment configuration template
├── README.md                  # Squad B technical documentation & integration guide
│
├── schemas/                   # Strongly typed Pydantic contracts
│   ├── __init__.py
│   ├── prediction.py          # Squad A Input Contract (MLPrediction)
│   └── diagnostic.py          # Squad C Output Contract (DiagnosticResult)
│
├── integration/               # Squad A Raw Model Adapters
│   ├── __init__.py
│   └── squad_a_adapter.py     # Adapts raw Squad A prediction dicts to MLPrediction
│
├── agents/                    # LangGraph State Graph Agent Engine
│   ├── __init__.py
│   ├── state.py               # AgentState typing
│   ├── graph.py               # DiagnosticEngine class & compiled LangGraph StateGraph
│   └── nodes/                 # Explicit diagnostic pipeline nodes
│       ├── prediction.py      # Node 1: ML prediction validation
│       ├── context.py         # Node 2: Telemetry context builder
│       ├── retrieval.py       # Node 3: Medical Device Hybrid RAG search execution
│       ├── historical.py      # Node 4: Text-to-SQL maintenance log query
│       ├── diagnosis.py       # Node 5 & 6: Root cause analysis & LLM explanation
│       ├── recommendation.py # Node 7: Recommended action item generator
│       ├── priority.py        # Node 8: Priority assignment (LOW, MEDIUM, HIGH, CRITICAL)
│       └── human_review.py    # Node 9: Human review decision flag
│
├── rag/                       # Retrieval Augmented Generation Engine
│   ├── __init__.py
│   ├── embeddings.py          # BGE Embeddings (BAAI/bge-small-en-v1.5 + fallback)
│   ├── bm25.py                # Okapi BM25 Lexical Keyword Search
│   ├── vector_store.py        # Dense Vector Store with Cosine Index & Metadata Filtering
│   ├── hybrid_search.py       # Dense + Lexical Hybrid Search Orchestrator
│   └── reranker.py            # Reciprocal Rank Fusion (RRF) & Optional Cohere Reranker API
│
├── knowledge_base/            # Medical Device Knowledge Base & Ingestion
│   ├── __init__.py
│   ├── metadata.py            # MedicalDeviceMetadata & DocumentMetadata schema
│   ├── chunking.py            # Text chunker & Medical Device record formatter
│   ├── ingestion.py           # Dataset & manual ingestion with Target Leakage Protection
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
└── tests/                     # Isolated Test Suite
    ├── test_agents.py         # DiagnosticEngine & LangGraph state tests
    ├── test_integration.py    # Squad A adapter, evidence preservation & risk tests
    ├── test_rag.py            # Comprehensive Medical Device RAG & Target Leakage tests
    ├── test_sql.py            # SQL injection validator & read-only execution tests
    └── test_end_to_end.py     # Full vertical slice end-to-end test
```

---

## 🏥 Medical Device RAG & Knowledge Base Architecture

The RAG pipeline retrieves historical evidence from the **Faulty Medical Devices Global Dataset** (`DATA/medical_device_ml_dataset.csv`) and OEM maintenance guides:

```
                      Query (Equipment Type, Failure Mode, Anomalies)
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
        BGE Dense Vector Search                       BM25 Lexical Search
        (BAAI/bge-small-en-v1.5)                        (rank-bm25)
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          ▼
                         Reciprocal Rank Fusion (RRF, k=60)
                                          │
                         [Optional] Cohere Rerank API (v3.0)
                                          │
                                          ▼
                      Historical Medical Device Evidence & Citations
```

### 1. Metadata Preservation
Every indexed medical device record preserves:
- `device_id`: Unique identifier (e.g., `MD-INF-101`)
- `device_name`: Commercial / model designation
- `classification`: FDA/ISO device category (e.g., `Infusion Delivery System`)
- `risk_class`: Regulatory risk class (`Class I`, `Class II`, `Class III`)
- `country`: Country of manufacture/operation
- `manufacturer` & `parent_company`: OEM corporate entities
- `previous_events`: Count of historical malfunction events
- `previous_recalls`: Historical product recall count
- `previous_safety_notices`: Prior safety notices / advisory alerts
- `years_in_service`: Operational lifespan in active service

### 2. Target Leakage Protection
- The dataset target column `future_event` (Squad A's prediction objective) is **strictly excluded** during ingestion.
- The RAG system only indexes and presents verified past history (`HISTORICAL_EVIDENCE`), ensuring no future target leakage occurs.

### 3. Fully Local Operation (No Paid APIs Required)
- **BGE-small-en-v1.5** + **Okapi BM25** + **Reciprocal Rank Fusion (RRF)** run completely locally and free of charge.
- **Cohere Reranker** (`COHERE_API_KEY`) is purely optional; if omitted, RRF executes automatically.

---

## ⚡ Quick Start & Installation

### 1. Install Dependencies
```bash
pip install -r logic/requirements.txt
```

### 2. Configure Environment Variables
```bash
cp logic/.env.example .env
```

Key environment variables:
- `LLM_PROVIDER`: `openai` | `groq` | `fallback` (local deterministic mode)
- `OPENAI_API_KEY`: (Optional) Live LLM reasoning
- `GROQ_API_KEY`: (Optional) High-speed Groq inference
- `COHERE_API_KEY`: (Optional) Cohere reranker API

---

## 🚀 Running the Standalone Demo

```bash
python logic/demo/run_demo.py
```

---

## 🧪 Running Test Suite

Run all isolated unit and integration tests:
```bash
python -m pytest logic/tests -v
```

---

## 🤝 Integration Guide for Squad C

```python
from logic.integration import adapt_squad_a_prediction
from logic.agents.graph import DiagnosticEngine

# 1. Instantiate engine
engine = DiagnosticEngine()

# 2. Adapt raw Squad A CatBoost prediction payload
prediction = adapt_squad_a_prediction({
    "device_id": "MD-INF-101",
    "device_name": "Smart Infusion Pump System",
    "classification": "Infusion Delivery Equipment",
    "risk_class": "Class II",
    "manufacturer": "CareFusion BD",
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

# Output ready for Squad C API endpoint / UI presentation!
print(result.model_dump())
```
