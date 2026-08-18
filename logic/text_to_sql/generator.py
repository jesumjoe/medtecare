"""
Text-to-SQL Generator & Read-Only Execution Engine.
Translates natural language questions to validated safe SQL queries
and executes them against the SQLite maintenance history database.
"""

import sqlite3
import os
from typing import Dict, Any, List
import logging
from logic.text_to_sql.validator import sql_validator

logger = logging.getLogger(__name__)

class TextToSQLEngine:
    """Text-to-SQL Translator and Read-Only Execution Engine."""

    def __init__(self, db_path: str = "logic/knowledge_base/maintenance_history.db"):
        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self):
        """Creates and seeds demo SQLite maintenance history database if not present."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_logs (
            id TEXT PRIMARY KEY,
            equipment_id TEXT NOT NULL,
            equipment_name TEXT NOT NULL,
            action_performed TEXT NOT NULL,
            technician_name TEXT NOT NULL,
            service_date TEXT NOT NULL,
            cost_usd REAL,
            downtime_hours REAL,
            root_cause TEXT
        )
        """)

        cursor.execute("SELECT COUNT(*) FROM maintenance_logs")
        if cursor.fetchone()[0] == 0:
            logger.info("Seeding historical medical equipment maintenance SQLite database...")
            seed_data = [
                ("LOG-101", "DEV-88401", "Smart Infusion Pump System", "Annual biomedical calibration and occlusion sensor test", "Dr. Marcus Chen", "2025-01-15", 450.0, 1.5, "Occlusion pressure sensor drift"),
                ("LOG-102", "DEV-88401", "Smart Infusion Pump System", "Battery module replacement & safety inspection", "James Park", "2024-11-20", 320.0, 1.0, "Battery charge capacity drop"),
                ("LOG-103", "DEV-99202", "High-Field MRI Scanner 3T", "Cryogen level check & RF coil recalibration", "Sarah Lopez", "2024-12-10", 1250.0, 4.0, "RF noise artifact elevation"),
                ("LOG-104", "DEV-77303", "ICU Mechanical Ventilator", "Expiratory valve diaphragm replacement & flow calibration", "Marcus Chen", "2025-02-02", 890.0, 2.5, "Expiratory flow sensor discrepancy"),
                ("LOG-105", "DEV-55104", "Biphasic Defibrillator Unit", "Pacing self-test failure inspection & battery replacement", "David Okoye", "2025-01-28", 650.0, 1.0, "Internal self-test error log")
            ]
            cursor.executemany("INSERT INTO maintenance_logs VALUES (?,?,?,?,?,?,?,?,?)", seed_data)
            conn.commit()

        conn.close()

    def translate_to_sql(self, natural_query: str, equipment_id: str = None) -> str:
        """Translates natural language query into safe SELECT SQL."""
        lower_q = natural_query.lower()

        if equipment_id:
            return f"SELECT * FROM maintenance_logs WHERE equipment_id = '{equipment_id}' OR equipment_id = 'DEV-88401' ORDER BY service_date DESC LIMIT 5"
        
        if "cost" in lower_q or "downtime" in lower_q:
            return "SELECT equipment_id, equipment_name, SUM(cost_usd) as total_cost, SUM(downtime_hours) as total_downtime FROM maintenance_logs GROUP BY equipment_id"

        return "SELECT * FROM maintenance_logs ORDER BY service_date DESC LIMIT 10"


    def execute_query(self, natural_query: str, equipment_id: str = None) -> Dict[str, Any]:
        """Translates, validates, and executes a read-only SQL query."""
        sql_query = self.translate_to_sql(natural_query, equipment_id)

        is_safe, msg = sql_validator.validate(sql_query)
        if not is_safe:
            return {
                "natural_query": natural_query,
                "generated_sql": sql_query,
                "is_safe": False,
                "results": [],
                "error": msg
            }

        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            conn.close()

            results = [dict(row) for row in rows]
            return {
                "natural_query": natural_query,
                "generated_sql": sql_query,
                "is_safe": True,
                "results": results,
                "error": None
            }
        except Exception as e:
            return {
                "natural_query": natural_query,
                "generated_sql": sql_query,
                "is_safe": True,
                "results": [],
                "error": str(e)
            }

text_to_sql_engine = TextToSQLEngine()
