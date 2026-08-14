"""
Node 4: Retrieve Historical Maintenance Context via Text-to-SQL.
"""

from typing import Dict, Any
from logic.text_to_sql.generator import text_to_sql_engine

def retrieve_historical_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Queries historical maintenance work orders using safe read-only SQL."""
    eq_id = state.get("equipment_id", "EQ-001")
    sql_res = text_to_sql_engine.execute_query(
        natural_query=f"Show previous maintenance logs for {eq_id}",
        equipment_id=eq_id
    )
    state["historical_context"] = sql_res.get("results", [])
    return state
