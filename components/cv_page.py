"""
SkillGraph AI — CV Parser & Skill Extraction Component
Extracts text from uploaded CVs (PDF, TXT, MD), scans for verified technical competencies,
allows interactive user confirmation/rejection, and persists confirmed skills to the user's Skill Graph.
"""

import io
import re
import streamlit as st
from typing import Dict, Any, List, Set
from services.auth_service import get_current_user
from services.user_graph_service import UserGraphService

# Comprehensive technology and engineering skill taxonomy
KNOWN_SKILLS = {
    "Python": ("Software Engineering", "Core programming language for software, automation, and AI"),
    "SQL": ("Databases", "Relational querying, schema design, and analytical queries"),
    "Docker": ("DevOps & Cloud", "Containerization and local reproducible environments"),
    "Kubernetes": ("DevOps & Cloud", "Container orchestration, cluster scaling, and deployment"),
    "Git": ("Software Engineering", "Distributed version control and branch workflows"),
    "Linux": ("Systems", "Unix command line, shell scripting, and server administration"),
    "React": ("Web Development", "Component-driven frontend UI library with hooks"),
    "TypeScript": ("Web Development", "Static typing for modern full-stack JavaScript applications"),
    "Next.js": ("Web Development", "Production React framework with SSR and server components"),
    "FastAPI": ("Software Engineering", "Modern, asynchronous high-performance Python web APIs"),
    "PostgreSQL": ("Databases", "Advanced relational database with ACID compliance"),
    "MongoDB": ("Databases", "Document-oriented NoSQL database for unstructured data"),
    "Redis": ("Databases", "In-memory key-value cache and pub/sub message broker"),
    "AWS": ("DevOps & Cloud", "Cloud infrastructure (EC2, S3, Lambda, IAM, VPC)"),
    "Machine Learning": ("Artificial Intelligence", "Supervised and unsupervised statistical modeling"),
    "Deep Learning": ("Artificial Intelligence", "Neural networks, backpropagation, and architectures"),
    "PyTorch": ("Artificial Intelligence", "Dynamic tensor library for deep learning research and deployment"),
    "TensorFlow": ("Artificial Intelligence", "Machine learning framework for training and inference"),
    "NLP": ("Artificial Intelligence", "Natural language processing, embeddings, and tokenization"),
    "Computer Vision": ("Artificial Intelligence", "Image classification, object detection, and CNNs"),
    "LLMs": ("Artificial Intelligence", "Large language models, prompt engineering, and fine-tuning"),
    "Data Structures": ("Computer Science", "Arrays, trees, graphs, heaps, and algorithmic efficiency"),
    "Algorithms": ("Computer Science", "Sorting, search, dynamic programming, and Big-O"),
    "CI/CD": ("DevOps & Cloud", "Automated build, test, and continuous delivery pipelines"),
    "GraphQL": ("Web Development", "Declarative API query language and schema runtime"),
    "C++": ("Systems", "High-performance systems programming and memory management"),
    "Rust": ("Systems", "Memory-safe systems programming without garbage collection"),
    "Statistics": ("Mathematics", "Probability distributions, hypothesis testing, and variance"),
    "Linear Algebra": ("Mathematics", "Matrix transformations, eigenvalues, and vector spaces"),
    "Spark": ("Data Engineering", "Distributed batch and stream data processing"),
    "Kafka": ("Data Engineering", "Distributed event streaming and real-time messaging")
}


def extract_text_from_file(uploaded_file) -> str:
    """Safely extracts text content from uploaded PDF or text file."""
    fname = uploaded_file.name.lower()

    if fname.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except Exception as e:
            st.error(f"Failed to parse PDF document: {str(e)}")
            return ""
    else:
        # Plain text / Markdown
        try:
            return uploaded_file.getvalue().decode("utf-8", errors="replace")
        except Exception as e:
            st.error(f"Failed to read text file: {str(e)}")
            return ""


def detect_skills_in_text(text: str) -> List[Dict[str, Any]]:
    """Matches text against verified engineering skill dictionary."""
    text_clean = text.lower()
    found = []

    for skill_name, (area, desc) in KNOWN_SKILLS.items():
        # Match using word boundaries
        pattern = r'\b' + re.escape(skill_name.lower()) + r'\b'
        matches = list(re.finditer(pattern, text_clean))
        if matches:
            count = len(matches)
            proficiency = "Advanced" if count >= 4 else ("Intermediate" if count >= 2 else "Beginner")
            found.append({
                "name": skill_name,
                "area": area,
                "description": desc,
                "mentions": count,
                "suggested_proficiency": proficiency
            })

    return sorted(found, key=lambda x: x["mentions"], reverse=True)


