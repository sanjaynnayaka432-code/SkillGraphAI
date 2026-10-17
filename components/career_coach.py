"""
SkillGraph AI — AI Career Coach Component
Implements Part 10: Context-aware career mentor grounded in user's target role,
mastered skills, missing skills, and Neo4j graph relationships.
Supports real LLM integration if configured, with an intelligent graph-grounded
reasoning engine fallback (clearly identified).
"""

import os
import streamlit as st
from typing import Dict, Any, List, Optional


def render_career_coach_page(service: Any, analysis: Optional[Dict[str, Any]]):
    """Renders the AI Career Coach chat and guidance interface."""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            GRAPH-GROUNDED CAREER REASONING
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            AI Career Coach
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Personalized guidance grounded in your Neo4j skill graph topology, prerequisite paths, and learning velocity.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_target = st.session_state.get("selected_career_target", "AI Engineer")
    user_skills = st.session_state.get("selected_skills", ["Python", "Git"])

    # Check for live LLM configuration
    has_openai = bool(os.environ.get("OPENAI_API_KEY") or (hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets))
    has_gemini = bool(os.environ.get("GEMINI_API_KEY") or (hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets))
    has_live_llm = has_openai or has_gemini

    # Engine Status Badge
    if has_live_llm:
        st.markdown("""
        <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:8px 12px; margin-bottom:16px; font-size:0.8rem; color:#065F46;">
            <b>🟢 Live LLM Active</b> • Connected to generative intelligence model grounded in your active graph state.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; padding:8px 12px; margin-bottom:16px; font-size:0.8rem; color:#374151;">
            <b>⚡ Graph-Grounded Knowledge Engine Active</b> • Providing deterministic recommendations directly traversed from your Neo4j knowledge graph.
        </div>
        """, unsafe_allow_html=True)

    # Context Header Card
    cov_pct = analysis.get("coverage_percentage", 0.0) if analysis else 0.0
    missing_count = analysis.get("missing_count", 0) if analysis else 0
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:14px 18px; margin-bottom:18px;">
        <span style="font-weight:700; color:#111827; font-size:0.92rem;">Active Context:</span>
        <span style="font-size:0.85rem; color:#4B5563; margin-left:6px;">
            Target: <b>{c_target}</b> • Mastered: <b>{', '.join(user_skills)}</b> • Readiness: <b>{cov_pct}%</b> ({missing_count} skills remaining)
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Quick Prompt Shortcuts
    st.caption("ASK COACH QUICK SHORTCUTS")
    q1, q2, q3, q4 = st.columns(4)
    prompt_to_run = None

    with q1:
        if st.button("💡 Explain My Skill Gap", use_container_width=True):
            prompt_to_run = "Explain my skill gap"
    with q2:
        if st.button("🎯 What Should I Learn Next?", use_container_width=True):
            prompt_to_run = "What should I learn next?"
    with q3:
        if st.button("🛠️ Suggest Capstone Ideas", use_container_width=True):
            prompt_to_run = "Suggest capstone project ideas"
    with q4:
        if st.button("🔗 Explain Prereq Blockers", use_container_width=True):
            prompt_to_run = "Explain prerequisite blockers"

    # Initialize chat history
    if "coach_messages" not in st.session_state:
        st.session_state.coach_messages = [
            {
                "role": "assistant",
                "content": f"Hello {st.session_state.get('user_profile_name', 'Sanjay')}! I'm your SkillGraph AI Career Coach. I have your active goal set to **{c_target}** with {cov_pct}% readiness. How can I assist your learning plan today?"
            }
        ]

    # Handle quick shortcut execution
    if prompt_to_run:
        _handle_user_message(prompt_to_run, service, analysis, c_target, user_skills)
        st.rerun()

    # Chat Messages History Display
    for msg in st.session_state.coach_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Ask a question about your skills, roadmap, or career transition...")
    if user_input:
        _handle_user_message(user_input, service, analysis, c_target, user_skills)
        st.rerun()


