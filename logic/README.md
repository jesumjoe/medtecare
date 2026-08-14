# Squad B — The Logic Engine (AI Agents & Knowledge Base)

Welcome to **Squad B (The Logic)** module for **SentinelOps Predictive Maintenance Platform**.

Squad B provides autonomous AI agent orchestration, BGE+BM25 Hybrid RAG knowledge retrieval, read-only Text-to-SQL historical log analysis, evidence synthesis, and structured maintenance diagnostic reasoning.

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
├── agents/                    # LangGraph State Graph Agent Engine
│   ├── __init__.py
│   ├── state.py               # AgentState typing
│   ├── graph.py               # DiagnosticEngine class & compiled LangGraph StateGraph
│   └── nodes/                 # Explicit diagnostic pipeline nodes
│       ├── prediction.py      # Node 1: ML prediction validation
│       ├── context.py         # Node 2: Telemetry context builder
│       ├── retrieval.py       # Node 3: Hybrid RAG search execution
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
│   ├── vector_store.py        # Dense Vector Store Cosine Index
│   ├── hybrid_search.py       # Dense + Lexical Hybrid Search Orchestrator
│   └── reranker.py            # Cohere Reranker API with Reciprocal Rank Fusion (RRF) fallback
│
├── knowledge_base/            # OEM Documentation & Ingestion
│   ├── __init__.py
│   ├── chunking.py            # Overlapping text chunker utility
│   ├── metadata.py            # Document metadata schema
│   ├── ingestion.py           # Document ingestion manager
│   └── documents/             # Demo OEM Manuals (SKF Bearings, CNC Spindles, Hydraulics, Robotics)
│
├── llm/                       # Diagnostic Reasoning & Evidence Synthesis
│   ├── __init__.py
│   ├── provider.py            # Configurable LLM Provider (OpenAI/Anthropic/Groq/Ollama/Fallback)
│   ├── prompts.py             # System prompts for diagnostic reasoning
│   └── diagnostic.py          # Evidence categorizer (MODEL, DOCUMENT, HISTORICAL, AI INFERENCE)
│
├── text_to_sql/               # Standalone Read-Only Text-to-SQL Service
│   ├── __init__.py
│   ├── validator.py           # Strict SQL Security Validator (allows ONLY SELECT, blocks write operations)
│   └── generator.py           # Natural language translator & SQLite execution engine
│
├── demo/                      # Standalone Demonstration Module
│   ├── mock_prediction.json   # Sample Squad A input payload
│   └── run_demo.py            # Executable demo script
│
└── tests/                     # Isolated Test Suite
    ├── test_agents.py         # DiagnosticEngine & LangGraph state tests
    ├── test_rag.py            # Hybrid search, BM25, and BGE vector tests
    ├── test_sql.py            # SQL injection validator & read-only execution tests
    └── test_end_to_end.py     # Full vertical slice end-to-end test
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
- `LLM_PROVIDER`: `openai` (or `fallback` for local rule-based mode)
- `OPENAI_API_KEY`: Your OpenAI API Key
- `COHERE_API_KEY`: (Optional) Cohere Reranker API key. If absent, the system uses Reciprocal Rank Fusion (RRF) automatically.

---

## 🚀 Running the Standalone Demo

To verify Squad B logic independently before Squad C backend integration:
```bash
python logic/demo/run_demo.py
```
This loads `logic/demo/mock_prediction.json`, passes it to `DiagnosticEngine`, executes the 9-node LangGraph workflow, and outputs structured `DiagnosticResult` JSON to stdout.

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
from logic.schemas.prediction import MLPrediction
from logic.agents.graph import DiagnosticEngine

# 1. Instantiate engine
engine = DiagnosticEngine()

# 2. Prepare prediction (from Squad A ML model)
prediction = MLPrediction(
    equipment_id="EQ-001",
    equipment_type="CNC Milling Machine",
    risk_score=87.0,
    predicted_failure="Spindle Bearing Seizure",
    model_confidence=0.94,
    important_features=["Bearing Temp (+34%)", "Vibration RMS (8.7 mm/s)"]
)

# 3. Analyze and receive structured output
result = engine.analyze(prediction)

# Pass result directly to Squad C FastAPI endpoint / Supabase!
print(result.model_dump())
```
