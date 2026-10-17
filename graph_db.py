"""
SkillGraph AI — Graph Database Layer & Career Analytics Engine
Neo4j Driver Integration + Demo Mode Fallback Engine
"""

import os
from collections import defaultdict, deque
from typing import Dict, List, Optional, Set, Tuple, Any

try:
    from neo4j import GraphDatabase, Driver
    HAS_NEO4J_LIB = True
except ImportError:
    HAS_NEO4J_LIB = False
    Driver = Any


# ==============================================================================
# DEMO MODE GRAPH DATASET (Matches database/seed.cypher 1-to-1)
# ==============================================================================

DEMO_CAREERS = [
    {
        "id": "ai_engineer",
        "name": "AI Engineer",
        "category": "Artificial Intelligence",
        "avg_salary_range": "$130k - $190k",
        "description": "Designs, deploys, and scales machine learning and generative AI models into production environments.",
        "skills": [
            {"name": "Python", "importance": "Core"},
            {"name": "Machine Learning", "importance": "Core"},
            {"name": "Deep Learning", "importance": "Core"},
            {"name": "Neural Networks", "importance": "Specialized"},
            {"name": "Statistics", "importance": "Foundational"},
            {"name": "APIs", "importance": "Foundational"},
            {"name": "Git", "importance": "Foundational"},
            {"name": "Cloud Computing", "importance": "Intermediate"},
            {"name": "MLOps", "importance": "Specialized"}
        ]
    },
    {
        "id": "data_scientist",
        "name": "Data Scientist",
        "category": "Data Science",
        "avg_salary_range": "$115k - $165k",
        "description": "Extracts actionable business insights using statistical inference, machine learning, and predictive modeling.",
        "skills": [
            {"name": "Python", "importance": "Core"},
            {"name": "SQL", "importance": "Core"},
            {"name": "Statistics", "importance": "Core"},
            {"name": "Data Analysis", "importance": "Core"},
            {"name": "Machine Learning", "importance": "Core"},
            {"name": "Data Visualization", "importance": "Intermediate"},
            {"name": "Deep Learning", "importance": "Specialized"},
            {"name": "Git", "importance": "Foundational"}
        ]
    },
    {
        "id": "software_developer",
        "name": "Software Developer",
        "category": "Software Engineering",
        "avg_salary_range": "$105k - $155k",
        "description": "Builds robust, high-performance web applications, services, APIs, and scalable distributed backend systems.",
        "skills": [
            {"name": "Python", "importance": "Core"},
            {"name": "Data Structures", "importance": "Core"},
            {"name": "Algorithms", "importance": "Core"},
            {"name": "Git", "importance": "Core"},
            {"name": "APIs", "importance": "Core"},
            {"name": "Web Development", "importance": "Core"},
            {"name": "SQL", "importance": "Intermediate"},
            {"name": "Linux", "importance": "Intermediate"},
            {"name": "Cloud Computing", "importance": "Specialized"}
        ]
    },
    {
        "id": "cybersecurity_analyst",
        "name": "Cybersecurity Analyst",
        "category": "Security",
        "avg_salary_range": "$95k - $145k",
        "description": "Protects networks, endpoints, systems, and cloud infrastructure from threats, vulnerabilities, and intrusions.",
        "skills": [
            {"name": "Networking", "importance": "Core"},
            {"name": "Security Fundamentals", "importance": "Core"},
            {"name": "Linux", "importance": "Core"},
            {"name": "Python", "importance": "Core"},
            {"name": "Cloud Computing", "importance": "Specialized"},
            {"name": "Git", "importance": "Foundational"},
            {"name": "SQL", "importance": "Foundational"}
        ]
    },
    {
        "id": "data_analyst",
        "name": "Data Analyst",
        "category": "Analytics",
        "avg_salary_range": "$75k - $115k",
        "description": "Transforms raw telemetry and databases into interactive dashboards, reports, and data-driven narratives.",
        "skills": [
            {"name": "SQL", "importance": "Core"},
            {"name": "Data Analysis", "importance": "Core"},
            {"name": "Data Visualization", "importance": "Core"},
            {"name": "Statistics", "importance": "Core"},
            {"name": "Python", "importance": "Intermediate"},
            {"name": "Git", "importance": "Foundational"}
        ]
    }
]

