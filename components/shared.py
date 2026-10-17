"""
SkillGraph AI — Shared UI Components & Design System
Minimalist, high-performance career intelligence SaaS design system.
Inspired by Skill Graph reference: crisp black typography, white/light-gray cards,
restrained orange accents (#EA580C), purple/violet graph highlights (#8B5CF6),
and elegant serif headlines.
"""

import streamlit as st
from typing import Optional, List, Dict, Any


def get_global_css() -> str:
    """Returns the core design stylesheet matching the Skill Graph aesthetic."""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

        /* Global typography & light theme canvas */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #111827;
        }

        .stApp {
            background-color: #FAFAFA !important;
        }

        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 4rem !important;
            max-width: 1360px !important;
        }

        /* Serif Headlines */
        .serif-headline {
            font-family: 'Playfair Display', Georgia, serif !important;
            font-size: 2.75rem;
            font-weight: 800;
            line-height: 1.15;
            color: #111827;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }

        .serif-headline-italic {
            font-family: 'Playfair Display', Georgia, serif !important;
            font-style: italic;
            color: #EA580C;
            font-weight: 700;
        }

        /* Intelligence Pill Badge */
        .sg-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #F3F4F6;
            border: 1px solid #E5E7EB;
            color: #374151;
            padding: 4px 12px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .sg-badge-dot {
            width: 7px;
            height: 7px;
            background-color: #EA580C;
            border-radius: 1px;
            display: inline-block;
        }

        /* Minimalist SaaS Card */
        .sg-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }

        .sg-card:hover {
            border-color: #D1D5DB;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        }

        .sg-card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sg-card-subtitle {
            font-size: 0.88rem;
            color: #6B7280;
            line-height: 1.45;
            margin-bottom: 16px;
        }

        /* Metric Block */
        .metric-box {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #111827;
            line-height: 1.1;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
        }

        .metric-label {
            font-size: 0.78rem;
            font-weight: 600;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-sub {
            font-size: 0.8rem;
            color: #9CA3AF;
            margin-top: 4px;
        }

        /* Skill Status Badges */
        .skill-tag-mastered {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: #ECFDF5;
            color: #065F46;
            border: 1px solid #A7F3D0;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 3px;
        }

        .skill-tag-ready {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: #FFF7ED;
            color: #9A3412;
            border: 1px solid #FED7AA;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 3px;
        }

        .skill-tag-blocked {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: #F3F4F6;
            color: #4B5563;
            border: 1px solid #E5E7EB;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 3px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem !important;
        }

        .nav-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 14px;
            border-bottom: 1px solid #F3F4F6;
            margin-bottom: 14px;
        }

        .nav-logo-box {
            width: 34px;
            height: 34px;
            background: #111827;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1rem;
            position: relative;
        }

        .nav-logo-dot {
            width: 6px;
            height: 6px;
            background-color: #EA580C;
            border-radius: 50%;
            position: absolute;
            top: 7px;
            right: 7px;
        }

        .nav-brand-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #111827;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }

        .nav-brand-sub {
            font-size: 0.72rem;
            color: #6B7280;
            font-weight: 500;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        /* Streamlit Primary Button Override (Solid Black or Orange) */
        button[kind="primary"] {
            background-color: #111827 !important;
            border: 1px solid #111827 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.2rem !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.15s ease !important;
        }

        button[kind="primary"]:hover {
            background-color: #EA580C !important;
            border-color: #EA580C !important;
            box-shadow: 0 4px 12px rgba(234, 88, 12, 0.25) !important;
        }

        button[kind="secondary"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            color: #374151 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
        }

        button[kind="secondary"]:hover {
            border-color: #9CA3AF !important;
            color: #111827 !important;
            background-color: #F9FAFB !important;
        }

        /* Active Navigation Button Styling */
        .nav-active-btn button {
            background-color: #111827 !important;
            color: #FFFFFF !important;
            border-color: #111827 !important;
            font-weight: 700 !important;
        }

        /* Step Timeline */
        .roadmap-step {
            display: flex;
            gap: 16px;
            margin-bottom: 20px;
            position: relative;
        }

        .roadmap-step:not(:last-child)::after {
            content: '';
            position: absolute;
            top: 36px;
            left: 17px;
            bottom: -16px;
            width: 2px;
            background-color: #E5E7EB;
        }

        .step-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.88rem;
            flex-shrink: 0;
            z-index: 1;
        }

        .step-circle-completed {
            background-color: #059669;
            color: #FFFFFF;
        }

        .step-circle-active {
            background-color: #EA580C;
            color: #FFFFFF;
        }

        .step-circle-locked {
            background-color: #F3F4F6;
            color: #9CA3AF;
            border: 1px solid #E5E7EB;
        }
    </style>
    """


def render_page_header(title: str, subtitle: Optional[str] = None, badge: Optional[str] = None):
    """Renders a clean, elegant page header consistent with the Skill Graph aesthetic."""
    badge_html = f"""
    <div class="sg-badge">
        <span class="sg-badge-dot"></span>
        {badge}
    </div>
    """ if badge else ""

    sub_html = f"""
    <p style="font-size: 1.05rem; color: #4B5563; margin-top: 4px; margin-bottom: 22px; max-width: 820px; line-height: 1.5;">
        {subtitle}
    </p>
    """ if subtitle else ""

    st.markdown(f"""
    <div>
        {badge_html}
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 6px 0;">
            {title}
        </h1>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, subtext: Optional[str] = None, accent_color: str = "#111827"):
    """Renders a minimalist SaaS metric block."""
    sub_html = f'<div class="metric-sub">{subtext}</div>' if subtext else ""
    return f"""
    <div class="metric-box">
        <div class="metric-label">{title}</div>
        <div class="metric-value" style="color: {accent_color};">{value}</div>
        {sub_html}
    </div>
    """
