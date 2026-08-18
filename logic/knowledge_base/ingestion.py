"""
Knowledge Base Document Ingestion Manager for Medical Devices & Technical Manuals.
Loads, processes, and indexes medical device dataset records and OEM maintenance guides
into BM25 Lexical (rank-bm25) and BGE Dense Vector (BAAI/bge-small-en-v1.5) indices.

Target Leakage Protection:
- Any `future_event` column in datasets is strictly filtered out during ingestion.
- Historical attributes are tagged clearly as HISTORICAL_EVIDENCE.
"""

import os
import csv
from typing import List, Dict, Any, Optional
import logging
from logic.rag.embeddings import embeddings_service
from logic.rag.vector_store import vector_store
from logic.rag.bm25 import bm25_retriever
from logic.knowledge_base.chunking import chunk_text, format_medical_device_record
from logic.knowledge_base.metadata import MedicalDeviceMetadata

logger = logging.getLogger(__name__)

# Fallback catalog of diverse medical device records across Class I, II, III for standalone demo / offline mode
DEFAULT_MEDICAL_DEVICES = [
    {
        "device_id": "MD-INF-101",
        "device_name": "Infusion Pump Volumetric Alaris-X4",
        "classification": "Infusion Delivery System",
        "risk_class": "Class II",
        "country": "United States",
        "manufacturer": "CareFusion / BD Medical",
        "parent_company": "Becton, Dickinson and Company",
        "previous_events": 4,
        "previous_recalls": 1,
        "previous_safety_notices": 2,
        "years_in_service": 4.5,
        "failure_mode": "Occlusion pressure sensor drift and downstream air-in-line false alarms",
        "maintenance_notes": "Recalibrated pressure transducer and replaced peristaltic finger assembly per OEM bulletin SB-2024-08."
    },
    {
        "device_id": "MD-DEF-204",
        "device_name": "Automated External Defibrillator LifePak-CR2",
        "classification": "Cardiovascular Defibrillation Device",
        "risk_class": "Class III",
        "country": "Germany",
        "manufacturer": "Physio-Control",
        "parent_company": "Stryker Corporation",
        "previous_events": 2,
        "previous_recalls": 0,
        "previous_safety_notices": 1,
        "years_in_service": 3.0,
        "failure_mode": "High-voltage capacitor discharge charging delay (>12 seconds)",
        "maintenance_notes": "Main power capacitor bank tested; battery contact pins cleaned and dielectric integrity verified."
    },
    {
        "device_id": "MD-SURG-309",
        "device_name": "Robotic Surgical System DaVinci Xi Endowrist",
        "classification": "Robotic Assisted Surgical Instrument",
        "risk_class": "Class II",
        "country": "United States",
        "manufacturer": "Intuitive Surgical Inc.",
        "parent_company": "Intuitive Surgical Inc.",
        "previous_events": 5,
        "previous_recalls": 1,
        "previous_safety_notices": 3,
        "years_in_service": 2.8,
        "failure_mode": "Tendon cable tension loss on master tool manipulator axis 4",
        "maintenance_notes": "Performed full axis recalibration; replaced manipulator pulley cable set per Class II recall protocol."
    },
    {
        "device_id": "MD-VEN-412",
        "device_name": "Critical Care ICU Ventilator PB-980",
        "classification": "Mechanical Respiratory Ventilator",
        "risk_class": "Class III",
        "country": "Ireland",
        "manufacturer": "Medtronic Covidien",
        "parent_company": "Medtronic plc",
        "previous_events": 6,
        "previous_recalls": 2,
        "previous_safety_notices": 4,
        "years_in_service": 5.2,
        "failure_mode": "Exhalation flow sensor calibration failure and spontaneous breath trigger drift",
        "maintenance_notes": "Replaced exhalation flow transducer; updated firmware to v3.4 to resolve sensor sampling hysteresis."
    },
    {
        "device_id": "MD-DIA-515",
        "device_name": "Hemodialysis Machine 5008S CorDiax",
        "classification": "Renal Replacement Hemodialysis Unit",
        "risk_class": "Class II",
        "country": "Germany",
        "manufacturer": "Fresenius Medical Care",
        "parent_company": "Fresenius SE & Co. KGaA",
        "previous_events": 3,
        "previous_recalls": 0,
        "previous_safety_notices": 2,
        "years_in_service": 6.1,
        "failure_mode": "Dialysate temperature regulation instability and conductivity cell scaling",
        "maintenance_notes": "Decalcified balance chambers, replaced thermal regulation thermistor, verified ultrafiltration accuracy."
    },
    {
        "device_id": "MD-PAC-620",
        "device_name": "Dual-Chamber Pacemaker Azure XT DR MRI",
        "classification": "Implantable Cardiac Pulse Generator",
        "risk_class": "Class III",
        "country": "United States",
        "manufacturer": "Medtronic Cardiac Rhythm",
        "parent_company": "Medtronic plc",
        "previous_events": 1,
        "previous_recalls": 0,
        "previous_safety_notices": 1,
        "years_in_service": 2.1,
        "failure_mode": "Telemetry RF inductive coupling loss during MRI mode transitions",
        "maintenance_notes": "Programmer software patch applied; telemetry coil sensitivity tested within safe operating margins."
    },
    {
        "device_id": "MD-IMG-730",
        "device_name": "Mobile C-Arm Fluoroscopy Ziehm Vision RFD",
        "classification": "Diagnostic X-Ray Imaging System",
        "risk_class": "Class II",
        "country": "Germany",
        "manufacturer": "Ziehm Imaging GmbH",
        "parent_company": "Ziehm Imaging",
        "previous_events": 2,
        "previous_recalls": 0,
        "previous_safety_notices": 1,
        "years_in_service": 3.8,
        "failure_mode": "X-ray tube liquid cooling circulation pressure drop and generator thermal trip",
        "maintenance_notes": "Flushed cooling heat exchanger; replaced dielectric oil circuit pump and verified beam collimation."
    },
    {
        "device_id": "MD-MON-840",
        "device_name": "Multi-Parameter Patient Monitor IntelliVue MX800",
        "classification": "Physiological Patient Monitoring",
        "risk_class": "Class II",
        "country": "Netherlands",
        "manufacturer": "Philips Healthcare",
        "parent_company": "Koninklijke Philips N.V.",
        "previous_events": 3,
        "previous_recalls": 1,
        "previous_safety_notices": 2,
        "years_in_service": 4.0,
        "failure_mode": "SpO2 optical module communication timeout and ECG lead arrhythmia false triggers",
        "maintenance_notes": "Replaced multi-measurement server (MMS) interface board; calibrated optical sensor channel."
    }
]