DEMO_SKILLS = [
    {"id": "python", "name": "Python", "category": "Programming", "difficulty": "Foundational", "estimated_hours": 40, "description": "Core programming language for software, automation, data science, and AI pipelines."},
    {"id": "sql", "name": "SQL", "category": "Databases", "difficulty": "Foundational", "estimated_hours": 30, "description": "Relational querying language for filtering, aggregation, joins, and data manipulation."},
    {"id": "statistics", "name": "Statistics", "category": "Mathematics", "difficulty": "Foundational", "estimated_hours": 35, "description": "Probability distributions, hypothesis testing, regression analysis, and variance."},
    {"id": "data_analysis", "name": "Data Analysis", "category": "Analytics", "difficulty": "Intermediate", "estimated_hours": 35, "description": "Exploratory data analysis, cohort analysis, metric tracking, and anomaly detection."},
    {"id": "data_visualization", "name": "Data Visualization", "category": "Analytics", "difficulty": "Intermediate", "estimated_hours": 25, "description": "Designing visual charts and executive dashboards using Plotly, Seaborn, Tableau, or PowerBI."},
    {"id": "machine_learning", "name": "Machine Learning", "category": "AI & Data Science", "difficulty": "Intermediate", "estimated_hours": 50, "description": "Supervised and unsupervised learning, decision trees, gradient boosting, and evaluation metrics."},
    {"id": "deep_learning", "name": "Deep Learning", "category": "AI & Data Science", "difficulty": "Advanced", "estimated_hours": 60, "description": "Multi-layer neural architectures, backpropagation, PyTorch/TensorFlow, and GPU training."},
    {"id": "neural_networks", "name": "Neural Networks", "category": "AI & Data Science", "difficulty": "Advanced", "estimated_hours": 45, "description": "Convolutional (CNNs), Recurrent (RNNs), Transformers, and attention mechanisms."},
    {"id": "git", "name": "Git", "category": "Development Tools", "difficulty": "Foundational", "estimated_hours": 15, "description": "Version control, branch management, merge conflict resolution, and collaborative PRs."},
    {"id": "data_structures", "name": "Data Structures", "category": "Computer Science", "difficulty": "Foundational", "estimated_hours": 40, "description": "Arrays, linked lists, hash tables, stacks, queues, trees, and graphs."},
    {"id": "algorithms", "name": "Algorithms", "category": "Computer Science", "difficulty": "Intermediate", "estimated_hours": 45, "description": "Time/space complexity (Big-O), sorting, searching, recursion, and dynamic programming."},
    {"id": "apis", "name": "APIs", "category": "Software Engineering", "difficulty": "Intermediate", "estimated_hours": 25, "description": "RESTful API design, FastAPI/Flask, request handling, JSON schemas, and authentication."},
    {"id": "web_development", "name": "Web Development", "category": "Software Engineering", "difficulty": "Intermediate", "estimated_hours": 45, "description": "HTML5, CSS3, modern JavaScript, responsive interfaces, and full-stack integration."},
    {"id": "linux", "name": "Linux", "category": "Systems & Operations", "difficulty": "Foundational", "estimated_hours": 20, "description": "Shell scripting, file system permissions, process management, and SSH."},
    {"id": "networking", "name": "Networking", "category": "Systems & Operations", "difficulty": "Foundational", "estimated_hours": 30, "description": "TCP/IP model, DNS, HTTP/HTTPS protocols, subnets, routing, and sockets."},
    {"id": "security_fundamentals", "name": "Security Fundamentals", "category": "Security", "difficulty": "Intermediate", "estimated_hours": 35, "description": "CIA triad, threat modeling, cryptography basics, OWASP Top 10, and firewall rules."},
    {"id": "cloud_computing", "name": "Cloud Computing", "category": "Systems & Operations", "difficulty": "Intermediate", "estimated_hours": 35, "description": "Cloud architecture, AWS/GCP/Azure primitives, serverless, and managed databases."},
    {"id": "mlops", "name": "MLOps", "category": "AI & Data Science", "difficulty": "Advanced", "estimated_hours": 40, "description": "Model registry, CI/CD for ML, experiment tracking, Docker containerization, and monitoring."}
]

