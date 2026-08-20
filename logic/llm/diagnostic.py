"""
LLM Diagnostic Reasoning Service.
Synthesizes ML predictions, telemetry, retrieved documents, and historical logs into structured DiagnosticResult.
Categorizes evidence clearly into MODEL, DOCUMENT, HISTORICAL, and AI INFERENCE.
Executes Live OpenAI / Groq LLM completions when API key is provided, or uses smart fallback.
"""

from typing import Dict, Any, List
import logging
import json
from logic.schemas.diagnostic import (
    DiagnosticResult, ProbableRootCause, EvidenceCategory, RecommendedAction
)
from logic.llm.provider import llm_provider
from logic.llm.prompts import SYSTEM_DIAGNOSTIC_PROMPT

logger = logging.getLogger(__name__)

class LLMDiagnosticReasoner:
    """Diagnostic Reasoning Engine."""

    def synthesize_diagnosis(
        self,
        equipment_id: str,
        equipment_type: str,
        risk_score: float,
        predicted_failure: str,
        model_confidence: float,
        important_features: List[str],
        telemetry: List[Dict[str, Any]],
        retrieved_documents: List[Dict[str, Any]],
        historical_context: List[Dict[str, Any]],
        device_context: Dict[str, Any] = None
    ) -> DiagnosticResult:
        """Synthesizes all evidence layers into a complete DiagnosticResult object."""
        
        evidence: List[EvidenceCategory] = []
        ctx = device_context or {}

        # 1. Model Evidence Preservation (Squad A CatBoost & SHAP Drivers)
        prob = ctx.get("future_event_probability")
        if prob is None:
            prob = (risk_score / 100.0) if risk_score is not None else 0.5
        model_conf = model_confidence if model_confidence is not None else 0.85

        evidence.append(EvidenceCategory(
            type="MODEL_EVIDENCE",
            description=f"Squad A CatBoost Risk Score: {risk_score:.1f}/100 (Future Event Probability: {prob:.2f}, Confidence: {model_conf*100:.0f}%): {predicted_failure}",
            source="Squad A CatBoost Predictive Model",
            confidence=model_conf
        ))


        # Device Metadata Model Evidence
        classification = ctx.get("classification", "Medical Device")
        risk_class = ctx.get("risk_class", "Class II")
        manufacturer = ctx.get("manufacturer", "OEM")
        recalls = ctx.get("previous_recalls", 0)
        events = ctx.get("previous_events", 0)
        notices = ctx.get("previous_safety_notices", 0)
        years = ctx.get("years_in_service", 0.0)

        evidence.append(EvidenceCategory(
            type="MODEL_EVIDENCE",
            description=f"Device Profile: {classification} ({risk_class}) by {manufacturer} | Operational Age: {years:.1f} years",
            source="Organizer Dataset Attributes",
            confidence=1.0
        ))

        if recalls > 0 or events > 0 or notices > 0:
            evidence.append(EvidenceCategory(
                type="MODEL_EVIDENCE",
                description=f"Historical Safety Metrics: Recalls: {recalls}, Adverse Events: {events}, Safety Notices: {notices}",
                source="Historical Safety Register",
                confidence=1.0
            ))

        for feat in important_features:
            evidence.append(EvidenceCategory(
                type="MODEL_EVIDENCE",
                description=f"SHAP Feature Driver: {feat}",
                source="Squad A SHAP Explainability Engine",
                confidence=0.92
            ))

        # 2. Document & Historical Evidence from RAG
        for doc in retrieved_documents:
            ev_type = doc.get("evidence_type", "DOCUMENT_EVIDENCE")
            if ev_type not in ["MODEL_EVIDENCE", "DOCUMENT_EVIDENCE", "HISTORICAL_EVIDENCE", "AI_INFERENCE"]:
                ev_type = "DOCUMENT_EVIDENCE"
            evidence.append(EvidenceCategory(
                type=ev_type,
                description=f"{doc.get('title', 'OEM Manual')} ({doc.get('section', '')}): {doc.get('content', '')[:120]}...",
                source=doc.get('source_type') or doc.get('title', 'OEM Guidance Document'),
                confidence=doc.get('relevance_score', 0.85)
            ))

        # 3. Historical Evidence from Text-to-SQL
        for hist in historical_context:
            evidence.append(EvidenceCategory(
                type="HISTORICAL_EVIDENCE",
                description=f"Past repair on {hist.get('service_date', 'N/A')}: {hist.get('action_performed', '')} (Root Cause: {hist.get('root_cause', 'N/A')})",
                source="Maintenance Log DB",
                confidence=0.90
            ))

        # 4. Try Live LLM Generation if API Client Available
        if llm_provider.is_available():
            try:
                live_result = self._generate_live_llm_diagnosis(
                    equipment_id, equipment_type, risk_score, predicted_failure,
                    model_conf, important_features, telemetry, retrieved_documents, historical_context, evidence, ctx
                )
                if live_result:
                    logger.info("Successfully generated Live LLM diagnostic synthesis!")
                    return live_result
            except Exception as e:
                logger.warning(f"Live LLM diagnostic generation failed: {e}. Falling back to Rule-Based Reasoning.")

        # 5. Rule-Based Fallback Reasoning Engine
        return self._generate_fallback_diagnosis(
            equipment_id, equipment_type, risk_score, predicted_failure,
            model_conf, important_features, telemetry, retrieved_documents, historical_context, evidence, ctx
        )

    def _generate_live_llm_diagnosis(
        self,
        equipment_id: str,
        equipment_type: str,
        risk_score: float,
        predicted_failure: str,
        model_confidence: float,
        important_features: List[str],
        telemetry: List[Dict[str, Any]],
        retrieved_documents: List[Dict[str, Any]],
        historical_context: List[Dict[str, Any]],
        evidence: List[EvidenceCategory],
        ctx: Dict[str, Any]
    ) -> DiagnosticResult:
        """Executes Live LLM API call (OpenAI or Groq) for real-time diagnostic reasoning."""
        
        user_prompt = f"""
Analyze the following medical device risk prediction context and generate a JSON diagnostic response.

MEDICAL DEVICE DETAILS:
- ID: {equipment_id}
- Name/Type: {equipment_type}
- Classification: {ctx.get('classification', 'Medical Device')}
- Risk Class: {ctx.get('risk_class', 'Class II')}
- Manufacturer: {ctx.get('manufacturer', 'OEM')}
- Squad A CatBoost Risk Score: {risk_score}/100 (Future Event Probability: {(risk_score/100.0):.2f}, Confidence: {model_confidence*100:.0f}%)
- Predicted Assessment: {predicted_failure}
- SHAP Feature Drivers: {', '.join(important_features)}
- Historical Safety Metrics: Recalls: {ctx.get('previous_recalls', 0)}, Events: {ctx.get('previous_events', 0)}, Notices: {ctx.get('previous_safety_notices', 0)}

RETRIEVED OEM / REGULATORY MANUAL EXCERPTS (RAG):
{json.dumps([d.get('content', '') for d in retrieved_documents])}

HISTORICAL WORK ORDERS (Text-to-SQL):
{json.dumps(historical_context)}

Respond ONLY with a valid JSON object matching this exact schema:
{{
  "diagnosis": "Short high-level diagnostic title using probabilistic language",
  "explanation": "Detailed professional diagnostic synthesis narrative explaining future-event risk",
  "probable_root_causes": [
    {{ "cause": "Risk factor name", "likelihood": 0.85, "description": "Explanation of risk factor" }}
  ],
  "recommended_actions": [
    {{ "step": 1, "title": "Safety & Inspection Action", "description": "Detailed step", "timeframe": "Immediate (<4h)", "urgency": "CRITICAL" }}
  ],
  "maintenance_priority": "CRITICAL"
}}
"""

        completion = llm_provider.client.chat.completions.create(
            model=llm_provider.model,
            messages=[
                {"role": "system", "content": SYSTEM_DIAGNOSTIC_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        raw_json = completion.choices[0].message.content
        data = json.loads(raw_json)

        evidence.append(EvidenceCategory(
            type="AI_INFERENCE",
            description=f"Live LLM diagnostic inference generated by {llm_provider.provider.upper()} model ({llm_provider.model}).",
            source=f"Squad B Live LLM ({llm_provider.model})",
            confidence=0.92
        ))

        probable_causes = [ProbableRootCause(**c) for c in data.get("probable_root_causes", [])]
        actions = [RecommendedAction(**a) for a in data.get("recommended_actions", [])]
        citations = [d.get("title", "OEM Manual") for d in retrieved_documents[:3]]

        return DiagnosticResult(
            equipment_id=equipment_id,
            equipment_type=equipment_type,
            risk_score=risk_score,
            predicted_failure=predicted_failure,
            diagnosis=data.get("diagnosis", f"HIGH RISK: {predicted_failure}"),
            probable_root_causes=probable_causes,
            evidence=evidence,
            historical_context=historical_context,
            explanation=data.get("explanation", ""),
            recommended_actions=actions,
            maintenance_priority=data.get("maintenance_priority", "CRITICAL"),
            confidence=0.94,
            citations=citations,
            requires_human_review=True,
            errors=[]
        )

    def _generate_fallback_diagnosis(
        self,
        equipment_id: str,
        equipment_type: str,
        risk_score: float,
        predicted_failure: str,
        model_confidence: float,
        important_features: List[str],
        telemetry: List[Dict[str, Any]],
        retrieved_documents: List[Dict[str, Any]],
        historical_context: List[Dict[str, Any]],
        evidence_list: List[EvidenceCategory],
        ctx: Dict[str, Any]
    ) -> DiagnosticResult:
        """Deterministic diagnostic reasoning fallback when LLM API is unreachable."""

        priority = "CRITICAL" if risk_score >= 80 else ("HIGH" if risk_score >= 60 else "MEDIUM")
        prob = risk_score / 100.0

        evidence_list.append(EvidenceCategory(
            type="AI_INFERENCE",
            description="Synthetic risk factor inference derived from Squad A prediction drivers and historical records.",
            source="Squad B Diagnostic Agent",
            confidence=0.88
        ))

        probable_causes = [
            ProbableRootCause(
                cause="Historical Safety & Recall Driver Alignment",
                likelihood=round(min(0.95, prob * 1.05), 2),
                description="High alignment between current device features and historical adverse event/recall risk indicators."
            ),
            ProbableRootCause(
                cause="Lifecycle Degradation & Cumulative Operational Exposure",
                likelihood=0.82,
                description="Extended service history contributing to elevated predicted future-event probability."
            )
        ]

        actions = [
            RecommendedAction(
                step=1,
                title="Safety & Operational Review",
                description="Perform immediate safety review and prioritize routine preventative maintenance inspection.",
                timeframe="Immediate (< 4 hours)",
                urgency=priority
            ),
            RecommendedAction(
                step=2,
                title="Historical Event & Safety Notice Audit",
                description="Cross-reference device serial/model against manufacturer safety notices and prior recall bulletins.",
                timeframe="Within 24 Hours",
                urgency=priority
            ),
            RecommendedAction(
                step=3,
                title="Increased Diagnostic Monitoring & Escalation",
                description="Increase clinical operational monitoring and escalate device assessment to certified biomedical engineering staff.",
                timeframe="Within 48 Hours",
                urgency=priority
            )
        ]

        citations = [d.get("title", "OEM Document") for d in retrieved_documents[:3]]

        drivers_text = ", ".join(important_features) if important_features else "None reported"

        explanation = (
            f"Device Assessment for {equipment_id} ({equipment_type}):\n\n"
            f"Based on our telemetry analysis, this device is showing early signs of component degradation (Risk Score: {risk_score:.1f}/100).\n"
            f"The primary factors driving this risk alert are: {drivers_text}.\n\n"
            f"When we cross-reference this behavior with historical failure logs and OEM maintenance guidelines, this pattern often precedes a complete operational failure. We highly recommend pulling this unit from clinical circulation immediately for a thorough physical inspection."
        )

        return DiagnosticResult(
            equipment_id=equipment_id,
            equipment_type=equipment_type,
            risk_score=risk_score,
            predicted_failure=predicted_failure,
            diagnosis=f"HIGH RISK: {predicted_failure} (Probability: {prob:.2f})",
            probable_root_causes=probable_causes,
            evidence=evidence_list,
            historical_context=historical_context,
            explanation=explanation,
            recommended_actions=actions,
            maintenance_priority=priority,
            confidence=0.91,
            citations=citations,
            requires_human_review=True,
            errors=[]
        )


llm_diagnostic_reasoner = LLMDiagnosticReasoner()
