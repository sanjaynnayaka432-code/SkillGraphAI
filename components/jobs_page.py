"""
SkillGraph AI — Jobs Intelligence Page
Curated benchmark roles and custom job analyzer with real-time graph skill comparison,
gap analysis, match percentage calculation, and direct saving to the user's Applications tracker.
"""

import streamlit as st
from typing import Dict, Any, List
from services.auth_service import get_current_user
from services.user_graph_service import UserGraphService


BENCHMARK_JOBS = [
    {
        "id": "job_ai_eng_1",
        "title": "AI Systems Engineer",
        "company": "ScaleAI Labs",
        "location": "Remote",
        "salary": "$140,000 - $195,000",
        "required_skills": ["Python", "PyTorch", "Docker", "Machine Learning", "FastAPI"],
        "description": "Architect high-performance distributed inference systems and finetuning pipelines for frontier LLM models."
    },
    {
        "id": "job_fullstack_2",
        "title": "Senior Full-Stack Engineer",
        "company": "Vercel Ecosystems",
        "location": "San Francisco, CA (Hybrid)",
        "salary": "$135,000 - $180,000",
        "required_skills": ["React", "TypeScript", "Next.js", "PostgreSQL", "Git"],
        "description": "Build high-throughput developer experience platforms with Next.js App Router, serverless edge functions, and Postgres."
    },
    {
        "id": "job_ds_3",
        "title": "Staff Data Scientist",
        "company": "Databricks Solutions",
        "location": "Remote",
        "salary": "$150,000 - $210,000",
        "required_skills": ["Python", "SQL", "Statistics", "Machine Learning", "Spark"],
        "description": "Develop predictive revenue forecasting, customer churn algorithms, and causal inference experiments at massive scale."
    },
    {
        "id": "job_devops_4",
        "title": "Cloud Infrastructure & Platform Engineer",
        "company": "Cloudflare Network",
        "location": "New York, NY",
        "salary": "$130,000 - $175,000",
        "required_skills": ["Kubernetes", "Docker", "AWS", "Linux", "CI/CD"],
        "description": "Design resilient multi-cloud edge infrastructure, automated Helm deployments, and zero-trust security postures."
    },
    {
        "id": "job_swe_5",
        "title": "Backend Systems Software Developer",
        "company": "Stripe Payments",
        "location": "Remote",
        "salary": "$145,000 - $200,000",
        "required_skills": ["Python", "SQL", "Git", "Data Structures", "Redis"],
        "description": "Build fault-tolerant ledger services, transactional idempotent APIs, and low-latency distributed event streaming."
    }
]


