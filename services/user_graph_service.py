"""
SkillGraph AI — User Graph & Data Persistence Service
Manages user-isolated skill areas, individual skills, graph relationships,
career goals, job applications, feedback, and notifications.
Integrates with live Neo4j Aura when configured, and SQLite for guaranteed local persistence.
"""

import os
import json
import sqlite3
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from services.neo4j_service import Neo4jService


class UserGraphService:
    """Manages persistent graph nodes and user application data."""

    def __init__(self, neo4j_service: Optional[Neo4jService] = None, db_path: str = "data/user_profiles.db"):
        self.neo4j = neo4j_service
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_sqlite()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_sqlite(self):
        with self._get_connection() as conn:
            # Skill Areas table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_skill_areas (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    color TEXT DEFAULT '#EA580C',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Individual Skills table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_skills (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    area_id TEXT,
                    name TEXT NOT NULL,
                    proficiency TEXT DEFAULT 'Beginner',
                    status TEXT DEFAULT 'Learning',
                    progress INTEGER DEFAULT 30,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Graph Relationships table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_relationships (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    rel_type TEXT DEFAULT 'requires',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Career Goals table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_goals (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    objective TEXT,
                    target_date TEXT,
                    status TEXT DEFAULT 'In Progress',
                    linked_skills TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Job Applications table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_applications (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    location TEXT,
                    status TEXT DEFAULT 'Interested',
                    date_applied TEXT,
                    notes TEXT,
                    url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # User Notifications table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_notifications (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    type TEXT DEFAULT 'info',
                    read INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Feedback table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_feedback (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    rating INTEGER,
                    category TEXT,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # =========================================================================
    # STARTER SEED FOR NEW USER GRAPH
    # =========================================================================
    def ensure_user_starter_graph(self, user_id: str):
        """Ensures a new user has initial foundational areas and skills."""
        areas = self.get_user_areas(user_id)
        if areas:
            return  # Already has data

        # Seed initial starter areas
        swe_area_id = self.create_area(user_id, "Software Engineering", "Core principles of scalable software development")
        ai_area_id = self.create_area(user_id, "Machine Learning", "Statistical modeling, deep learning, and AI pipelines")
        web_area_id = self.create_area(user_id, "Web Development", "Modern full-stack web and cloud systems")

        # Seed starter skills
        s_git = self.create_skill(user_id, "Git", swe_area_id, proficiency="Intermediate", status="Mastered", progress=100)
        s_py = self.create_skill(user_id, "Python", swe_area_id, proficiency="Advanced", status="Mastered", progress=100)
        s_algo = self.create_skill(user_id, "Data Structures", swe_area_id, proficiency="Intermediate", status="Learning", progress=60)
        
        s_math = self.create_skill(user_id, "Linear Algebra", ai_area_id, proficiency="Beginner", status="Learning", progress=40)
        s_ml = self.create_skill(user_id, "Deep Learning", ai_area_id, proficiency="Beginner", status="Not Started", progress=10)
        
        s_js = self.create_skill(user_id, "TypeScript", web_area_id, proficiency="Intermediate", status="Learning", progress=50)
        s_react = self.create_skill(user_id, "React", web_area_id, proficiency="Beginner", status="Not Started", progress=0)

        # Seed starter relationships
        self.create_relationship(user_id, s_py, s_algo, "requires")
        self.create_relationship(user_id, s_py, s_ml, "requires")
        self.create_relationship(user_id, s_math, s_ml, "requires")
        self.create_relationship(user_id, s_js, s_react, "requires")

        # Seed initial notification
        self.add_notification(user_id, "Welcome to SkillGraph AI", "Your personalized career graph workspace has been initialized.", "info")

    # =========================================================================
    # SKILL AREAS CRUD
    # =========================================================================
    def get_user_areas(self, user_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM user_skill_areas WHERE user_id = ? ORDER BY name ASC",
                (user_id,)
            )
            return [dict(r) for r in cur.fetchall()]

    def create_area(self, user_id: str, name: str, description: str = "", color: str = "#EA580C") -> str:
        name_clean = name.strip()
        area_id = str(uuid.uuid4())

        # Check duplicate
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT id FROM user_skill_areas WHERE user_id = ? AND LOWER(name) = LOWER(?)",
                (user_id, name_clean)
            )
            existing = cur.fetchone()
            if existing:
                return existing["id"]

            conn.execute(
                "INSERT INTO user_skill_areas (id, user_id, name, description, color) VALUES (?, ?, ?, ?, ?)",
                (area_id, user_id, name_clean, description.strip(), color)
            )
            conn.commit()

        # Neo4j persistence if live
        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = """
                MERGE (u:User {id: $user_id})
                MERGE (a:SkillArea {id: $area_id})
                SET a.name = $name, a.description = $description, a.color = $color
                MERGE (u)-[:OWNS_AREA]->(a)
                """
                self.neo4j.execute_query(cypher, {
                    "user_id": user_id,
                    "area_id": area_id,
                    "name": name_clean,
                    "description": description.strip(),
                    "color": color
                })
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j create_area failed: {e}")

        return area_id

    def update_area(self, user_id: str, area_id: str, name: str, description: str = "") -> bool:
        name_clean = name.strip()
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE user_skill_areas SET name = ?, description = ? WHERE id = ? AND user_id = ?",
                (name_clean, description.strip(), area_id, user_id)
            )
            conn.commit()

        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = """
                MATCH (u:User {id: $user_id})-[:OWNS_AREA]->(a:SkillArea {id: $area_id})
                SET a.name = $name, a.description = $description
                """
                self.neo4j.execute_query(cypher, {
                    "user_id": user_id,
                    "area_id": area_id,
                    "name": name_clean,
                    "description": description.strip()
                })
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j update_area failed: {e}")

        return True

    def delete_area(self, user_id: str, area_id: str) -> bool:
        with self._get_connection() as conn:
            # Reassign skills to unassigned or delete
            conn.execute("UPDATE user_skills SET area_id = NULL WHERE area_id = ? AND user_id = ?", (area_id, user_id))
            conn.execute("DELETE FROM user_skill_areas WHERE id = ? AND user_id = ?", (area_id, user_id))
            conn.commit()

        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = """
                MATCH (u:User {id: $user_id})-[:OWNS_AREA]->(a:SkillArea {id: $area_id})
                DETACH DELETE a
                """
                self.neo4j.execute_query(cypher, {"user_id": user_id, "area_id": area_id})
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j delete_area failed: {e}")

        return True

    # =========================================================================
    # SKILLS CRUD
    # =========================================================================
    def get_user_skills(self, user_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute(
                """
                SELECT s.*, a.name AS area_name, a.color AS area_color
                FROM user_skills s
                LEFT JOIN user_skill_areas a ON s.area_id = a.id
                WHERE s.user_id = ?
                ORDER BY s.name ASC
                """,
                (user_id,)
            )
            return [dict(r) for r in cur.fetchall()]

    def create_skill(
        self,
        user_id: str,
        name: str,
        area_id: Optional[str] = None,
        proficiency: str = "Beginner",
        status: str = "Learning",
        progress: int = 25,
        description: str = ""
    ) -> str:
        name_clean = name.strip()
        skill_id = str(uuid.uuid4())

        # Check duplicate
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT id FROM user_skills WHERE user_id = ? AND LOWER(name) = LOWER(?)",
                (user_id, name_clean)
            )
            existing = cur.fetchone()
            if existing:
                return existing["id"]

            conn.execute(
                """
                INSERT INTO user_skills (id, user_id, area_id, name, proficiency, status, progress, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (skill_id, user_id, area_id, name_clean, proficiency, status, progress, description.strip())
            )
            conn.commit()

        # Neo4j persistence if live
        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = """
                MERGE (u:User {id: $user_id})
                MERGE (s:Skill {id: $skill_id})
                SET s.name = $name, s.proficiency = $proficiency, s.status = $status,
                    s.progress = $progress, s.description = $description
                MERGE (u)-[:HAS_SKILL]->(s)
                WITH s, u
                OPTIONAL MATCH (a:SkillArea {id: $area_id})
                FOREACH (_ IN CASE WHEN a IS NOT NULL THEN [1] ELSE [] END |
                    MERGE (a)-[:CONTAINS_SKILL]->(s)
                )
                """
                self.neo4j.execute_query(cypher, {
                    "user_id": user_id,
                    "skill_id": skill_id,
                    "area_id": area_id or "",
                    "name": name_clean,
                    "proficiency": proficiency,
                    "status": status,
                    "progress": progress,
                    "description": description.strip()
                })
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j create_skill failed: {e}")

        return skill_id

    def update_skill(self, user_id: str, skill_id: str, updates: Dict[str, Any]) -> bool:
        allowed = ["name", "area_id", "proficiency", "status", "progress", "description"]
        filtered = {k: v for k, v in updates.items() if k in allowed}
        if not filtered:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in filtered.keys()])
        params = list(filtered.values()) + [datetime.now().isoformat(), skill_id, user_id]

        with self._get_connection() as conn:
            conn.execute(
                f"UPDATE user_skills SET {set_clause}, updated_at = ? WHERE id = ? AND user_id = ?",
                params
            )
            conn.commit()

        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = """
                MATCH (u:User {id: $user_id})-[:HAS_SKILL]->(s:Skill {id: $skill_id})
                SET s += $updates
                """
                self.neo4j.execute_query(cypher, {
                    "user_id": user_id,
                    "skill_id": skill_id,
                    "updates": filtered
                })
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j update_skill failed: {e}")

        return True

    def delete_skill(self, user_id: str, skill_id: str) -> bool:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM user_relationships WHERE (source_id = ? OR target_id = ?) AND user_id = ?", (skill_id, skill_id, user_id))
            conn.execute("DELETE FROM user_skills WHERE id = ? AND user_id = ?", (skill_id, user_id))
            conn.commit()

        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = """
                MATCH (u:User {id: $user_id})-[:HAS_SKILL]->(s:Skill {id: $skill_id})
                DETACH DELETE s
                """
                self.neo4j.execute_query(cypher, {"user_id": user_id, "skill_id": skill_id})
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j delete_skill failed: {e}")

        return True

    # =========================================================================
    # RELATIONSHIPS CRUD
    # =========================================================================
    def get_user_relationships(self, user_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM user_relationships WHERE user_id = ?",
                (user_id,)
            )
            return [dict(r) for r in cur.fetchall()]

    def create_relationship(self, user_id: str, source_id: str, target_id: str, rel_type: str = "requires") -> Optional[str]:
        if source_id == target_id:
            return None

        rel_id = str(uuid.uuid4())
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT id FROM user_relationships WHERE user_id = ? AND source_id = ? AND target_id = ?",
                (user_id, source_id, target_id)
            )
            if cur.fetchone():
                return None  # Prevent duplicate

            conn.execute(
                "INSERT INTO user_relationships (id, user_id, source_id, target_id, rel_type) VALUES (?, ?, ?, ?, ?)",
                (rel_id, user_id, source_id, target_id, rel_type)
            )
            conn.commit()

        if self.neo4j and self.neo4j.is_connected:
            try:
                cypher = f"""
                MATCH (s:Skill {{id: $source_id}}), (t:Skill {{id: $target_id}})
                MERGE (s)-[:REQUIRES]->(t)
                """
                self.neo4j.execute_query(cypher, {"source_id": source_id, "target_id": target_id})
            except Exception as e:
                print(f"[UserGraphService Warning] Neo4j create_relationship failed: {e}")

        return rel_id

    def delete_relationship(self, user_id: str, rel_id: str) -> bool:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM user_relationships WHERE id = ? AND user_id = ?", (rel_id, user_id))
            conn.commit()
        return True

    # =========================================================================
    # FULL USER GRAPH VISUALIZATION DATA
    # =========================================================================
    def get_full_graph_data(
        self,
        user_id: str,
        show_skills: bool = True,
        show_relations: bool = True,
        level_filter: str = "All",
        progressing_only: bool = False
    ) -> Dict[str, Any]:
        """Generates nodes and links suitable for interactive Vis.js rendering."""
        areas = self.get_user_areas(user_id)
        skills = self.get_user_skills(user_id)
        relationships = self.get_user_relationships(user_id)

        nodes = []
        links = []

        area_id_map = {a["id"]: a for a in areas}
        skill_id_map = {s["id"]: s for s in skills}

        # 1. Add Skill Area nodes (hubs)
        for a in areas:
            nodes.append({
                "id": a["id"],
                "label": a["name"],
                "type": "Area",
                "color": a.get("color", "#EA580C"),
                "size": 32,
                "shape": "box",
                "description": a.get("description", "")
            })

        # 2. Add Skill nodes if enabled
        if show_skills:
            for s in skills:
                # Apply filters
                if level_filter != "All" and s.get("proficiency") != level_filter:
                    continue
                if progressing_only and s.get("status") not in ("Learning", "In Progress"):
                    continue

                nodes.append({
                    "id": s["id"],
                    "label": s["name"],
                    "type": "Skill",
                    "area_id": s.get("area_id"),
                    "area_name": s.get("area_name", "General"),
                    "proficiency": s.get("proficiency", "Beginner"),
                    "status": s.get("status", "Learning"),
                    "progress": s.get("progress", 30),
                    "description": s.get("description", "")
                })

                # Connect skill to parent area hub
                if s.get("area_id") and s.get("area_id") in area_id_map:
                    links.append({
                        "source": s["area_id"],
                        "target": s["id"],
                        "type": "contains",
                        "label": ""
                    })

        # 3. Add Relationships if enabled
        if show_relations:
            active_node_ids = {n["id"] for n in nodes}
            for r in relationships:
                if r["source_id"] in active_node_ids and r["target_id"] in active_node_ids:
                    links.append({
                        "id": r["id"],
                        "source": r["source_id"],
                        "target": r["target_id"],
                        "type": r.get("rel_type", "requires"),
                        "label": r.get("rel_type", "requires")
                    })

        return {"nodes": nodes, "links": links}

    # =========================================================================
    # CAREER GOALS CRUD
    # =========================================================================
    def get_user_goals(self, user_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM user_goals WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                try:
                    r["linked_skills"] = json.loads(r.get("linked_skills") or "[]")
                except Exception:
                    r["linked_skills"] = []
            return rows

    def create_goal(self, user_id: str, title: str, objective: str, target_date: str, linked_skills: List[str]) -> str:
        goal_id = str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO user_goals (id, user_id, title, objective, target_date, status, linked_skills)
                VALUES (?, ?, ?, ?, ?, 'In Progress', ?)
                """,
                (goal_id, user_id, title.strip(), objective.strip(), target_date, json.dumps(linked_skills))
            )
            conn.commit()
        return goal_id

    def update_goal(self, user_id: str, goal_id: str, updates: Dict[str, Any]) -> bool:
        if "linked_skills" in updates and isinstance(updates["linked_skills"], list):
            updates["linked_skills"] = json.dumps(updates["linked_skills"])
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        params = list(updates.values()) + [goal_id, user_id]
        with self._get_connection() as conn:
            conn.execute(f"UPDATE user_goals SET {set_clause} WHERE id = ? AND user_id = ?", params)
            conn.commit()
        return True

    def delete_goal(self, user_id: str, goal_id: str) -> bool:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM user_goals WHERE id = ? AND user_id = ?", (goal_id, user_id))
            conn.commit()
        return True

    # =========================================================================
    # JOB APPLICATIONS CRUD
    # =========================================================================
    def get_user_applications(self, user_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM user_applications WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
            return [dict(r) for r in cur.fetchall()]

    def create_application(
        self,
        user_id: str,
        company: str,
        role: str,
        location: str = "Remote",
        status: str = "Interested",
        date_applied: Optional[str] = None,
        notes: str = "",
        url: str = ""
    ) -> str:
        app_id = str(uuid.uuid4())
        date_val = date_applied or datetime.now().strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO user_applications (id, user_id, company, role, location, status, date_applied, notes, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (app_id, user_id, company.strip(), role.strip(), location.strip(), status, date_val, notes.strip(), url.strip())
            )
            conn.commit()
        return app_id

    def update_application(self, user_id: str, app_id: str, updates: Dict[str, Any]) -> bool:
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        params = list(updates.values()) + [datetime.now().isoformat(), app_id, user_id]
        with self._get_connection() as conn:
            conn.execute(f"UPDATE user_applications SET {set_clause}, updated_at = ? WHERE id = ? AND user_id = ?", params)
            conn.commit()
        return True

    def delete_application(self, user_id: str, app_id: str) -> bool:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM user_applications WHERE id = ? AND user_id = ?", (app_id, user_id))
            conn.commit()
        return True

    # =========================================================================
    # NOTIFICATIONS & FEEDBACK
    # =========================================================================
    def get_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM user_notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 20", (user_id,))
            return [dict(r) for r in cur.fetchall()]

    def add_notification(self, user_id: str, title: str, message: str, n_type: str = "info") -> str:
        nid = str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO user_notifications (id, user_id, title, message, type) VALUES (?, ?, ?, ?, ?)",
                (nid, user_id, title.strip(), message.strip(), n_type)
            )
            conn.commit()
        return nid

    def mark_notifications_read(self, user_id: str):
        with self._get_connection() as conn:
            conn.execute("UPDATE user_notifications SET read = 1 WHERE user_id = ?", (user_id,))
            conn.commit()

    def submit_feedback(self, user_id: str, rating: int, category: str, comment: str) -> str:
        fid = str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO user_feedback (id, user_id, rating, category, comment) VALUES (?, ?, ?, ?, ?)",
                (fid, user_id, rating, category, comment.strip())
            )
            conn.commit()
        return fid
