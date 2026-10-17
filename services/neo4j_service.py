"""
SkillGraph AI — Centralized Neo4j Service
Manages driver lifecycle, connection health checks, parameterized query execution,
and explicit LIVE vs DEMO status tracking.
"""

import os
from typing import Dict, List, Optional, Tuple, Any

try:
    from neo4j import GraphDatabase, Driver
    HAS_NEO4J = True
except ImportError:
    HAS_NEO4J = False
    Driver = Any


def get_neo4j_credentials(secrets_dict: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Retrieve Neo4j credentials from Streamlit secrets dictionary or OS environment."""
    uri = None
    username = None
    password = None

    if secrets_dict:
        uri = secrets_dict.get("NEO4J_URI")
        username = secrets_dict.get("NEO4J_USERNAME")
        password = secrets_dict.get("NEO4J_PASSWORD")

    if not uri:
        uri = os.environ.get("NEO4J_URI")
    if not username:
        username = os.environ.get("NEO4J_USERNAME")
    if not password:
        password = os.environ.get("NEO4J_PASSWORD")

    return uri, username, password


class Neo4jService:
    """Centralized database service managing Neo4j connection lifecycle and queries."""

    def __init__(self, uri: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver: Optional[Driver] = None
        self._connected = False
        self._connection_error: Optional[str] = None

        if HAS_NEO4J and uri and username and password:
            try:
                self.driver = GraphDatabase.driver(uri, auth=(username, password))
                self.driver.verify_connectivity()
                self._connected = True
            except Exception as e:
                self._connected = False
                self._connection_error = str(e)
        else:
            if not HAS_NEO4J:
                self._connection_error = "neo4j Python package is not installed."
            else:
                self._connection_error = "Neo4j credentials not configured."

    @property
    def is_connected(self) -> bool:
        """True if driver is connected to a live verified Neo4j cluster."""
        return self._connected

    @property
    def is_live_mode(self) -> bool:
        """Explicit indicator of LIVE vs DEMO mode."""
        return self._connected

    @property
    def status_message(self) -> str:
        if self._connected:
            return f"Connected to Neo4j Aura ({self.masked_uri})"
        return f"Demo Mode: {self._sanitize_error(self._connection_error)}"

    @property
    def masked_uri(self) -> str:
        """Returns the URI with any embedded credentials securely masked."""
        if not self.uri:
            return "Demo Mode (In-Memory Graph)"
        import re
        return re.sub(r'://([^:]+):([^@]+)@', r'://\1:******@', self.uri)

    def _sanitize_error(self, err_msg: Optional[str]) -> str:
        """Sanitizes connection error strings by stripping sensitive passwords or tokens."""
        if not err_msg:
            return ""
        sanitized = err_msg
        if self.password and self.password in sanitized:
            sanitized = sanitized.replace(self.password, "******")
        if self.uri and "@" in self.uri:
            # Mask user:pass@ inside URI in error text
            import re
            sanitized = re.sub(r'://([^:]+):([^@]+)@', r'://\1:******@', sanitized)
        return sanitized

    def close(self):
        """Cleanly close driver resources."""
        if self.driver:
            try:
                self.driver.close()
            except Exception:
                pass
            finally:
                self.driver = None
                self._connected = False

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Safely execute a parameterized read Cypher query within a session context."""
        if not self._connected or not self.driver:
            raise RuntimeError("Cannot execute live Cypher query: Neo4j is not connected.")

        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def run_health_check(self) -> Dict[str, Any]:
        """
        Runs comprehensive, non-destructive health checks against the configured database.
        Safely executes a lightweight query: RETURN 1 AS healthy.
        Returns structured diagnostic report with PASS/WARN/FAIL/DEMO statuses.
        Never displays passwords or secret tokens.
        """
        diagnostics = {
            "credentials_present": False,
            "connection_established": False,
            "read_query_success": False,
            "labels_found": [],
            "relationships_found": [],
            "career_count": 0,
            "skill_count": 0,
            "overall_status": "DEMO",
            "message": "",
            "masked_uri": self.masked_uri
        }

        # Check credentials configuration
        if not self.uri or not self.username or not self.password:
            diagnostics["overall_status"] = "DEMO"
            diagnostics["message"] = "Credentials not configured. Running in Demo Mode with full graph snapshot."
            return diagnostics

        diagnostics["credentials_present"] = True

        # Check driver connection
        if not self._connected or not self.driver:
            diagnostics["overall_status"] = "FAIL"
            diagnostics["message"] = f"Failed to connect: {self._sanitize_error(self._connection_error)}"
            return diagnostics

        try:
            # 1. Lightweight ping query: RETURN 1 AS healthy
            with self.driver.session() as session:
                res = session.run("RETURN 1 AS healthy")
                record = res.single()
                if not record or record.get("healthy") != 1:
                    diagnostics["read_query_success"] = False
                    diagnostics["overall_status"] = "FAIL"
                    diagnostics["message"] = "Ping query 'RETURN 1 AS healthy' did not return expected result."
                    return diagnostics

            diagnostics["read_query_success"] = True
            diagnostics["connection_established"] = True

            # 2. Schema check: Node labels
            try:
                labels_res = self.execute_query("CALL db.labels() YIELD label RETURN collect(label) AS labels")
                if labels_res:
                    diagnostics["labels_found"] = labels_res[0].get("labels", [])
            except Exception:
                pass

            # 3. Schema check: Relationship types
            try:
                rels_res = self.execute_query("CALL db.relationshipTypes() YIELD relationshipType RETURN collect(relationshipType) AS types")
                if rels_res:
                    diagnostics["relationships_found"] = rels_res[0].get("types", [])
            except Exception:
                pass

            # 4. Data counts: Careers
            try:
                career_cnt = self.execute_query("MATCH (c:Career) RETURN count(c) AS cnt")
                if career_cnt:
                    diagnostics["career_count"] = career_cnt[0].get("cnt", 0)
            except Exception:
                pass

            # 5. Data counts: Skills
            try:
                skill_cnt = self.execute_query("MATCH (s:Skill) RETURN count(s) AS cnt")
                if skill_cnt:
                    diagnostics["skill_count"] = skill_cnt[0].get("cnt", 0)
            except Exception:
                pass

            diagnostics["overall_status"] = "PASS"
            diagnostics["message"] = f"Live Neo4j cluster healthy with {diagnostics['career_count']} careers and {diagnostics['skill_count']} skills."

        except Exception as e:
            # Catch authentication errors, timeouts, or network drops
            diagnostics["read_query_success"] = False
            diagnostics["overall_status"] = "FAIL"
            diagnostics["message"] = f"Query execution failed: {self._sanitize_error(str(e))}"

        return diagnostics