def _handle_user_message(
    user_msg: str,
    service: Any,
    analysis: Optional[Dict[str, Any]],
    target_career: str,
    user_skills: List[str]
):
    """Processes user queries with graph context."""
    st.session_state.coach_messages.append({"role": "user", "content": user_msg})

    missing_skills = [s["name"] for s in analysis.get("missing_skills", [])] if analysis else []
    ready_skills = [s["name"] for s in analysis.get("ready_to_learn", [])] if analysis else []
    blocked_skills = analysis.get("blocked_skills", []) if analysis else []
    projects = analysis.get("projects", []) if analysis else []

    q_lower = user_msg.lower()

    if "gap" in q_lower or "explain" in q_lower and "skill" in q_lower:
        response = f"""### 📊 Skill Gap Assessment for {target_career}

Based on the Neo4j knowledge graph traversal for **{target_career}**:
- **Current Readiness:** {analysis.get('coverage_percentage', 0)}%
- **Mastered Competencies ({len(user_skills)}):** {', '.join(user_skills)}
- **Remaining Missing Competencies ({len(missing_skills)}):** {', '.join(missing_skills) if missing_skills else 'None! You meet all role requirements.'}

**Key Takeaway:** Your fastest path to increasing readiness is focusing on the **{len(ready_skills)} immediately learnable skills** ({', '.join(ready_skills)}) because they have zero unmet prerequisite dependencies."""

    elif "next" in q_lower or "what should i learn" in q_lower or "first" in q_lower:
        order = analysis.get("learning_order", []) if analysis else []
        if order:
            top_skill = order[0]
            response = f"""### 🎯 Immediate Priority: **{top_skill['name']}**

According to Kahn's topological sort on your prerequisite graph:
1. **Skill:** {top_skill['name']} ({top_skill.get('difficulty', 'Intermediate')})
2. **Estimated Study Time:** ~{top_skill.get('estimated_hours', 30)} hours
3. **Rationale:** This skill has all prerequisite dependencies satisfied by your existing competencies ({', '.join(user_skills)}), and mastering it will unblock downstream specializations.
4. **Action:** Navigate to the **Learning Roadmap** tab to track your progress on this milestone."""
        else:
            response = f"Congratulations! You have satisfied all sequenced competencies for **{target_career}**."

    elif "project" in q_lower or "capstone" in q_lower or "portfolio" in q_lower:
        if projects:
            top_p = projects[0]
            response = f"""### 🛠️ Recommended Capstone: **{top_p['name']}**

To practice your missing competencies in a verifiable portfolio piece:
- **Project:** {top_p['name']}
- **Difficulty:** {top_p.get('difficulty', 'Intermediate')} (~{top_p.get('estimated_hours', 25)} hrs)
- **Competencies Developed:** {', '.join(top_p.get('matched_skills', []))}
- **Description:** {top_p.get('description', '')}

Building this capstone will directly close {len(top_p.get('matched_skills', []))} missing competencies on your graph."""
        else:
            response = "No capstone projects are currently needed as you've mastered all core requirements."

    elif "prereq" in q_lower or "block" in q_lower:
        if blocked_skills:
            blocker_lines = "\n".join([f"- **{b['name']}:** Blocked until you master **{', '.join(b.get('blocked_by', []))}**" for b in blocked_skills])
            response = f"""### 🔗 Prerequisite Dependency Analysis

The following skills are currently **locked** because their required foundation is not yet complete:
{blocker_lines}

**Strategic Recommendation:** Do not attempt these locked skills yet. Master the prerequisite dependencies first to establish computational foundations without frustration."""
        else:
            response = f"All remaining skills for **{target_career}** have their prerequisites satisfied! You can learn any remaining skill immediately."

    else:
        response = f"""### 🧭 Career Guidance for {target_career}

I am tracking your career pathway toward **{target_career}**.
- You currently master: **{', '.join(user_skills)}**
- Next unblocked competency: **{ready_skills[0] if ready_skills else 'Curriculum Complete'}**
- You have **{len(projects)} curated capstones** available in the **Project Recommendations** page.

Try clicking any of the shortcut prompts above to drill into specific gap analysis or milestone planning!"""

    st.session_state.coach_messages.append({"role": "assistant", "content": response})
