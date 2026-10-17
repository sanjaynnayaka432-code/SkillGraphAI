// ==============================================================================
// SkillGraph AI — Seed Script (Idempotent using MERGE)
// Neo4j × hackFront India Graph Builder Build Sprint
//
// Node Types:
//   (:Career {id, name, description, category, avg_salary_range})
//   (:Skill {id, name, category, difficulty, estimated_hours, description})
//   (:Resource {id, name, url, type, platform, duration_hours})
//   (:Project {id, name, difficulty, estimated_hours, description, github_template})
//
// Relationships:
//   (:Career)-[:REQUIRES_SKILL {importance: 'Core'|'Specialized'|'Foundational'}]->(:Skill)
//   (:Skill)-[:PREREQUISITE_OF]->(:Skill)   // (prerequisite)-[:PREREQUISITE_OF]->(advanced)
//   (:Skill)-[:TAUGHT_BY]->(:Resource)
//   (:Project)-[:DEVELOPS_SKILL]->(:Skill)
// ==============================================================================

// Create Unique Constraints for Fast Lookups & Idempotency
CREATE CONSTRAINT career_id_unique IF NOT EXISTS FOR (c:Career) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT resource_id_unique IF NOT EXISTS FOR (r:Resource) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT project_id_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE;

// ------------------------------------------------------------------------------
// 1. CAREERS
// ------------------------------------------------------------------------------
MERGE (c1:Career {id: 'ai_engineer'})
SET c1.name = 'AI Engineer',
    c1.description = 'Designs, deploys, and scales machine learning and generative AI models into production environments.',
    c1.category = 'Artificial Intelligence',
    c1.avg_salary_range = '$130k - $190k';

MERGE (c2:Career {id: 'data_scientist'})
SET c2.name = 'Data Scientist',
    c2.description = 'Extracts actionable business insights using statistical inference, machine learning, and predictive modeling.',
    c2.category = 'Data Science',
    c2.avg_salary_range = '$115k - $165k';

MERGE (c3:Career {id: 'software_developer'})
SET c3.name = 'Software Developer',
    c3.description = 'Builds robust, high-performance web applications, services, APIs, and scalable distributed backend systems.',
    c3.category = 'Software Engineering',
    c3.avg_salary_range = '$105k - $155k';

MERGE (c4:Career {id: 'cybersecurity_analyst'})
SET c4.name = 'Cybersecurity Analyst',
    c4.description = 'Protects networks, endpoints, systems, and cloud infrastructure from threats, vulnerabilities, and intrusions.',
    c4.category = 'Security',
    c4.avg_salary_range = '$95k - $145k';

MERGE (c5:Career {id: 'data_analyst'})
SET c5.name = 'Data Analyst',
    c5.description = 'Transforms raw telemetry and databases into interactive dashboards, reports, and data-driven narratives.',
    c5.category = 'Analytics',
    c5.avg_salary_range = '$75k - $115k';

// ------------------------------------------------------------------------------
// 2. SKILLS
// ------------------------------------------------------------------------------
MERGE (s1:Skill {id: 'python'})
SET s1.name = 'Python',
    s1.category = 'Programming',
    s1.difficulty = 'Foundational',
    s1.estimated_hours = 40,
    s1.description = 'Core programming language for software, automation, data science, and AI pipelines.';

MERGE (s2:Skill {id: 'sql'})
SET s2.name = 'SQL',
    s2.category = 'Databases',
    s2.difficulty = 'Foundational',
    s2.estimated_hours = 30,
    s2.description = 'Relational querying language for filtering, aggregation, joins, and data manipulation.';

MERGE (s3:Skill {id: 'statistics'})
SET s3.name = 'Statistics',
    s3.category = 'Mathematics',
    s3.difficulty = 'Foundational',
    s3.estimated_hours = 35,
    s3.description = 'Probability distributions, hypothesis testing, regression analysis, and variance.';

