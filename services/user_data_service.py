"""
SkillGraph AI — User Data Service
Isolates user-specific career objectives, completed competencies, velocity preferences,
and capstone progress by stable user ID, preventing cross-user data leakage.
"""

import os
import json
import sqlite3
from typing import Dict, Any, List, Optional


DEFAULT_USER_DATA = {
    "selected_career_target": "AI Engineer",
    "selected_skills": ["Python", "Git"],
    "completed_skills": ["Python", "Git"],
    "in_progress_skills": [],
    "completed_projects": [],
    "weekly_hours": 15,
    "education_level": "Bachelor's Degree"
}


class UserDataService:
    """Manages isolated user profiles and learning progress records."""

    def __init__(self, db_path: str = "data/user_profiles.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    career_target TEXT NOT NULL,
                    selected_skills TEXT NOT NULL,
                    completed_skills TEXT NOT NULL,
                    in_progress_skills TEXT NOT NULL,
                    completed_projects TEXT NOT NULL,
                    weekly_hours INTEGER NOT NULL,
                    education_level TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def load_user_data(self, user_id: str) -> Dict[str, Any]:
        """Loads personal settings and progress for the given user ID."""
        if not user_id:
            return dict(DEFAULT_USER_DATA)

        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    """
                    SELECT career_target, selected_skills, completed_skills,
                           in_progress_skills, completed_projects, weekly_hours,
                           education_level
                    FROM user_profiles WHERE user_id = ?
                    """,
                    (user_id,)
                )
                row = cur.fetchone()

            if row:
                return {
                    "selected_career_target": row["career_target"],
                    "selected_skills": json.loads(row["selected_skills"]),
                    "completed_skills": json.loads(row["completed_skills"]),
                    "in_progress_skills": json.loads(row["in_progress_skills"]),
                    "completed_projects": json.loads(row["completed_projects"]),
                    "weekly_hours": int(row["weekly_hours"]),
                    "education_level": row["education_level"]
                }
        except Exception as e:
            print(f"[UserDataService Warning] Load failed for {user_id}: {e}")

        # Return defaults for new accounts
        return dict(DEFAULT_USER_DATA)

    def save_user_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Saves personal settings and progress for the given user ID."""
        if not user_id:
            return False

        career_target = data.get("selected_career_target", "AI Engineer")
        selected_skills = json.dumps(data.get("selected_skills", ["Python", "Git"]))
        completed_skills = json.dumps(data.get("completed_skills", ["Python", "Git"]))
        in_progress_skills = json.dumps(data.get("in_progress_skills", []))
        completed_projects = json.dumps(data.get("completed_projects", []))
        weekly_hours = int(data.get("weekly_hours", 15))
        education_level = data.get("education_level", "Bachelor's Degree")

        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO user_profiles (
                        user_id, career_target, selected_skills, completed_skills,
                        in_progress_skills, completed_projects, weekly_hours, education_level, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(user_id) DO UPDATE SET
                        career_target = excluded.career_target,
                        selected_skills = excluded.selected_skills,
                        completed_skills = excluded.completed_skills,
                        in_progress_skills = excluded.in_progress_skills,
                        completed_projects = excluded.completed_projects,
                        weekly_hours = excluded.weekly_hours,
                        education_level = excluded.education_level,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        user_id, career_target, selected_skills, completed_skills,
                        in_progress_skills, completed_projects, weekly_hours, education_level
                    )
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"[UserDataService Warning] Save failed for {user_id}: {e}")
            return False