def render_jobs_page(user_graph_service: UserGraphService):
    """Renders the Jobs Explorer with personalized graph matching."""
    user = get_current_user()
    user_id = user.id if user else "guest_user"

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:#F5F3FF; border:1px solid #DDD6FE; color:#5B21B6; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700;">
            <span>💼</span> CAREER OPPORTUNITIES & GAP MATCHING
        </div>
        <h1 style="font-size: 2.1rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 6px 0 2px 0;">
            Jobs & Skill Alignment
        </h1>
        <p style="font-size: 0.95rem; color: #4B5563; max-width: 820px; line-height: 1.5;">
            Compare industry roles directly against your live Skill Graph. Discover matched strengths, uncover missing prerequisite gaps, and save opportunities to your application pipeline.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # User's mastered skills lookup
    user_skills = user_graph_service.get_user_skills(user_id)
    mastered_skills = {s["name"].lower() for s in user_skills if s.get("status") == "Mastered"}
    all_user_skills = {s["name"].lower() for s in user_skills}

    # Search & Filter Row
    f_col1, f_col2, f_col3 = st.columns([2.5, 1.8, 1.2])
    with f_col1:
        keyword = st.text_input("Search Roles or Companies", placeholder="e.g. AI Engineer, Python, Vercel...", key="job_kw_search")
    with f_col2:
        loc_filter = st.selectbox("Location", ["All Locations", "Remote", "San Francisco, CA", "New York, NY"], key="job_loc_filter")
    with f_col3:
        st.write("")
        st.write("")
        if st.button("➕ Add Custom Role", key="btn_trigger_custom_job", use_container_width=True):
            st.session_state.show_add_custom_job = not st.session_state.get("show_add_custom_job", False)

    # Custom Job Entry Form
    if st.session_state.get("show_add_custom_job"):
        with st.expander("📝 Analyze a Custom Job Specification", expanded=True):
            st.markdown("Enter details for a role you found to compare against your skill graph.")
            with st.form("custom_job_form"):
                cj_title = st.text_input("Role Title", placeholder="e.g. AI Research Engineer").strip()
                cj_comp = st.text_input("Company", placeholder="e.g. Mistral AI").strip()
                cj_loc = st.text_input("Location", placeholder="e.g. Paris / Remote").strip()
                cj_skills_raw = st.text_input("Required Skills (Comma separated)", placeholder="Python, PyTorch, Docker, Git").strip()
                cj_desc = st.text_area("Job Description", placeholder="Role responsibilities and expectations...").strip()
                if st.form_submit_button("Analyze & Save to Applications"):
                    if cj_title and cj_comp:
                        user_graph_service.create_application(
                            user_id,
                            company=cj_comp,
                            role=cj_title,
                            location=cj_loc or "Remote",
                            status="Interested",
                            notes=f"Required skills: {cj_skills_raw}\n{cj_desc}"
                        )
                        st.success(f"✓ Saved '{cj_title}' at {cj_comp} directly into your Applications tracker!")
                        st.session_state.show_add_custom_job = False
                        st.rerun()

    # Filter benchmark jobs
    filtered_jobs = []
    for j in BENCHMARK_JOBS:
        if loc_filter != "All Locations" and loc_filter not in j["location"]:
            continue
        if keyword:
            kw = keyword.lower()
            text_haystack = f"{j['title']} {j['company']} {' '.join(j['required_skills'])}".lower()
            if kw not in text_haystack:
                continue
        filtered_jobs.append(j)

    st.markdown(f"**Showing {len(filtered_jobs)} Available Roles**")

    # Render Job Cards with Real-Time Skill Match Calculator
    for job in filtered_jobs:
        reqs = job["required_skills"]
        total_req = len(reqs)

        matched = [s for s in reqs if s.lower() in mastered_skills]
        learning = [s for s in reqs if s.lower() in all_user_skills and s.lower() not in mastered_skills]
        gaps = [s for s in reqs if s.lower() not in all_user_skills]

        # Calculate score (Mastered = 100%, Learning = 50%)
        score = int(((len(matched) * 1.0 + len(learning) * 0.5) / total_req) * 100) if total_req > 0 else 0

        score_badge = "background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0;" if score >= 70 else ("background:#FFF7ED; color:#C2410C; border:1px solid #FED7AA;" if score >= 40 else "background:#FEF2F2; color:#991B1B; border:1px solid #FECACA;")

        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:22px; margin-bottom:18px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="font-size:1.3rem; font-weight:800; color:#111827;">{job['title']}</div>
                    <div style="font-size:0.9rem; color:#4B5563; font-weight:600; margin-top:2px;">
                        🏢 {job['company']} • 📍 {job['location']} • 💰 {job['salary']}
                    </div>
                </div>
                <div style="{score_badge} padding:4px 12px; border-radius:14px; font-weight:800; font-size:0.92rem; text-align:center;">
                    {score}% Match
                </div>
            </div>
            <div style="font-size:0.88rem; color:#4B5563; margin:10px 0 14px 0; line-height:1.5;">
                {job['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Match Breakdown Badges
        b_col1, b_col2 = st.columns([4, 1.2])
        with b_col1:
            st.markdown("**Skill Requirements Alignment:**")
            badges_html = []
            for s in reqs:
                if s.lower() in mastered_skills:
                    badges_html.append(f"<span style='background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700; margin-right:6px;'>✓ {s}</span>")
                elif s.lower() in all_user_skills:
                    badges_html.append(f"<span style='background:#F5F3FF; color:#5B21B6; border:1px solid #DDD6FE; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700; margin-right:6px;'>⚡ {s} (Learning)</span>")
                else:
                    badges_html.append(f"<span style='background:#FEF2F2; color:#991B1B; border:1px solid #FECACA; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700; margin-right:6px;'>⚠️ {s} (Missing Gap)</span>")
            st.markdown("".join(badges_html), unsafe_allow_html=True)

        with b_col2:
            st.write("")
            if st.button("💾 Save to Applications", key=f"btn_save_job_{job['id']}", use_container_width=True, type="primary"):
                user_graph_service.create_application(
                    user_id,
                    company=job["company"],
                    role=job["title"],
                    location=job["location"],
                    status="Interested",
                    notes=f"Benchmark salary: {job['salary']}\nRequired skills: {', '.join(job['required_skills'])}"
                )
                user_graph_service.add_notification(user_id, "Job Saved", f"Added '{job['title']}' at {job['company']} to applications.", "info")
                st.success(f"✓ Saved '{job['title']}' to your Applications tracker!")
                st.rerun()

        st.markdown("<hr style='border:none; border-top:1px solid #F1F5F9; margin:16px 0;'/>", unsafe_allow_html=True)