MERGE (s4:Skill {id: 'data_analysis'})
SET s4.name = 'Data Analysis',
    s4.category = 'Analytics',
    s4.difficulty = 'Intermediate',
    s4.estimated_hours = 35,
    s4.description = 'Exploratory data analysis, cohort analysis, metric tracking, and anomaly detection.';

MERGE (s5:Skill {id: 'data_visualization'})
SET s5.name = 'Data Visualization',
    s5.category = 'Analytics',
    s5.difficulty = 'Intermediate',
    s5.estimated_hours = 25,
    s5.description = 'Designing visual charts and executive dashboards using Plotly, Seaborn, Tableau, or PowerBI.';

MERGE (s6:Skill {id: 'machine_learning'})
SET s6.name = 'Machine Learning',
    s6.category = 'AI & Data Science',
    s6.difficulty = 'Intermediate',
    s6.estimated_hours = 50,
    s6.description = 'Supervised and unsupervised learning, decision trees, gradient boosting, and evaluation metrics.';

MERGE (s7:Skill {id: 'deep_learning'})
SET s7.name = 'Deep Learning',
    s7.category = 'AI & Data Science',
    s7.difficulty = 'Advanced',
    s7.estimated_hours = 60,
    s7.description = 'Multi-layer neural architectures, backpropagation, PyTorch/TensorFlow, and GPU training.';

MERGE (s8:Skill {id: 'neural_networks'})
SET s8.name = 'Neural Networks',
    s8.category = 'AI & Data Science',
    s8.difficulty = 'Advanced',
    s8.estimated_hours = 45,
    s8.description = 'Convolutional (CNNs), Recurrent (RNNs), Transformers, and attention mechanisms.';

MERGE (s9:Skill {id: 'git'})
SET s9.name = 'Git',
    s9.category = 'Development Tools',
    s9.difficulty = 'Foundational',
    s9.estimated_hours = 15,
    s9.description = 'Version control, branch management, merge conflict resolution, and collaborative PRs.';

MERGE (s10:Skill {id: 'data_structures'})
SET s10.name = 'Data Structures',
    s10.category = 'Computer Science',
    s10.difficulty = 'Foundational',
    s10.estimated_hours = 40,
    s10.description = 'Arrays, linked lists, hash tables, stacks, queues, trees, and graphs.';

MERGE (s11:Skill {id: 'algorithms'})
SET s11.name = 'Algorithms',
    s11.category = 'Computer Science',
    s11.difficulty = 'Intermediate',
    s11.estimated_hours = 45,
    s11.description = 'Time/space complexity (Big-O), sorting, searching, recursion, and dynamic programming.';

MERGE (s12:Skill {id: 'apis'})
SET s12.name = 'APIs',
    s12.category = 'Software Engineering',
    s12.difficulty = 'Intermediate',
    s12.estimated_hours = 25,
    s12.description = 'RESTful API design, FastAPI/Flask, request handling, JSON schemas, and authentication.';

MERGE (s13:Skill {id: 'web_development'})
SET s13.name = 'Web Development',
    s13.category = 'Software Engineering',
    s13.difficulty = 'Intermediate',
    s13.estimated_hours = 45,
    s13.description = 'HTML5, CSS3, modern JavaScript, responsive interfaces, and full-stack integration.';

MERGE (s14:Skill {id: 'linux'})
SET s14.name = 'Linux',
    s14.category = 'Systems & Operations',
    s14.difficulty = 'Foundational',
    s14.estimated_hours = 20,
    s14.description = 'Shell scripting, file system permissions, process management, and SSH.';

MERGE (s15:Skill {id: 'networking'})
SET s15.name = 'Networking',
    s15.category = 'Systems & Operations',
    s15.difficulty = 'Foundational',
    s15.estimated_hours = 30,
    s15.description = 'TCP/IP model, DNS, HTTP/HTTPS protocols, subnets, routing, and sockets.';

MERGE (s16:Skill {id: 'security_fundamentals'})
SET s16.name = 'Security Fundamentals',
    s16.category = 'Security',
    s16.difficulty = 'Intermediate',
    s16.estimated_hours = 35,
    s16.description = 'CIA triad, threat modeling, cryptography basics, OWASP Top 10, and firewall rules.';