# (prerequisite)-[:PREREQUISITE_OF]->(advancedSkill)
DEMO_PREREQUISITES = [
    ("Python", "Machine Learning"),
    ("Python", "APIs"),
    ("Python", "Data Structures"),
    ("Statistics", "Machine Learning"),
    ("Statistics", "Data Analysis"),
    ("SQL", "Data Analysis"),
    ("Data Analysis", "Data Visualization"),
    ("Machine Learning", "Deep Learning"),
    ("Deep Learning", "Neural Networks"),
    ("Data Structures", "Algorithms"),
    ("Networking", "Security Fundamentals"),
    ("Linux", "Cloud Computing"),
    ("Linux", "Security Fundamentals"),
    ("Git", "Web Development"),
    ("APIs", "Web Development"),
    ("Machine Learning", "MLOps"),
    ("Cloud Computing", "MLOps")
]

DEMO_PROJECTS = [
    {
        "id": "churn_prediction",
        "name": "Customer Churn Prediction",
        "difficulty": "Intermediate",
        "estimated_hours": 25,
        "description": "Train classification models (Random Forest, XGBoost) to predict SaaS churn with feature importance and ROC evaluation.",
        "skills": ["Machine Learning", "Python", "Data Analysis"],
        "url": "https://github.com/topics/customer-churn-prediction"
    },
    {
        "id": "sales_dashboard",
        "name": "Sales Analytics Dashboard",
        "difficulty": "Beginner",
        "estimated_hours": 20,
        "description": "Interactive business intelligence dashboard tracking revenue, customer acquisition cost, and cohort retention metrics.",
        "skills": ["SQL", "Data Analysis", "Data Visualization"],
        "url": "https://github.com/topics/sales-dashboard"
    },
    {
        "id": "portfolio_website",
        "name": "Personal Portfolio Website",
        "difficulty": "Beginner",
        "estimated_hours": 18,
        "description": "Responsive personal developer site featuring project showcases, automated CI/CD deployment, and contact API endpoints.",
        "skills": ["Web Development", "Git", "APIs"],
        "url": "https://github.com/topics/portfolio-website"
    },
    {
        "id": "security_lab",
        "name": "Network Security Lab",
        "difficulty": "Advanced",
        "estimated_hours": 30,
        "description": "Simulated intrusion detection system with Wireshark packet capture, firewall rule hardening, and port scanning defense.",
        "skills": ["Networking", "Security Fundamentals", "Linux"],
        "url": "https://github.com/topics/security-lab"
    },
    {
        "id": "ai_resume_analyzer",
        "name": "AI Resume Analyzer",
        "difficulty": "Advanced",
        "estimated_hours": 35,
        "description": "Production NLP pipeline extracting entities, ranking candidate fit against job descriptions, and generating recommendations.",
        "skills": ["Neural Networks", "Deep Learning", "Python", "MLOps"],
        "url": "https://github.com/topics/resume-analyzer"
    },
    {
        "id": "movie_recommender",
        "name": "Movie Recommendation Engine",
        "difficulty": "Intermediate",
        "estimated_hours": 25,
        "description": "Hybrid collaborative and content-based filtering system using matrix factorization and cosine similarity on movie datasets.",
        "skills": ["Machine Learning", "Statistics", "Python"],
        "url": "https://github.com/topics/recommendation-engine"
    },
    {
        "id": "cloud_rest_api",
        "name": "Scalable Cloud REST API",
        "difficulty": "Intermediate",
        "estimated_hours": 25,
        "description": "Containerized FastAPI service connected to PostgreSQL, equipped with JWT auth, rate limiting, and automated unit tests.",
        "skills": ["APIs", "Cloud Computing", "SQL", "Data Structures"],
        "url": "https://github.com/topics/fastapi-crud"
    }
]