class KnowledgeBaseIngestion:
    """Ingestion and indexing orchestrator for medical devices and technical documentation."""

    def __init__(self, docs_dir: str = "logic/knowledge_base/documents", dataset_csv: str = "DATA/medical_device_ml_dataset.csv"):
        self.docs_dir = docs_dir
        self.dataset_csv = dataset_csv
        self._is_indexed = False
        self._indexed_count = 0

    def load_and_index_documents(
        self,
        csv_path: Optional[str] = None,
        docs_dir: Optional[str] = None,
        max_csv_rows: Optional[int] = 1000,
        force_reload: bool = False
    ) -> int:
        """Loads medical device records and OEM manuals, creates chunks, and indexes into BGE and BM25.
        
        Target Leakage Protection:
        - If CSV has `future_event`, it is never stored in document content or metadata.
        """
        if self._is_indexed and not force_reload:
            return self._indexed_count

        documents: List[Dict[str, Any]] = []

        # 1. Ingest Medical Device Dataset CSV if available
        target_csv = csv_path or self.dataset_csv
        csv_loaded = False

        if target_csv and os.path.exists(target_csv):
            try:
                logger.info(f"Loading medical device dataset from '{target_csv}'...")
                with open(target_csv, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.DictReader(f)
                    count = 0
                    for row in reader:
                        if max_csv_rows and count >= max_csv_rows:
                            break

                        # Sanitize & enforce Target Leakage Protection
                        sanitized = {k: v for k, v in row.items() if k != "future_event"}
                        
                        device_id = sanitized.get("device_id") or sanitized.get("id") or f"MD-CSV-{count+1}"
                        device_name = sanitized.get("device_name") or sanitized.get("model") or "Medical Device"
                        classification = sanitized.get("classification") or sanitized.get("device_class") or "Medical Device"
                        risk_class = sanitized.get("risk_class") or sanitized.get("risk_level") or "Class II"
                        manufacturer = sanitized.get("manufacturer") or sanitized.get("maker") or "OEM Manufacturer"
                        country = sanitized.get("country") or "Global"
                        
                        content = format_medical_device_record(sanitized)
                        
                        documents.append({
                            "id": f"MD_ROW_{count}_{device_id}",
                            "device_id": device_id,
                            "device_name": device_name,
                            "classification": classification,
                            "risk_class": risk_class,
                            "manufacturer": manufacturer,
                            "parent_company": sanitized.get("parent_company", manufacturer),
                            "country": country,
                            "previous_events": int(float(sanitized.get("previous_events", 0) or 0)),
                            "previous_recalls": int(float(sanitized.get("previous_recalls", 0) or 0)),
                            "previous_safety_notices": int(float(sanitized.get("previous_safety_notices", 0) or 0)),
                            "years_in_service": float(sanitized.get("years_in_service", 1.0) or 1.0),
                            "title": f"{device_name} ({device_id})",
                            "section": f"{classification} — Historical Record",
                            "content": content,
                            "evidence_type": "HISTORICAL_EVIDENCE",
                            "source_type": "Medical Device Global Safety Database"
                        })
                        count += 1

                csv_loaded = len(documents) > 0
                logger.info(f"Loaded {count} medical device records from dataset CSV.")
            except Exception as e:
                logger.warning(f"Error loading CSV '{target_csv}': {e}. Proceeding with default device catalog.")

        # 2. If no CSV found or loaded, load rich default medical device catalog
        if not csv_loaded:
            logger.info("Indexing default medical device catalog...")
            for idx, dev in enumerate(DEFAULT_MEDICAL_DEVICES):
                content = format_medical_device_record(dev)
                documents.append({
                    "id": f"MD_DEF_{idx}_{dev['device_id']}",
                    "device_id": dev["device_id"],
                    "device_name": dev["device_name"],
                    "classification": dev["classification"],
                    "risk_class": dev["risk_class"],
                    "manufacturer": dev["manufacturer"],
                    "parent_company": dev["parent_company"],
                    "country": dev["country"],
                    "previous_events": dev["previous_events"],
                    "previous_recalls": dev["previous_recalls"],
                    "previous_safety_notices": dev["previous_safety_notices"],
                    "years_in_service": dev["years_in_service"],
                    "title": f"{dev['device_name']} ({dev['device_id']})",
                    "section": f"{dev['classification']} — Safety History",
                    "content": content,
                    "evidence_type": "HISTORICAL_EVIDENCE",
                    "source_type": "Medical Device Global Incident Database"
                })

        # 3. Load technical manual documents if present
        target_docs_dir = docs_dir or self.docs_dir
        if target_docs_dir and os.path.exists(target_docs_dir):
            for filename in os.listdir(target_docs_dir):
                if filename.endswith(".txt"):
                    filepath = os.path.join(target_docs_dir, filename)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        text_content = f.read()

                    lines = [line.strip() for line in text_content.splitlines() if line.strip()]
                    title = lines[1].replace("Title: ", "") if len(lines) > 1 and "Title:" in lines[1] else filename
                    section = lines[2].replace("Section: ", "") if len(lines) > 2 and "Section:" in lines[2] else "Technical Reference"

                    chunks = chunk_text(text_content, chunk_size=400, chunk_overlap=50)
                    for c_idx, chunk in enumerate(chunks):
                        documents.append({
                            "id": f"DOC_{filename}_{c_idx}",
                            "device_id": f"DOC-{filename}",
                            "device_name": title,
                            "classification": "OEM Maintenance Manual",
                            "risk_class": "OEM Guidance",
                            "manufacturer": "OEM Technical Publications",
                            "parent_company": "OEM",
                            "country": "Global",
                            "previous_events": 0,
                            "previous_recalls": 0,
                            "previous_safety_notices": 0,
                            "years_in_service": 0.0,
                            "title": title,
                            "section": section,
                            "content": chunk,
                            "evidence_type": "DOCUMENT_EVIDENCE",
                            "source_type": "OEM Maintenance Manual"
                        })

        if not documents:
            logger.error("No documents or medical device records available for indexing.")
            return 0

        # 4. Generate BGE Embeddings
        texts = [doc["content"] for doc in documents]
        embeddings = embeddings_service.embed_documents(texts)

        # 5. Populate Vector Store & BM25 Retriever
        vector_store.clear()
        vector_store.add_documents(documents, embeddings)
        bm25_retriever.index_documents(documents)

        self._is_indexed = True
        self._indexed_count = len(documents)
        logger.info(f"Successfully indexed {len(documents)} medical device & knowledge chunks into RAG pipeline.")
        return self._indexed_count

    def index_medical_device_records(self, records: List[Dict[str, Any]]) -> int:
        """Indexes an explicit list of medical device dictionaries (ideal for unit testing without CSV files)."""
        documents: List[Dict[str, Any]] = []
        for idx, rec in enumerate(records):
            sanitized = {k: v for k, v in rec.items() if k != "future_event"}
            device_id = str(sanitized.get("device_id") or sanitized.get("id") or f"TEST-DEV-{idx}")
            device_name = str(sanitized.get("device_name") or "Test Device")
            classification = str(sanitized.get("classification") or "Test Classification")
            risk_class = str(sanitized.get("risk_class") or "Class II")
            manufacturer = str(sanitized.get("manufacturer") or "Test Manufacturer")

            content = format_medical_device_record(sanitized)
            documents.append({
                "id": f"REC_{idx}_{device_id}",
                "device_id": device_id,
                "device_name": device_name,
                "classification": classification,
                "risk_class": risk_class,
                "manufacturer": manufacturer,
                "parent_company": sanitized.get("parent_company", manufacturer),
                "country": sanitized.get("country", "Global"),
                "previous_events": int(sanitized.get("previous_events", 0)),
                "previous_recalls": int(sanitized.get("previous_recalls", 0)),
                "previous_safety_notices": int(sanitized.get("previous_safety_notices", 0)),
                "years_in_service": float(sanitized.get("years_in_service", 1.0)),
                "title": f"{device_name} ({device_id})",
                "section": f"{classification} Record",
                "content": content,
                "evidence_type": "HISTORICAL_EVIDENCE",
                "source_type": "Medical Device Global Dataset"
            })

        texts = [d["content"] for d in documents]
        embeddings = embeddings_service.embed_documents(texts)

        vector_store.clear()
        vector_store.add_documents(documents, embeddings)
        bm25_retriever.index_documents(documents)

        self._is_indexed = True
        self._indexed_count = len(documents)
        return len(documents)


knowledge_ingestion_service = KnowledgeBaseIngestion()