MERGE (s17:Skill {id: 'cloud_computing'})
SET s17.name = 'Cloud Computing',
    s17.category = 'Systems & Operations',
    s17.difficulty = 'Intermediate',
    s17.estimated_hours = 35,
    s17.description = 'Cloud architecture, AWS/GCP/Azure primitives, serverless, and managed databases.';

MERGE (s18:Skill {id: 'mlops'})
SET s18.name = 'MLOps',
    s18.category = 'AI & Data Science',
    s18.difficulty = 'Advanced',
    s18.estimated_hours = 40,
    s18.description = 'Model registry, CI/CD for ML, experiment tracking, Docker containerization, and monitoring.';

// ------------------------------------------------------------------------------
// 3. PREREQUISITES: (prerequisite)-[:PREREQUISITE_OF]->(advancedSkill)
// ------------------------------------------------------------------------------
// Python prerequisites
MERGE (p:Skill {id: 'python'})
MERGE (ml:Skill {id: 'machine_learning'})
MERGE (p)-[:PREREQUISITE_OF]->(ml);

MERGE (p:Skill {id: 'python'})
MERGE (api:Skill {id: 'apis'})
MERGE (p)-[:PREREQUISITE_OF]->(api);

MERGE (p:Skill {id: 'python'})
MERGE (ds:Skill {id: 'data_structures'})
MERGE (p)-[:PREREQUISITE_OF]->(ds);

// Statistics prerequisites
MERGE (stat:Skill {id: 'statistics'})
MERGE (ml:Skill {id: 'machine_learning'})
MERGE (stat)-[:PREREQUISITE_OF]->(ml);

MERGE (stat:Skill {id: 'statistics'})
MERGE (da:Skill {id: 'data_analysis'})
MERGE (stat)-[:PREREQUISITE_OF]->(da);

// SQL prerequisites
MERGE (sql:Skill {id: 'sql'})
MERGE (da:Skill {id: 'data_analysis'})
MERGE (sql)-[:PREREQUISITE_OF]->(da);

// Data Analysis prerequisites
MERGE (da:Skill {id: 'data_analysis'})
MERGE (dv:Skill {id: 'data_visualization'})
MERGE (da)-[:PREREQUISITE_OF]->(dv);

// Machine Learning -> Deep Learning
MERGE (ml:Skill {id: 'machine_learning'})
MERGE (dl:Skill {id: 'deep_learning'})
MERGE (ml)-[:PREREQUISITE_OF]->(dl);

// Deep Learning -> Neural Networks
MERGE (dl:Skill {id: 'deep_learning'})
MERGE (nn:Skill {id: 'neural_networks'})
MERGE (dl)-[:PREREQUISITE_OF]->(nn);

// Data Structures -> Algorithms
MERGE (ds:Skill {id: 'data_structures'})
MERGE (algo:Skill {id: 'algorithms'})
MERGE (ds)-[:PREREQUISITE_OF]->(algo);

// Networking -> Security Fundamentals
MERGE (net:Skill {id: 'networking'})
MERGE (sec:Skill {id: 'security_fundamentals'})
MERGE (net)-[:PREREQUISITE_OF]->(sec);

// Linux -> Cloud Computing
MERGE (lin:Skill {id: 'linux'})
MERGE (cloud:Skill {id: 'cloud_computing'})
MERGE (lin)-[:PREREQUISITE_OF]->(cloud);

// Linux -> Security Fundamentals
MERGE (lin:Skill {id: 'linux'})
MERGE (sec:Skill {id: 'security_fundamentals'})
MERGE (lin)-[:PREREQUISITE_OF]->(sec);

// Git -> Web Development
MERGE (git:Skill {id: 'git'})
MERGE (web:Skill {id: 'web_development'})
MERGE (git)-[:PREREQUISITE_OF]->(web);

// APIs -> Web Development
MERGE (api:Skill {id: 'apis'})
MERGE (web:Skill {id: 'web_development'})
MERGE (api)-[:PREREQUISITE_OF]->(web);