def render_cv_page(user_graph_service: UserGraphService):
    """Renders the functional CV parser and skill extractor page."""
    user = get_current_user()
    user_id = user.id if user else "guest_user"

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:#EFF6FF; border:1px solid #DBEAFE; color:#1E40AF; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700;">
            <span>📄</span> CV INTELLIGENCE & SKILL EXTRACTION
        </div>
        <h1 style="font-size: 2.1rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 6px 0 2px 0;">
            CV & Resume Parser
        </h1>
        <p style="font-size: 0.95rem; color: #4B5563; max-width: 820px; line-height: 1.5;">
            Upload your CV (PDF or plain text). Our parser identifies potential skills and lets you review, confirm, and import them directly into your personal Skill Graph.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_upload, c_preview = st.columns([1.2, 1], gap="medium")

    with c_upload:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
            <div style="font-weight:700; font-size:1rem; color:#111827; margin-bottom:4px;">Upload Document</div>
            <div style="font-size:0.82rem; color:#6B7280; margin-bottom:14px;">Supported formats: PDF, TXT, MD (Max size 10MB)</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_cv = st.file_uploader("Select CV / Resume file", type=["pdf", "txt", "md"], key="cv_file_uploader", label_visibility="collapsed")

        if uploaded_cv:
            # Validate size (< 10 MB)
            file_size_mb = uploaded_cv.size / (1024 * 1024)
            if file_size_mb > 10:
                st.error("Uploaded file exceeds 10MB limit. Please upload a smaller document.")
            else:
                with st.spinner("Extracting text and scanning competencies..."):
                    text_content = extract_text_from_file(uploaded_cv)

                if text_content:
                    st.session_state["cv_extracted_text"] = text_content
                    st.session_state["cv_detected_skills"] = detect_skills_in_text(text_content)
                    st.success(f"✓ Parsed document successfully ({len(text_content.split())} words extracted).")

    with c_preview:
        if st.session_state.get("cv_extracted_text"):
            text = st.session_state["cv_extracted_text"]
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:20px;">
                <div style="font-weight:700; font-size:1rem; color:#111827; margin-bottom:6px;">Document Summary</div>
                <div style="font-size:0.82rem; color:#4B5563; margin-bottom:10px;">
                    Word Count: <b>{}</b> • Detected Skills: <b>{}</b>
                </div>
            </div>
            """.format(len(text.split()), len(st.session_state.get("cv_detected_skills", []))), unsafe_allow_html=True)

            with st.expander("View Raw Extracted Text", expanded=False):
                st.text_area("Extracted Text", value=text[:2500] + ("..." if len(text) > 2500 else ""), height=220, disabled=True)
        else:
            st.markdown("""
            <div style="background:#F9FAFB; border:1px dashed #D1D5DB; border-radius:12px; padding:40px 20px; text-align:center; color:#6B7280; font-size:0.88rem;">
                Upload a CV on the left to see extracted text and detected skill signals.
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # DETECTED SKILLS REVIEW & IMPORT
    # -------------------------------------------------------------------------
    detected = st.session_state.get("cv_detected_skills", [])
    if detected:
        st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:24px 0;'/>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <div>
                <h3 style="font-size:1.3rem; font-weight:800; color:#111827; margin:0;">
                    Detected Skills ({len(detected)})
                </h3>
                <p style="font-size:0.85rem; color:#6B7280; margin:2px 0 0 0;">
                    Review skills found in your CV before adding them. Uncheck any skill you do not wish to import.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        existing_user_skills = {s["name"].lower(): s for s in user_graph_service.get_user_skills(user_id)}

        selected_to_import = []
        grid_cols = st.columns(3)

        for i, sk in enumerate(detected):
            col = grid_cols[i % 3]
            already_has = sk["name"].lower() in existing_user_skills

            with col:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:12px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; font-size:0.95rem; color:#111827;">{sk['name']}</span>
                        <span style="font-size:0.7rem; background:#F3F4F6; color:#4B5563; padding:2px 6px; border-radius:6px; font-weight:600;">{sk['mentions']} mentions</span>
                    </div>
                    <div style="font-size:0.75rem; color:#6B7280; margin:4px 0;">Domain: {sk['area']}</div>
                </div>
                """, unsafe_allow_html=True)

                if already_has:
                    st.caption("✓ Already in your graph")
                else:
                    chk = st.checkbox(f"Import {sk['name']}", value=True, key=f"chk_import_{sk['name']}")
                    if chk:
                        selected_to_import.append(sk)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        btn_c1, btn_c2 = st.columns([2, 4])
        with btn_c1:
            if st.button(f"📥 Import {len(selected_to_import)} Skills to Graph", type="primary", use_container_width=True):
                if not selected_to_import:
                    st.warning("No new skills selected for import.")
                else:
                    user_areas = {a["name"]: a["id"] for a in user_graph_service.get_user_areas(user_id)}
                    imported_count = 0

                    for item in selected_to_import:
                        area_name = item["area"]
                        # Auto-create area if missing
                        if area_name not in user_areas:
                            new_aid = user_graph_service.create_area(user_id, area_name)
                            user_areas[area_name] = new_aid

                        parent_area_id = user_areas[area_name]
                        user_graph_service.create_skill(
                            user_id,
                            name=item["name"],
                            area_id=parent_area_id,
                            proficiency=item["suggested_proficiency"],
                            status="Learning",
                            progress=40,
                            description=item["description"]
                        )
                        imported_count += 1

                    user_graph_service.add_notification(user_id, "CV Skills Imported", f"Imported {imported_count} skills into your knowledge graph.", "success")
                    st.success(f"✓ Successfully imported {imported_count} skills into your Skill Graph!")
                    st.session_state["cv_detected_skills"] = []
                    st.rerun()
