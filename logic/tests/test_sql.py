import pytest
from logic.text_to_sql.validator import sql_validator
from logic.text_to_sql.generator import text_to_sql_engine

def test_valid_select_query():
    is_safe, msg = sql_validator.validate("SELECT * FROM maintenance_logs WHERE equipment_id = 'EQ-001'")
    assert is_safe is True

def test_blocked_drop_query():
    is_safe, msg = sql_validator.validate("DROP TABLE maintenance_logs")
    assert is_safe is False
    assert "Only READ-ONLY SELECT queries are permitted" in msg

def test_blocked_delete_query():
    is_safe, msg = sql_validator.validate("DELETE FROM maintenance_logs WHERE id = 'LOG-101'")
    assert is_safe is False

def test_blocked_semicolon_chaining():
    is_safe, msg = sql_validator.validate("SELECT * FROM maintenance_logs; DROP TABLE maintenance_logs")
    assert is_safe is False

def test_text_to_sql_execution():
    res = text_to_sql_engine.execute_query("Show previous logs for EQ-001", equipment_id="EQ-001")
    assert res["is_safe"] is True
    assert len(res["results"]) > 0