// Machine Learning + Cloud -> MLOps
MERGE (ml:Skill {id: 'machine_learning'})
MERGE (mlops:Skill {id: 'mlops'})
MERGE (ml)-[:PREREQUISITE_OF]->(mlops);

MERGE (cloud:Skill {id: 'cloud_computing'})
MERGE (mlops:Skill {id: 'mlops'})
MERGE (cloud)-[:PREREQUISITE_OF]->(mlops);

// ------------------------------------------------------------------------------
// 4. CAREER REQUIREMENTS: (Career)-[:REQUIRES_SKILL]->(Skill)
// ------------------------------------------------------------------------------

// AI Engineer
MERGE (c:Career {id: 'ai_engineer'})
MERGE (s1:Skill {id: 'python'})
MERGE (s2:Skill {id: 'machine_learning'})
MERGE (s3:Skill {id: 'deep_learning'})
MERGE (s4:Skill {id: 'neural_networks'})
MERGE (s5:Skill {id: 'statistics'})
MERGE (s6:Skill {id: 'apis'})
MERGE (s7:Skill {id: 'git'})
MERGE (s8:Skill {id: 'cloud_computing'})
MERGE (s9:Skill {id: 'mlops'})
MERGE (c)-[r1:REQUIRES_SKILL]->(s1) SET r1.importance = 'Core'
MERGE (c)-[r2:REQUIRES_SKILL]->(s2) SET r2.importance = 'Core'
MERGE (c)-[r3:REQUIRES_SKILL]->(s3) SET r3.importance = 'Core'
MERGE (c)-[r4:REQUIRES_SKILL]->(s4) SET r4.importance = 'Specialized'
MERGE (c)-[r5:REQUIRES_SKILL]->(s5) SET r5.importance = 'Foundational'
MERGE (c)-[r6:REQUIRES_SKILL]->(s6) SET r6.importance = 'Foundational'
MERGE (c)-[r7:REQUIRES_SKILL]->(s7) SET r7.importance = 'Foundational'
MERGE (c)-[r8:REQUIRES_SKILL]->(s8) SET r8.importance = 'Intermediate'
MERGE (c)-[r9:REQUIRES_SKILL]->(s9) SET r9.importance = 'Specialized';

// Data Scientist
MERGE (c:Career {id: 'data_scientist'})
MERGE (s1:Skill {id: 'python'})
MERGE (s2:Skill {id: 'sql'})
MERGE (s3:Skill {id: 'statistics'})
MERGE (s4:Skill {id: 'data_analysis'})
MERGE (s5:Skill {id: 'machine_learning'})
MERGE (s6:Skill {id: 'data_visualization'})
MERGE (s7:Skill {id: 'deep_learning'})
MERGE (s8:Skill {id: 'git'})
MERGE (c)-[r1:REQUIRES_SKILL]->(s1) SET r1.importance = 'Core'
MERGE (c)-[r2:REQUIRES_SKILL]->(s2) SET r2.importance = 'Core'
MERGE (c)-[r3:REQUIRES_SKILL]->(s3) SET r3.importance = 'Core'
MERGE (c)-[r4:REQUIRES_SKILL]->(s4) SET r4.importance = 'Core'
MERGE (c)-[r5:REQUIRES_SKILL]->(s5) SET r5.importance = 'Core'
MERGE (c)-[r6:REQUIRES_SKILL]->(s6) SET r6.importance = 'Intermediate'
MERGE (c)-[r7:REQUIRES_SKILL]->(s7) SET r7.importance = 'Specialized'
MERGE (c)-[r8:REQUIRES_SKILL]->(s8) SET r8.importance = 'Foundational';

