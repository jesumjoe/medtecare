"""
Strict SQL Security Validator for Text-to-SQL Execution.
Rejects non-SELECT queries, SQL injection syntax, and destructive keywords.
"""

import re
from typing import Tuple

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE",
    "CREATE", "GRANT", "REVOKE", "REPLACE", "EXEC", "EXECUTE",
    "UNION", "--", "/*", "*/", "ATTACH", "DETACH", "PRAGMA"
]

class SQLValidator:
    """Security Validator enforcing Read-Only SELECT constraints."""

    def validate(self, sql_query: str) -> Tuple[bool, str]:
        """Validates that query is purely a single read-only SELECT statement."""
        if not sql_query or not isinstance(sql_query, str):
            return False, "Invalid SQL query format."

        clean_sql = sql_query.strip().upper()

        # Must begin with SELECT
        if not clean_sql.startswith("SELECT"):
            return False, "Security Violation: Only READ-ONLY SELECT queries are permitted."

        # Reject semicolon query chaining
        if ";" in clean_sql.strip(";"):
            return False, "Security Violation: Semicolon query chaining is prohibited."

        # Reject destructive keywords
        for keyword in FORBIDDEN_KEYWORDS:
            if re.search(r"\b" + re.escape(keyword) + r"\b", clean_sql):
                return False, f"Security Violation: Forbidden keyword '{keyword}' detected."

        return True, "SQL query validated as safe READ-ONLY SELECT statement."

sql_validator = SQLValidator()
