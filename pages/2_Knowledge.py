import streamlit as st
import pandas as pd
from styles import inject_css, navbar, footer

st.set_page_config(
    page_title="OvaSight — คลังความรู้",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
navbar("knowledge")

st.markdown('<div class="content-body">', unsafe_allow_html=True)

if st.button("⬅️ กลับหน้าหลัก (Home)", key="back_home_know"):
    st.switch_page("app.py")

st.markdown('<div class="section-title" style="margin-top:15px;">📚 ข้อมูลสารานุกรมทางการแพทย์และพยาธิวิทยาคลินิก</div>', unsafe_allow_html=True)

st.markdown("#### 🔍 ค้นหาและเปรียบเทียบข้อมูลสัณฐานวิทยาปรสิต (Parasite Morphology Comparison)")

df_parasite = pd.DataFrame({
    'ชื่อทางวิทยาศาสตร์': ['Enterobius vermicularis', 'Ascaris lumbricoides', 'Trichuris trichiura', 'Hookworm'],
    'ชื่อสามัญ': ['พยาธิเข็มหมุด (Pinworm)', 'พยาธิไส้เดือน', 'พยาธิแส้ม้า', 'พยาธิปากขอ'],
    'ลักษณะสัณฐานวิทยาภายใต้กล้องจุลทรรศน์': [
        'เปลือกหนาใส เรียบลื่น ด้านหนึ่งนูน อีกด้านหนึ่งแบนราบชัดเจนคล้ายรูปตัวอักษร D (D-shaped asymmetry)',
        'ทรงกลมหรือรี เปลือกหนาหลายชั้น ผิวด้านนอกขรุขระเป็นลอนคลื่นย้อมติดสีน้ำตาลน้ำดี',
        'รูปทรงคล้ายถังเบียร์หรือลูกขนุน มีจุกใสโปร่งแสง (Polar plugs) โผล่เด่นชัดทั้งสองหัวท้าย',
        'รูปไข่รี เปลือกบางใสเฉียบ ด้านในช่องว่างมักเห็นตัวอ่อนแบ่งตัวเป็นกลุ่มก้อนเซลล์ (Cleavage สเตจ)'
    ]
})

# ปรับปรุงความสวยงามของตารางผ่าน st.dataframe คอนฟิกแบบพรีเมียม
st.dataframe(
    df_parasite, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "ชื่อทางวิทยาศาสตร์": st.column_config.TextColumn("ชื่อทางวิทยาศาสตร์ (Scientific Name)", width="medium"),
        "ชื่อสามัญ": st.column_config.TextColumn("ชื่อสามัญ (Common Name)", width="medium"),
        "ลักษณะสัณฐานวิทยาภายใต้กล้องจุลทรรศน์": st.column_config.TextColumn("ลักษณะทางสัณฐานวิทยา (Morphology Characteristic)"),
    }
)

st.markdown("""
<div class="custom-box box-info" style="margin-top:28px;">
    <b>💡 อาการและพยาธิสภาพที่สำคัญของโรคพยาธิเข็มหมุด (Enterobiasis):</b><br>
    ผู้ป่วยส่วนใหญ่มักมีอาการคันบริเวณรอบทวารหนัก (Pruritus ani) อย่างรุนแรง โดยเฉพาะในเวลากลางคืนเนื่องจากพยาธิตัวเต็มวัยเพศเมียจะคลานออกมาวางไข่บริเวณผิวหนังรอบทวารหนัก ส่งผลให้เด็กนอนหลับไม่สนิท หงุดหงิดง่าย และอาจเกิดการติดเชื้อแบคทีเรียแทรกซ้อนจากการเกาจนผิวหนังถลอกได้ การวินิจฉัยหลักใช้วิธีสก็อตเทปเทสต์ (Scotch Tape Test) ในตอนเช้าตรู่ก่อนการชำระล้างร่างกาย
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
footer()