// Software Developer
MERGE (c:Career {id: 'software_developer'})
MERGE (s1:Skill {id: 'python'})
MERGE (s2:Skill {id: 'data_structures'})
MERGE (s3:Skill {id: 'algorithms'})
MERGE (s4:Skill {id: 'git'})
MERGE (s5:Skill {id: 'apis'})
MERGE (s6:Skill {id: 'web_development'})
MERGE (s7:Skill {id: 'sql'})
MERGE (s8:Skill {id: 'linux'})
MERGE (s9:Skill {id: 'cloud_computing'})
MERGE (c)-[r1:REQUIRES_SKILL]->(s1) SET r1.importance = 'Core'
MERGE (c)-[r2:REQUIRES_SKILL]->(s2) SET r2.importance = 'Core'
MERGE (c)-[r3:REQUIRES_SKILL]->(s3) SET r3.importance = 'Core'
MERGE (c)-[r4:REQUIRES_SKILL]->(s4) SET r4.importance = 'Core'
MERGE (c)-[r5:REQUIRES_SKILL]->(s5) SET r5.importance = 'Core'
MERGE (c)-[r6:REQUIRES_SKILL]->(s6) SET r6.importance = 'Core'
MERGE (c)-[r7:REQUIRES_SKILL]->(s7) SET r7.importance = 'Intermediate'
MERGE (c)-[r8:REQUIRES_SKILL]->(s8) SET r8.importance = 'Intermediate'
MERGE (c)-[r9:REQUIRES_SKILL]->(s9) SET r9.importance = 'Specialized';

// Cybersecurity Analyst
MERGE (c:Career {id: 'cybersecurity_analyst'})
MERGE (s1:Skill {id: 'networking'})
MERGE (s2:Skill {id: 'security_fundamentals'})
MERGE (s3:Skill {id: 'linux'})
MERGE (s4:Skill {id: 'python'})
MERGE (s5:Skill {id: 'cloud_computing'})
MERGE (s6:Skill {id: 'git'})
MERGE (s7:Skill {id: 'sql'})
MERGE (c)-[r1:REQUIRES_SKILL]->(s1) SET r1.importance = 'Core'
MERGE (c)-[r2:REQUIRES_SKILL]->(s2) SET r2.importance = 'Core'
MERGE (c)-[r3:REQUIRES_SKILL]->(s3) SET r3.importance = 'Core'
MERGE (c)-[r4:REQUIRES_SKILL]->(s4) SET r4.importance = 'Core'
MERGE (c)-[r5:REQUIRES_SKILL]->(s5) SET r5.importance = 'Specialized'
MERGE (c)-[r6:REQUIRES_SKILL]->(s6) SET r6.importance = 'Foundational'
MERGE (c)-[r7:REQUIRES_SKILL]->(s7) SET r7.importance = 'Foundational';

// Data Analyst
MERGE (c:Career {id: 'data_analyst'})
MERGE (s1:Skill {id: 'sql'})
MERGE (s2:Skill {id: 'data_analysis'})
MERGE (s3:Skill {id: 'data_visualization'})
MERGE (s4:Skill {id: 'statistics'})
MERGE (s5:Skill {id: 'python'})
MERGE (s6:Skill {id: 'git'})
MERGE (c)-[r1:REQUIRES_SKILL]->(s1) SET r1.importance = 'Core'
MERGE (c)-[r2:REQUIRES_SKILL]->(s2) SET r2.importance = 'Core'
MERGE (c)-[r3:REQUIRES_SKILL]->(s3) SET r3.importance = 'Core'
MERGE (c)-[r4:REQUIRES_SKILL]->(s4) SET r4.importance = 'Core'
MERGE (c)-[r5:REQUIRES_SKILL]->(s5) SET r5.importance = 'Intermediate'
MERGE (c)-[r6:REQUIRES_SKILL]->(s6) SET r6.importance = 'Foundational';

// ------------------------------------------------------------------------------
// 5. PROJECTS & (Project)-[:DEVELOPS_SKILL]->(Skill)
// ------------------------------------------------------------------------------
MERGE (p1:Project {id: 'churn_prediction'})
SET p1.name = 'Customer Churn Prediction',
    p1.difficulty = 'Intermediate',
    p1.estimated_hours = 25,
    p1.description = 'Train classification algorithms (Random Forest, XGBoost) to predict SaaS churn with feature importance and ROC analysis.',
    p1.github_template = 'https://github.com/topics/customer-churn-prediction';

