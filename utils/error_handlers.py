"""
SkillGraph AI — Error Handling Utilities
Standardized exception formatting and diagnostic error reporting.
"""

from typing import Dict, Any, Optional


class SkillGraphError(Exception):
    """Base exception for SkillGraph AI domain errors."""
    pass


class DatabaseConnectionError(SkillGraphError):
    """Raised when live Neo4j connection fails."""
    pass


class InvalidGraphSchemaError(SkillGraphError):
    """Raised when graph data is corrupted or violates constraints."""
    pass


def format_error_for_display(error: Exception, context: str = "") -> Dict[str, str]:
    """Sanitize and format errors for user-facing Streamlit display (never exposing secrets)."""
    raw_msg = str(error)
    # Mask any potential password strings
    sanitized = raw_msg
    for keyword in ["password", "pwd", "secret", "auth"]:
        if keyword in sanitized.lower():
            sanitized = f"An error occurred during {context or 'operation'}: Authentication or connectivity failure."
            break

    return {
        "title": f"Notice: {context}" if context else "System Notice",
        "message": sanitized,
        "type": error.__class__.__name__
    }
