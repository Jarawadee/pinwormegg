import streamlit as st
import pandas as pd
import plotly.express as px
from styles import inject_css, navbar, footer

st.set_page_config(
    page_title="OvaSight — แพลตฟอร์มวินิจฉัยไข่พยาธิเข็มหมุด",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

# CSS เพิ่มเติมสำหรับการ์ดที่กดได้ทั้งใบ
st.markdown("""
<style>
/* ซ่อนปุ่ม Streamlit ปกติ แล้วทำให้ครอบคลุมการ์ดทั้งหมด */
div[data-testid="column"] .card-btn-wrapper {
    position: relative;
}
div[data-testid="column"] .card-btn-wrapper div.stButton {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 10;
}
div[data-testid="column"] .card-btn-wrapper div.stButton > button {
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
    border-radius: 24px !important;
    padding: 0 !important;
}
/* การ์ดที่ hover จะมี effect */
div[data-testid="column"] .card-btn-wrapper:hover .menu-card {
    transform: translateY(-6px);
    box-shadow: 0 25px 35px -10px rgba(13, 148, 136, 0.18) !important;
    border-color: #5eead4 !important;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

navbar("home")

# ── 1. HERO MASSIVE BANNER ──────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-pill">🔬 สมาร์ทโฟนแพลตฟอร์ม AI</div>
  <div class="hero-title">OvaSight: แพลตฟอร์มวิเคราะห์และตรวจวินิจฉัย<br>ไข่พยาธิเข็มหมุดบนสมาร์ทโฟน</div>
  <div class="hero-sub">
    A Smart Smartphone-Based Platform for Pinworm Egg Analysis and Diagnosis ระบบผู้เชี่ยวชาญสนับสนุนการคัดกรองเชื้อ Enterobius vermicularis 
    ผ่านการถ่ายภาพด้วยเทคนิค Scotch Tape Technique ร่วมกับเลนส์กล้องจุลทรรศน์สมาร์ทโฟน
  </div>
  <div class="hero-stats">
    <div><div class="hero-stat-num">99%</div><div class="hero-stat-lbl">AI Model Accuracy</div></div>
    <div><div class="hero-stat-num">MobileNet-V3</div><div class="hero-stat-lbl">Deep Learning Backbone</div></div>
    <div><div class="hero-stat-num">&lt; 1.5s</div><div class="hero-stat-lbl">Inference Response Time</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 2. CONTENT SPACE ────────────────────────────────────────────────────
st.markdown('<div class="content-body">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧭 เข้าใช้งานโมดูลระบบงาน (Module Navigation)</div>', unsafe_allow_html=True)

col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    # wrapper div ที่ทำให้ปุ่มซ้อนทับการ์ดได้
    st.markdown("""
    <div class="card-btn-wrapper" style="position:relative; min-height:200px;">
      <div class="menu-card" style="transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
        <div class="feat-icon">📷</div>
        <div class="feat-title">1. AI Object Detection Workspace</div>
        <div class="feat-desc">อัปโหลดภาพสไลด์แผ่นใสเพื่อวิเคราะห์ ตรวจนับจำนวน และตีกรอบพิกัดไข่พยาธิเข็มหมุดโดยอัตโนมัติ</div>
        <div style="margin-top:20px; font-size:13px; font-weight:600; color:var(--green-primary);">เปิดโมดูล AI Detection →</div>
      </div>
    """, unsafe_allow_html=True)
    
    if st.button("AI Detection", key="btn_go_ai", use_container_width=True):
        st.switch_page("pages/1_AI_Detection.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_nav2:
    st.markdown("""
    <div class="card-btn-wrapper" style="position:relative; min-height:200px;">
      <div class="menu-card" style="transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
        <div class="feat-icon">📚</div>
        <div class="feat-title">2. Clinical Knowledge Base</div>
        <div class="feat-desc">คลังข้อมูลสารานุกรมทางการแพทย์ พยาธิวิทยา ลักษณะสัณฐานวิทยา (Morphology) และวงจรชีวิตพยาธิ</div>
        <div style="margin-top:20px; font-size:13px; font-weight:600; color:var(--green-primary);">เข้าสู่คลังความรู้ ค้นหาข้อมูล →</div>
      </div>
    """, unsafe_allow_html=True)
    
    if st.button("Knowledge Base", key="btn_go_know", use_container_width=True):
        st.switch_page("pages/2_Knowledge.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ส่วนแสดงข้อมูลสถิติภาพรวม
st.markdown('<div style="margin-top: 48px;" class="section-title">📊 สถิติเชิงระบาดวิทยาคลินิก (Demo Epidemiological Insights)</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="m-card"><div class="m-lbl">จำนวนการสแกนสะสม</div><div class="m-val">1,482 ครั้ง</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="m-card"><div class="m-lbl">ตรวจพบติดเชื้อ (Positive)</div><div class="m-val" style="color:#e11d48;">412 เคส (27.8%)</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="m-card"><div class="m-lbl">ความไวของระบบ (Sensitivity)</div><div class="m-val">96.5%</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="m-card"><div class="m-lbl">กลุ่มเสี่ยงสูงสุดปัจจุบัน</div><div class="m-val" style="color:#d97706;">เด็กปฐมวัย (4-7 ปี)</div></div>', unsafe_allow_html=True)

st.write("")
df_insight = pd.DataFrame({
    'กลุ่มอายุ': ['3-5 ปี', '6-8 ปี', '9-12 ปี', '13 ปีขึ้นไป'],
    'เคสตรวจพบเชื้อ (Positive)': [180, 154, 62, 16]
})

left_g, right_g = st.columns([1.2, 0.8])
with left_g:
    fig_bar = px.bar(
        df_insight, x='กลุ่มอายุ', y='เคสตรวจพบเชื้อ (Positive)',
        color_discrete_sequence=['#0d9488'],
        title="สถิติการตรวจพบจำแนกตามกลุ่มอายุของผู้ป่วย"
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=0, l=0, r=0),
        font=dict(family="Sarabun, sans-serif")
    )
    fig_bar.update_yaxes(gridcolor='#f1f5f9')
    st.plotly_chart(fig_bar, use_container_width=True)

with right_g:
    st.markdown("""
    <div class="custom-box box-info">
        <b>💡 คำแนะนำประกอบสถิติสาธารณสุข:</b><br>
        สถิติการใช้งานแสดงให้เห็นอย่างเด่นชัดว่า อัตราความชุกของโรคพยาธิเข็มหมุดจะหนาแน่นที่สุดในเด็กเล็กช่วงก่อนวัยเรียนและวัยประถมศึกษาตอนต้น แพลตฟอร์ม OvaSight บนสมาร์ทโฟนช่วยให้คัดกรองเชิงรุกได้อย่างรวดเร็ว
    </div>
    <div class="custom-box box-warn">
        <b>⚠️ ประกาศเตือนเชิงคลินิก:</b><br>
        ข้อมูลและสถิติทั้งหมดบนหน้าหลักนี้เป็นส่วนโมเดลจำลองข้อมูลเชิงระบาดวิทยาเพื่อทดสอบโครงสร้าง UI แพลตฟอร์มเท่านั้น
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
footer()