MERGE (p2:Project {id: 'sales_dashboard'})
SET p2.name = 'Sales Analytics Dashboard',
    p2.difficulty = 'Beginner',
    p2.estimated_hours = 20,
    p2.description = 'Interactive business intelligence dashboard tracking revenue, customer acquisition cost, and cohort retention metrics.',
    p2.github_template = 'https://github.com/topics/sales-dashboard';

MERGE (p3:Project {id: 'portfolio_website'})
SET p3.name = 'Personal Portfolio Website',
    p3.difficulty = 'Beginner',
    p3.estimated_hours = 18,
    p3.description = 'Responsive personal developer site featuring project showcases, automated CI/CD deployment, and contact API endpoints.',
    p3.github_template = 'https://github.com/topics/portfolio-website';

MERGE (p4:Project {id: 'security_lab'})
SET p4.name = 'Network Security Lab',
    p4.difficulty = 'Advanced',
    p4.estimated_hours = 30,
    p4.description = 'Simulated intrusion detection system with Wireshark packet capture, firewall rule hardening, and port scanning defense.',
    p4.github_template = 'https://github.com/topics/security-lab';

MERGE (p5:Project {id: 'ai_resume_analyzer'})
SET p5.name = 'AI Resume Analyzer',
    p5.difficulty = 'Advanced',
    p5.estimated_hours = 35,
    p5.description = 'Production NLP pipeline extracting entities, ranking candidate fit against job descriptions, and generating recommendations.',
    p5.github_template = 'https://github.com/topics/resume-analyzer';

MERGE (p6:Project {id: 'movie_recommender'})
SET p6.name = 'Movie Recommendation Engine',
    p6.difficulty = 'Intermediate',
    p6.estimated_hours = 25,
    p6.description = 'Hybrid collaborative and content-based filtering system using matrix factorization and cosine similarity on movie datasets.',
    p6.github_template = 'https://github.com/topics/recommendation-engine';

MERGE (p7:Project {id: 'cloud_rest_api'})
SET p7.name = 'Scalable Cloud REST API',
    p7.difficulty = 'Intermediate',
    p7.estimated_hours = 25,
    p7.description = 'Containerized FastAPI service connected to PostgreSQL, equipped with JWT auth, rate limiting, and automated unit tests.',
    p7.github_template = 'https://github.com/topics/fastapi-crud';

