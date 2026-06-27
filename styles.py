"""Shared CSS and professional rounded UI layout components for OvaSight."""
import streamlit as st

def inject_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Sarabun:wght@400;500;600;700&display=swap');

    html, body, [class*=\"css\"] {
        font-family: 'Plus Jakarta Sans', 'Sarabun', sans-serif;
    }
    
    /* ขยายพื้นที่หน้าจอเต็มใบแบบไม่มี Sidebar */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        background-color: #f8fafc;
    }
    
    /* ซ่อนแถบเมนู Sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    :root {
        --green-primary:  #0d9488;    
        --green-dark:     #115e59;
        --green-gradient: linear-gradient(135deg, #0f766e 0%, #042f2e 100%);
        --gray-border:    #e2e8f0;    
        --text-dark:      #0f172a;    
        --text-muted:     #64748b;    
    }

    /* Top Navigation Bar สไตล์มินิมอลโมเดิร์น */
    .top-nav {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--gray-border);
        padding: 18px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .nav-logo {
        font-size: 22px;
        font-weight: 700;
        color: var(--green-primary);
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: -0.5px;
    }
    .nav-links {
        display: flex;
        gap: 28px;
    }

    /* Hero Massive Banner แบบพรีเมียม */
    .hero-wrap {
        background: var(--green-gradient);
        color: #ffffff;
        padding: 64px 48px;
        text-align: left;
        position: relative;
        border-radius: 28px;
        margin: 32px 40px;
        box-shadow: 0 20px 40px -15px rgba(13, 148, 136, 0.25);
    }
    .hero-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 700;
        line-height: 1.25;
        margin-bottom: 16px;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 15px;
        color: #ccfbf1;
        max-width: 850px;
        line-height: 1.7;
        margin-bottom: 32px;
        opacity: 0.9;
    }
    .hero-stats {
        display: flex;
        gap: 48px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 24px;
    }
    .hero-stat-num {
        font-size: 28px;
        font-weight: 700;
        color: #2dd4bf;
    }
    .hero-stat-lbl {
        font-size: 12px;
        color: #99f6e4;
        margin-top: 2px;
    }

    /* Content Wrapper */
    .content-body {
        padding: 0 40px 40px 40px;
    }

    /* Section Header */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-dark);
        border-left: 6px solid var(--green-primary);
        padding-left: 14px;
        margin-bottom: 24px;
        letter-spacing: -0.3px;
    }

    /* Card Navigation ดีไซน์โค้งและเงาละมุนระดับ High-End */
    .menu-card {
        background: white;
        border: 1px solid var(--gray-border);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .menu-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 35px -10px rgba(13, 148, 136, 0.12);
        border-color: #5eead4;
    }
    .feat-icon {
        font-size: 26px;
        margin-bottom: 16px;
        background: #f0fdfa;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
    }
    .feat-title {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 8px;
    }
    .feat-desc {
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.6;
        margin-bottom: 20px;
        height: 45px;
    }

    /* Clinical Boxes */
    .custom-box {
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 18px;
        font-size: 14px;
        line-height: 1.6;
    }
    .box-info { background: #f0fdfa; border: 1px solid #b2f5ea; color: #115e59; }
    .box-warn { background: #fffbeb; border: 1px solid #fde68a; color: #78350f; }
    
    /* Metrics Layer */
    .m-card {
        background: #ffffff;
        border: 1px solid var(--gray-border);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01);
        transition: all 0.3s ease;
    }
    .m-card:hover {
        border-color: #cbd5e1;
    }
    .m-lbl { font-size: 13px; color: var(--text-muted); font-weight: 500; }
    .m-val { font-size: 26px; font-weight: 700; color: var(--text-dark); margin-top: 6px; }

    /* ปรับแต่งปุ่ม Streamlit เป็น Pill Shape */
    div.stButton > button {
        border-radius: 100px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: var(--green-primary) !important;
        color: var(--green-primary) !important;
        background-color: #f0fdfa !important;
        transform: scale(1.01);
    }
    
    /* ปรับแต่ง Uploader */
    [data-testid="stFileUploader"] > section {
        border-radius: 20px !important;
        border: 2px dashed #99f6e4 !important;
        background-color: #ffffff !important;
        padding: 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def navbar(active_page: str = "home"):
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-logo">🔬 OvaSight</div>
        <div class="nav-links">
            <span style="font-size:14px; font-weight:600; color:{'var(--green-primary)' if active_page=='home' else 'var(--text-muted)'}">หน้าหลัก</span>
            <span style="font-size:14px; font-weight:600; color:{'var(--green-primary)' if active_page=='ai' else 'var(--text-muted)'}">AI Detection Workspace</span>
            <span style="font-size:14px; font-weight:600; color:{'var(--green-primary)' if active_page=='knowledge' else 'var(--text-muted)'}">Clinical Knowledge</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div style="padding: 40px; text-align: center; font-size: 13px; color: #94a3b8; border-top: 1px solid #e2e8f0; margin-top: 56px; background: white; letter-spacing: 0.5px;">
        OvaSight © 2026 • Smartphone-Based Pinworm Egg Analysis and Diagnosis Platform
    </div>
    """, unsafe_allow_html=True)