DEMO_RESOURCES = [
    {"skill": "Python", "name": "Complete Python Mastery & Data Structures", "type": "Interactive Course", "platform": "Python Official & freeCodeCamp", "duration_hours": 25, "url": "https://docs.python.org/3/tutorial/"},
    {"skill": "SQL", "name": "Mode Analytics SQL Tutorial for Data", "type": "Interactive Tutorial", "platform": "Mode Analytics", "duration_hours": 15, "url": "https://mode.com/sql-tutorial/"},
    {"skill": "Statistics", "name": "Statistical Inference and Probability", "type": "Course", "platform": "Khan Academy", "duration_hours": 20, "url": "https://www.khanacademy.org/math/statistics-probability"},
    {"skill": "Machine Learning", "name": "Machine Learning Specialization", "type": "Specialization", "platform": "DeepLearning.AI / Coursera", "duration_hours": 45, "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
    {"skill": "Deep Learning", "name": "Practical Deep Learning for Coders", "type": "Video Course & Labs", "platform": "fast.ai", "duration_hours": 40, "url": "https://course.fast.ai/"},
    {"skill": "Neural Networks", "name": "Neural Networks: Zero to Hero", "type": "Video Lectures & Code", "platform": "Andrej Karpathy", "duration_hours": 30, "url": "https://karpathy.ai/zero-to-hero.html"},
    {"skill": "Git", "name": "Pro Git Book & Interactive Branching", "type": "Interactive", "platform": "Open Source", "duration_hours": 8, "url": "https://learngitbranching.js.org/"},
    {"skill": "Data Structures", "name": "Algorithms and Data Structures Roadmap", "type": "Problem Set & Tutorials", "platform": "NeetCode", "duration_hours": 35, "url": "https://neetcode.io/roadmap"},
    {"skill": "Algorithms", "name": "Algorithms and Data Structures Roadmap", "type": "Problem Set & Tutorials", "platform": "NeetCode", "duration_hours": 35, "url": "https://neetcode.io/roadmap"},
    {"skill": "APIs", "name": "Building High-Performance APIs with FastAPI", "type": "Documentation & Labs", "platform": "FastAPI Documentation", "duration_hours": 12, "url": "https://fastapi.tiangolo.com/tutorial/"},
    {"skill": "Web Development", "name": "MDN Web Docs: Front-End to Full-Stack", "type": "Documentation & Curriculum", "platform": "Mozilla Developer Network", "duration_hours": 30, "url": "https://developer.mozilla.org/en-US/docs/Learn"},
    {"skill": "Linux", "name": "Linux Journey — Systems & Command Line", "type": "Interactive Guide", "platform": "Linux Journey", "duration_hours": 14, "url": "https://linuxjourney.com/"},
    {"skill": "Networking", "name": "Computer Networking Fundamentals", "type": "Video & Practice Labs", "platform": "NetworkChuck / freeCodeCamp", "duration_hours": 18, "url": "https://www.youtube.com/watch?v=IPvYjXCsTg8"},
    {"skill": "Security Fundamentals", "name": "Pre-Security & Cyber Fundamentals", "type": "Hands-On Labs", "platform": "TryHackMe", "duration_hours": 25, "url": "https://tryhackme.com/path/outline/presecurity"},
    {"skill": "Cloud Computing", "name": "Cloud Practitioner Essentials", "type": "Course", "platform": "AWS Skill Builder", "duration_hours": 15, "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/"},
    {"skill": "Data Visualization", "name": "Interactive Data Visualization with Plotly", "type": "Tutorial & Examples", "platform": "Plotly Official", "duration_hours": 12, "url": "https://plotly.com/python/"},
    {"skill": "Data Analysis", "name": "Exploratory Data Analysis Mastery", "type": "Course", "platform": "Kaggle Learn", "duration_hours": 15, "url": "https://www.kaggle.com/learn/data-cleaning"},
    {"skill": "MLOps", "name": "Full Stack LLM BootCamp & MLOps", "type": "Course & Labs", "platform": "Full Stack Deep Learning", "duration_hours": 25, "url": "https://fullstackdeeplearning.com/"}
]


# ==============================================================================
# NEO4J CLIENT & CONFIGURATION
# ==============================================================================

def get_credentials(secrets_dict: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Retrieve Neo4j credentials from Streamlit secrets or OS environment."""
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


class Neo4jClient:
    """Manages connection, session lifecycle, and parameterized queries for Neo4j."""

    def __init__(self, uri: Optional[str], username: Optional[str], password: Optional[str]):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver: Optional[Driver] = None
        self._connected = False
        self._connection_error = None

        if HAS_NEO4J_LIB and uri and username and password:
            try:
                self.driver = GraphDatabase.driver(uri, auth=(username, password))
                # Quick verification
                self.driver.verify_connectivity()
                self._connected = True
            except Exception as e:
                self._connected = False
                self._connection_error = str(e)
        else:
            if not HAS_NEO4J_LIB:
                self._connection_error = "Neo4j Python library not installed"
            else:
                self._connection_error = "Missing Neo4j credentials"

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def status_message(self) -> str:
        if self._connected:
            return f"Connected to Neo4j Aura ({self.uri})"
        return f"Demo Mode Active: {self._connection_error}"

    def close(self):
        if self.driver:
            try:
                self.driver.close()
            except Exception:
                pass

    def run_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Safely execute parameterized query with automatic session closing."""
        if not self._connected or not self.driver:
            raise RuntimeError("Neo4j driver is not connected.")

        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]


# ==============================================================================
# CAREER & SKILL DATA SERVICE (Hybrid Neo4j with Seamless Demo Mode)
# ==============================================================================

class SkillGraphService:
    """Unified service providing graph queries and topological career gap analysis."""

    def __init__(self, neo4j_client: Neo4jClient):
        self.client = neo4j_client
        self._skills_dict = {s["name"]: s for s in DEMO_SKILLS}

    @property
    def is_live_mode(self) -> bool:
        return self.client.is_connected

    def get_careers(self) -> List[Dict[str, Any]]:
        """Fetch all available target careers."""
        if self.client.is_connected:
            try:
                query = """
                MATCH (c:Career)
                RETURN c.id AS id, c.name AS name, c.description AS description,
                       c.category AS category, c.avg_salary_range AS avg_salary_range
                ORDER BY c.name
                """
                results = self.client.run_query(query)
                if results:
                    return results
            except Exception as e:
                print(f"[Warning] Neo4j fetch error, falling back to demo: {e}")

        # Demo fallback
        return [
            {
                "id": c["id"],
                "name": c["name"],
                "description": c["description"],
                "category": c["category"],
                "avg_salary_range": c["avg_salary_range"]
            }
            for c in DEMO_CAREERS
        ]

    def get_all_skills(self) -> List[Dict[str, Any]]:
        """Fetch all unique skills available in the graph."""
        if self.client.is_connected:
            try:
                query = """
                MATCH (s:Skill)
                RETURN s.id AS id, s.name AS name, s.category AS category,
                       s.difficulty AS difficulty, s.estimated_hours AS estimated_hours,
                       s.description AS description
                ORDER BY s.name
                """
                results = self.client.run_query(query)
                if results:
                    return results
            except Exception as e:
                print(f"[Warning] Neo4j fetch error, falling back to demo: {e}")

        return DEMO_SKILLS

    def get_career_required_skills(self, career_name: str) -> List[Dict[str, Any]]:
        """Fetch skills required by a specific career."""
        if self.client.is_connected:
            try:
                query = """
                MATCH (c:Career {name: $career_name})-[r:REQUIRES_SKILL]->(s:Skill)
                RETURN s.name AS name, s.category AS category, s.difficulty AS difficulty,
                       s.estimated_hours AS estimated_hours, s.description AS description,
                       r.importance AS importance
                ORDER BY s.name
                """
                results = self.client.run_query(query, {"career_name": career_name})
                if results:
                    return results
            except Exception as e:
                print(f"[Warning] Neo4j fetch error, falling back to demo: {e}")

        # Demo fallback
        for c in DEMO_CAREERS:
            if c["name"].lower() == career_name.lower():
                skills_out = []
                for sk in c["skills"]:
                    meta = self._skills_dict.get(sk["name"], {})
                    skills_out.append({
                        "name": sk["name"],
                        "importance": sk.get("importance", "Core"),
                        "category": meta.get("category", "General"),
                        "difficulty": meta.get("difficulty", "Intermediate"),
                        "estimated_hours": meta.get("estimated_hours", 30),
                        "description": meta.get("description", "")
                    })
                return skills_out
        return []

    def get_prerequisites(self) -> List[Tuple[str, str]]:
        """Fetch all (prerequisite, advancedSkill) pairs."""
        if self.client.is_connected:
            try:
                query = """
                MATCH (p:Skill)-[:PREREQUISITE_OF]->(a:Skill)
                RETURN p.name AS prerequisite, a.name AS advanced
                """
                results = self.client.run_query(query)
                if results:
                    return [(r["prerequisite"], r["advanced"]) for r in results]
            except Exception as e:
                print(f"[Warning] Neo4j fetch error, falling back to demo: {e}")

        return DEMO_PREREQUISITES

    def get_projects_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Fetch projects that develop the given skills."""
        if not skills:
            return []

        if self.client.is_connected:
            try:
                query = """
                MATCH (p:Project)-[:DEVELOPS_SKILL]->(s:Skill)
                WHERE s.name IN $skills
                RETURN p.id AS id, p.name AS name, p.difficulty AS difficulty,
                       p.estimated_hours AS estimated_hours, p.description AS description,
                       p.github_template AS url, collect(s.name) AS matched_skills
                ORDER BY size(matched_skills) DESC, p.name
                """
                results = self.client.run_query(query, {"skills": skills})
                if results:
                    return results
            except Exception as e:
                print(f"[Warning] Neo4j fetch error, falling back to demo: {e}")

        # Demo fallback
        skills_set = set(skills)
        matched_projects = []
        for p in DEMO_PROJECTS:
            overlap = [s for s in p["skills"] if s in skills_set]
            if overlap:
                matched_projects.append({
                    "id": p["id"],
                    "name": p["name"],
                    "difficulty": p["difficulty"],
                    "estimated_hours": p["estimated_hours"],
                    "description": p["description"],
                    "url": p["url"],
                    "matched_skills": overlap
                })

        # Sort by most matched missing skills first
        matched_projects.sort(key=lambda x: len(x["matched_skills"]), reverse=True)
        return matched_projects

    def get_resources_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Fetch learning resources for given skills."""
        if not skills:
            return []

        if self.client.is_connected:
            try:
                query = """
                MATCH (s:Skill)-[:TAUGHT_BY]->(r:Resource)
                WHERE s.name IN $skills
                RETURN r.id AS id, r.name AS name, r.url AS url, r.type AS type,
                       r.platform AS platform, r.duration_hours AS duration_hours,
                       s.name AS skill_name
                ORDER BY s.name, r.name
                """
                results = self.client.run_query(query, {"skills": skills})
                if results:
                    return results
            except Exception as e:
                print(f"[Warning] Neo4j fetch error, falling back to demo: {e}")

        # Demo fallback
        skills_set = set(skills)
        matched = [r for r in DEMO_RESOURCES if r["skill"] in skills_set]
        return [
            {
                "id": r["name"].lower().replace(" ", "_"),
                "name": r["name"],
                "url": r["url"],
                "type": r["type"],
                "platform": r["platform"],
                "duration_hours": r["duration_hours"],
                "skill_name": r["skill"]
            }
            for r in matched
        ]

    def get_subgraph_data(self, career_name: str, user_skills: List[str]) -> Dict[str, Any]:
        """Retrieve nodes and links for interactive graph visualization."""
        user_skills_set = set(user_skills)
        required_skills = self.get_career_required_skills(career_name)
        req_names = {s["name"] for s in required_skills}
        missing_names = req_names - user_skills_set
        prereqs = self.get_prerequisites()
        projects = self.get_projects_for_skills(list(req_names))
        resources = self.get_resources_for_skills(list(req_names))

        nodes = []
        links = []
        node_ids = set()

        def add_node(nid: str, label: str, ntype: str, status: str = "", extra: str = ""):
            if nid not in node_ids:
                node_ids.add(nid)
                nodes.append({
                    "id": nid,
                    "label": label,
                    "type": ntype,
                    "status": status,
                    "extra": extra
                })

        # Add Career Node
        career_node_id = f"career_{career_name}"
        add_node(career_node_id, career_name, "Career", "target", "Target Career")

        # Add Skill Nodes
        for s in required_skills:
            s_name = s["name"]
            sid = f"skill_{s_name}"
            status = "Mastered" if s_name in user_skills_set else "To Learn"
            add_node(sid, s_name, "Skill", status, f"{s.get('difficulty', '')} • {s.get('estimated_hours', 30)}h")
            links.append({
                "source": career_node_id,
                "target": sid,
                "label": "REQUIRES_SKILL",
                "type": "requires"
            })

        # Add Prerequisite links between skills in this career
        for p, a in prereqs:
            pid = f"skill_{p}"
            aid = f"skill_{a}"
            if pid in node_ids and aid in node_ids:
                links.append({
                    "source": pid,
                    "target": aid,
                    "label": "PREREQUISITE_OF",
                    "type": "prerequisite"
                })

        # Add Top Projects (up to 4 for visual cleanliness)
        for proj in projects[:4]:
            pid = f"project_{proj['id']}"
            add_node(pid, proj["name"], "Project", proj["difficulty"], f"{proj['estimated_hours']}h")
            for sk in proj.get("matched_skills", []):
                sid = f"skill_{sk}"
                if sid in node_ids:
                    links.append({
                        "source": pid,
                        "target": sid,
                        "label": "DEVELOPS_SKILL",
                        "type": "develops"
                    })

        # Add Top Resources (up to 5 for visual cleanliness)
        for res in resources[:5]:
            rid = f"resource_{res['skill_name']}_{res['name'][:10]}"
            add_node(rid, res["name"], "Resource", res["type"], f"{res['platform']} • {res['duration_hours']}h")
            sid = f"skill_{res['skill_name']}"
            if sid in node_ids:
                links.append({
                    "source": sid,
                    "target": rid,
                    "label": "TAUGHT_BY",
                    "type": "taught_by"
                })

        return {"nodes": nodes, "links": links}


# ==============================================================================
# GRAPH-BASED TOPOLOGICAL GAP ANALYSIS & ROADMAP ENGINE
# ==============================================================================

def analyze_career_gap(
    service: SkillGraphService,
    career_name: str,
    user_skills: List[str],
    weekly_hours: int = 15,
    education_level: str = "Bachelor's Degree",
    experience_level: str = "Entry Level (0-2 yrs)"
) -> Dict[str, Any]:
    """
    Computes graph-based skill gap, topological learning order with cycle safety,
    and prerequisite-aware milestone roadmap.
    """
    user_skills_set = set(user_skills)
    required_skills = service.get_career_required_skills(career_name)
    total_required = len(required_skills)

    if total_required == 0:
        return {
            "career": career_name,
            "coverage_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "learning_order": [],
            "roadmap_stages": [],
            "projects": [],
            "resources": [],
            "total_hours": 0,
            "estimated_weeks": 0
        }

    matched_skills = [s for s in required_skills if s["name"] in user_skills_set]
    missing_skills = [s for s in required_skills if s["name"] not in user_skills_set]
    coverage_percentage = round((len(matched_skills) / total_required) * 100, 1)

    missing_names = {s["name"] for s in missing_skills}
    missing_lookup = {s["name"]: s for s in missing_skills}

    # Prerequisite graph among missing skills
    prereqs = service.get_prerequisites()

    # Build adjacency & in-degree for missing skills
    # Note: If prerequisite is already mastered by user, it doesn't block!
    # A skill is blocked only by unmet prerequisites in missing_names.
    in_degree: Dict[str, int] = {name: 0 for name in missing_names}
    adj_list: Dict[str, List[str]] = defaultdict(list)
    unmet_prereq_map: Dict[str, List[str]] = defaultdict(list)

    for p, a in prereqs:
        if a in missing_names:
            if p in missing_names:
                adj_list[p].append(a)
                in_degree[a] += 1
                unmet_prereq_map[a].append(p)

    # Classify skills into "Ready to Learn" vs "Blocked by Prerequisites"
    ready_to_learn = [s for s in missing_skills if in_degree[s["name"]] == 0]
    blocked_skills = [
        {
            **s,
            "blocked_by": unmet_prereq_map[s["name"]]
        }
        for s in missing_skills if in_degree[s["name"]] > 0
    ]

    # Topological Sort (Kahn's Algorithm) with cycle prevention
    queue = deque([name for name in missing_names if in_degree[name] == 0])
    ordered_missing_names: List[str] = []
    seen = set()

    # Prioritize foundational difficulties within equal in-degree
    diff_priority = {"Foundational": 0, "Intermediate": 1, "Specialized": 2, "Advanced": 3}

    while queue:
        # Sort queue by skill difficulty priority
        sorted_q = sorted(list(queue), key=lambda x: diff_priority.get(missing_lookup[x].get("difficulty", "Intermediate"), 1))
        current = sorted_q[0]
        queue = deque(sorted_q[1:])

        ordered_missing_names.append(current)
        seen.add(current)

        for neighbor in adj_list[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If there was a cycle or disconnected elements, append remaining safely
    for name in missing_names:
        if name not in seen:
            ordered_missing_names.append(name)

    ordered_missing_skills = [missing_lookup[name] for name in ordered_missing_names]

    # Calculate hours and roadmap stages
    skills_hours = sum(s.get("estimated_hours", 30) for s in missing_skills)
    matched_projects = service.get_projects_for_skills(list(missing_names))
    matched_resources = service.get_resources_for_skills(list(missing_names))

    # Top recommended projects
    recommended_projects = matched_projects[:4]
    projects_hours = sum(p.get("estimated_hours", 25) for p in recommended_projects)
    total_hours = skills_hours + projects_hours

    # Weekly timeline
    weekly_hours = max(5, weekly_hours)
    estimated_weeks = round(total_hours / weekly_hours, 1)

    # Partition learning order into 4 Actionable Roadmap Stages
    # Stage 1: Foundations (Zero unmet prereqs & Foundational/Core)
    # Stage 2: Core Skills
    # Stage 3: Advanced Skills
    # Stage 4: Portfolio Projects
    stage1_skills = []
    stage2_skills = []
    stage3_skills = []

    for s in ordered_missing_skills:
        diff = s.get("difficulty", "Intermediate")
        if diff == "Foundational" or len(unmet_prereq_map.get(s["name"], [])) == 0:
            if diff in ["Foundational", "Intermediate"] and len(stage1_skills) < 3:
                stage1_skills.append(s)
            elif diff in ["Intermediate", "Core"]:
                stage2_skills.append(s)
            else:
                stage3_skills.append(s)
        elif diff in ["Advanced", "Specialized"]:
            stage3_skills.append(s)
        else:
            stage2_skills.append(s)

    # Balance stages if any is empty but skills exist
    if not stage1_skills and ordered_missing_skills:
        stage1_skills.append(ordered_missing_skills[0])
    if not stage2_skills and len(ordered_missing_skills) > 1:
        stage2_skills.append(ordered_missing_skills[min(1, len(ordered_missing_skills)-1)])

    roadmap_stages = [
        {
            "stage_num": 1,
            "title": "Stage 1: Foundations & Core Prerequisites",
            "description": "Establish essential syntax, computational thinking, and base primitives with zero blocker dependencies.",
            "skills": stage1_skills,
            "hours": sum(s.get("estimated_hours", 30) for s in stage1_skills)
        },
        {
            "stage_num": 2,
            "title": "Stage 2: Applied Core Competencies",
            "description": "Bridge foundational concepts into practical pipelines, libraries, and real-world architectures.",
            "skills": stage2_skills,
            "hours": sum(s.get("estimated_hours", 30) for s in stage2_skills)
        },
        {
            "stage_num": 3,
            "title": "Stage 3: Advanced Specialization & Tooling",
            "description": "Tackle high-impact domain specializations, neural/distributed systems, and industry-standard workflows.",
            "skills": stage3_skills,
            "hours": sum(s.get("estimated_hours", 30) for s in stage3_skills)
        },
        {
            "stage_num": 4,
            "title": "Stage 4: Portfolio Engineering & Real-World Projects",
            "description": "Synthesize acquired skills into end-to-end, production-ready capstones with verifiable code artifacts.",
            "projects": recommended_projects,
            "hours": projects_hours
        }
    ]

    return {
        "career": career_name,
        "total_required": total_required,
        "matched_count": len(matched_skills),
        "missing_count": len(missing_skills),
        "coverage_percentage": coverage_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ready_to_learn": ready_to_learn,
        "blocked_skills": blocked_skills,
        "learning_order": ordered_missing_skills,
        "roadmap_stages": roadmap_stages,
        "projects": recommended_projects,
        "resources": matched_resources,
        "total_hours": total_hours,
        "skills_hours": skills_hours,
        "projects_hours": projects_hours,
        "estimated_weeks": estimated_weeks,
        "weekly_hours": weekly_hours,
        "education_level": education_level,
        "experience_level": experience_level
    }