// Connect Projects to Skills
MERGE (p:Project {id: 'churn_prediction'})
MERGE (s1:Skill {id: 'machine_learning'})
MERGE (s2:Skill {id: 'python'})
MERGE (s3:Skill {id: 'data_analysis'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3);

MERGE (p:Project {id: 'sales_dashboard'})
MERGE (s1:Skill {id: 'sql'})
MERGE (s2:Skill {id: 'data_analysis'})
MERGE (s3:Skill {id: 'data_visualization'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3);

MERGE (p:Project {id: 'portfolio_website'})
MERGE (s1:Skill {id: 'web_development'})
MERGE (s2:Skill {id: 'git'})
MERGE (s3:Skill {id: 'apis'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3);

MERGE (p:Project {id: 'security_lab'})
MERGE (s1:Skill {id: 'networking'})
MERGE (s2:Skill {id: 'security_fundamentals'})
MERGE (s3:Skill {id: 'linux'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3);

MERGE (p:Project {id: 'ai_resume_analyzer'})
MERGE (s1:Skill {id: 'neural_networks'})
MERGE (s2:Skill {id: 'deep_learning'})
MERGE (s3:Skill {id: 'python'})
MERGE (s4:Skill {id: 'mlops'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3)
MERGE (p)-[:DEVELOPS_SKILL]->(s4);

MERGE (p:Project {id: 'movie_recommender'})
MERGE (s1:Skill {id: 'machine_learning'})
MERGE (s2:Skill {id: 'statistics'})
MERGE (s3:Skill {id: 'python'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3);

MERGE (p:Project {id: 'cloud_rest_api'})
MERGE (s1:Skill {id: 'apis'})
MERGE (s2:Skill {id: 'cloud_computing'})
MERGE (s3:Skill {id: 'sql'})
MERGE (s4:Skill {id: 'data_structures'})
MERGE (p)-[:DEVELOPS_SKILL]->(s1)
MERGE (p)-[:DEVELOPS_SKILL]->(s2)
MERGE (p)-[:DEVELOPS_SKILL]->(s3)
MERGE (p)-[:DEVELOPS_SKILL]->(s4);

// ------------------------------------------------------------------------------
// 6. RESOURCES & (Skill)-[:TAUGHT_BY]->(Resource)
// ------------------------------------------------------------------------------
MERGE (r1:Resource {id: 'res_python_bootcamp'})
SET r1.name = 'Complete Python Mastery & Data Structures',
    r1.url = 'https://docs.python.org/3/tutorial/',
    r1.type = 'Interactive Course',
    r1.platform = 'Python Official & freeCodeCamp',
    r1.duration_hours = 25;

MERGE (r2:Resource {id: 'res_sql_mode'})
SET r2.name = 'Mode Analytics SQL Tutorial for Data',
    r2.url = 'https://mode.com/sql-tutorial/',
    r2.type = 'Interactive Tutorial',
    r2.platform = 'Mode Analytics',
    r2.duration_hours = 15;

MERGE (r3:Resource {id: 'res_stat_khan'})
SET r3.name = 'Statistical Inference and Probability',
    r3.url = 'https://www.khanacademy.org/math/statistics-probability',
    r3.type = 'Course',
    r3.platform = 'Khan Academy',
    r3.duration_hours = 20;

MERGE (r4:Resource {id: 'res_ml_andrew'})
SET r4.name = 'Machine Learning Specialization',
    r4.url = 'https://www.coursera.org/specializations/machine-learning-introduction',
    r4.type = 'Specialization',
    r4.platform = 'DeepLearning.AI / Coursera',
    r4.duration_hours = 45;

MERGE (r5:Resource {id: 'res_dl_fastai'})
SET r5.name = 'Practical Deep Learning for Coders',
    r5.url = 'https://course.fast.ai/',
    r5.type = 'Video Course & Labs',
    r5.platform = 'fast.ai',
    r5.duration_hours = 40;

MERGE (r6:Resource {id: 'res_nn_karpathy'})
SET r6.name = 'Neural Networks: Zero to Hero',
    r6.url = 'https://karpathy.ai/zero-to-hero.html',
    r6.type = 'Video Lectures & Code',
    r6.platform = 'Andrej Karpathy',
    r6.duration_hours = 30;

MERGE (r7:Resource {id: 'res_git_pro'})
SET r7.name = 'Pro Git Book & Interactive Branching',
    r7.url = 'https://learngitbranching.js.org/',
    r7.type = 'Interactive',
    r7.platform = 'Open Source',
    r7.duration_hours = 8;

MERGE (r8:Resource {id: 'res_dsa_neetcode'})
SET r8.name = 'Algorithms and Data Structures Roadmap',
    r8.url = 'https://neetcode.io/roadmap',
    r8.type = 'Problem Set & Tutorials',
    r8.platform = 'NeetCode',
    r8.duration_hours = 35;

MERGE (r9:Resource {id: 'res_fastapi_doc'})
SET r9.name = 'Building High-Performance APIs with FastAPI',
    r9.url = 'https://fastapi.tiangolo.com/tutorial/',
    r9.type = 'Documentation & Labs',
    r9.platform = 'FastAPI Documentation',
    r9.duration_hours = 12;

MERGE (r10:Resource {id: 'res_web_mdn'})
SET r10.name = 'MDN Web Docs: Front-End to Full-Stack',
    r10.url = 'https://developer.mozilla.org/en-US/docs/Learn',
    r10.type = 'Documentation & Curriculum',
    r10.platform = 'Mozilla Developer Network',
    r10.duration_hours = 30;

MERGE (r11:Resource {id: 'res_linux_journey'})
SET r11.name = 'Linux Journey — Systems & Command Line',
    r11.url = 'https://linuxjourney.com/',
    r11.type = 'Interactive Guide',
    r11.platform = 'Linux Journey',
    r11.duration_hours = 14;

MERGE (r12:Resource {id: 'res_cs50_net'})
SET r12.name = 'Computer Networking Fundamentals',
    r12.url = 'https://www.youtube.com/watch?v=IPvYjXCsTg8',
    r12.type = 'Video & Practice Labs',
    r12.platform = 'NetworkChuck / freeCodeCamp',
    r12.duration_hours = 18;

MERGE (r13:Resource {id: 'res_tryhackme'})
SET r13.name = 'Pre-Security & Cyber Fundamentals',
    r13.url = 'https://tryhackme.com/path/outline/presecurity',
    r13.type = 'Hands-On Labs',
    r13.platform = 'TryHackMe',
    r13.duration_hours = 25;

MERGE (r14:Resource {id: 'res_cloud_aws'})
SET r14.name = 'Cloud Practitioner Essentials',
    r14.url = 'https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/',
    r14.type = 'Course',
    r14.platform = 'AWS Skill Builder',
    r14.duration_hours = 15;

MERGE (r15:Resource {id: 'res_plotly_guide'})
SET r15.name = 'Interactive Data Visualization with Plotly',
    r15.url = 'https://plotly.com/python/',
    r15.type = 'Tutorial & Examples',
    r15.platform = 'Plotly Official',
    r15.duration_hours = 12;

MERGE (r16:Resource {id: 'res_fullstack_deeplearning'})
SET r16.name = 'Full Stack LLM BootCamp & MLOps',
    r16.url = 'https://fullstackdeeplearning.com/',
    r16.type = 'Course & Labs',
    r16.platform = 'Full Stack Deep Learning',
    r16.duration_hours = 25;

MERGE (r17:Resource {id: 'res_da_kaggle'})
SET r17.name = 'Exploratory Data Analysis Mastery',
    r17.url = 'https://www.kaggle.com/learn/data-cleaning',
    r17.type = 'Course',
    r17.platform = 'Kaggle Learn',
    r17.duration_hours = 15;

// Link Skills to Resources
MERGE (s:Skill {id: 'python'}) MERGE (r:Resource {id: 'res_python_bootcamp'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'sql'}) MERGE (r:Resource {id: 'res_sql_mode'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'statistics'}) MERGE (r:Resource {id: 'res_stat_khan'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'machine_learning'}) MERGE (r:Resource {id: 'res_ml_andrew'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'deep_learning'}) MERGE (r:Resource {id: 'res_dl_fastai'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'neural_networks'}) MERGE (r:Resource {id: 'res_nn_karpathy'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'git'}) MERGE (r:Resource {id: 'res_git_pro'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'data_structures'}) MERGE (r:Resource {id: 'res_dsa_neetcode'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'algorithms'}) MERGE (r:Resource {id: 'res_dsa_neetcode'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'apis'}) MERGE (r:Resource {id: 'res_fastapi_doc'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'web_development'}) MERGE (r:Resource {id: 'res_web_mdn'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'linux'}) MERGE (r:Resource {id: 'res_linux_journey'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'networking'}) MERGE (r:Resource {id: 'res_cs50_net'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'security_fundamentals'}) MERGE (r:Resource {id: 'res_tryhackme'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'cloud_computing'}) MERGE (r:Resource {id: 'res_cloud_aws'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'data_visualization'}) MERGE (r:Resource {id: 'res_plotly_guide'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'data_analysis'}) MERGE (r:Resource {id: 'res_da_kaggle'}) MERGE (s)-[:TAUGHT_BY]->(r);
MERGE (s:Skill {id: 'mlops'}) MERGE (r:Resource {id: 'res_fullstack_deeplearning'}) MERGE (s)-[:TAUGHT_BY]->(r);
