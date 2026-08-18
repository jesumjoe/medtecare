"""
Text & Record Chunking Utilities for RAG Knowledge Base.
Provides overlapping sliding-window chunking for technical documents
and structured document builders for medical device dataset records.
"""

from typing import List, Dict, Any

def chunk_text(text: str, chunk_size: int = 400, chunk_overlap: int = 50) -> List[str]:
    """Splits a long text string into overlapping chunks for dense vector embedding & BM25 indexing."""
    if not text or not text.strip():
        return []

    words = text.strip().split()
    if len(words) <= chunk_size:
        return [" ".join(words)]

    chunks = []
    step = max(1, chunk_size - chunk_overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
    return chunks

def format_medical_device_record(record: Dict[str, Any]) -> str:
    """Formats a medical device dataset row into a searchable, informative document chunk.
    
    Target Leakage Prevention:
    - Strictly omits `future_event` (prediction target).
    - Highlights historical safety record, classification, risk class, and operating metrics.
    """
    device_id = str(record.get("device_id") or record.get("id") or "UNKNOWN-DEV")
    device_name = str(record.get("device_name") or "Medical Device")
    classification = str(record.get("classification") or "General Medical Device")
    risk_class = str(record.get("risk_class") or "Class II")
    country = str(record.get("country") or "Global")
    manufacturer = str(record.get("manufacturer") or "Unknown Manufacturer")
    parent_company = str(record.get("parent_company") or manufacturer)
    prev_events = record.get("previous_events", 0)
    prev_recalls = record.get("previous_recalls", 0)
    prev_safety_notices = record.get("previous_safety_notices", 0)
    years_in_service = record.get("years_in_service", 1.0)

    lines = [
        f"[HISTORICAL MEDICAL DEVICE SAFETY RECORD]",
        f"Device ID: {device_id} | Name: {device_name}",
        f"Classification: {classification} | Regulatory Risk Class: {risk_class}",
        f"Manufacturer: {manufacturer} (Parent Entity: {parent_company}) | Origin: {country}",
        f"Operating Lifespan: {years_in_service} years in active clinical service.",
        f"Historical Safety Metrics: {prev_events} recorded previous malfunction event(s), "
        f"{prev_recalls} prior product recall(s), and {prev_safety_notices} regulatory safety notice(s).",
    ]

    # Include additional diagnostic notes if present in record (avoiding target leakage)
    if "failure_mode" in record or "defect_description" in record or "malfunction_type" in record:
        defect = record.get("failure_mode") or record.get("defect_description") or record.get("malfunction_type")
        lines.append(f"Historical Failure Mode / Defect Profile: {defect}")

    if "maintenance_notes" in record:
        lines.append(f"Historical Maintenance Notes: {record['maintenance_notes']}")

    return "\n".join(lines)
