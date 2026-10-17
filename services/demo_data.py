"""
SkillGraph AI — Canonical Graph Dataset for Demo Mode & Testing
Matches database/seed.cypher 1-to-1.
"""

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
