import sys
import os
import time
import tensorflow as tf
from tensorflow.keras.models import load_model

# บังคับให้ Python รู้จักโฟลเดอร์รากด้านนอกเพื่อเรียกใช้ styles.py
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import cv2
import numpy as np
from styles import inject_css, navbar, footer

st.set_page_config(
    page_title="OvaSight — AI Inference",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
navbar("ai")

st.markdown('<div class="content-body">', unsafe_allow_html=True)

# ปุ่มย้อนกลับไปหน้าหลัก
if st.button("⬅️ กลับหน้าหลัก (Home)", key="back_home_ai"):
    st.switch_page("app.py")

st.markdown('<div class="section-title" style="margin-top:15px;">📷 โมดูลวินิจฉัยและตรวจหาไข่พยาธิอัตโนมัติด้วยปัญญาประดิษฐ์</div>', unsafe_allow_html=True)

# ── 1. LOAD MODEL ──
@st.cache_resource
def load_ovasight_model():
    model_path = "ev_mobilenet_mobile.keras"
    if not os.path.exists(model_path):
        model_path = "/content/ev_mobilenet_mobile.keras"

    def mse(y_true, y_pred):
        return tf.reduce_mean(tf.square(y_true - y_pred))

    try:
        return load_model(model_path, custom_objects={'mse': mse})
    except Exception as e:
        st.error(f"⚠️ ตรวจพบข้อผิดพลาดขณะดึงโครงสร้างโมเดล Keras: {e}")
        st.info("💡 ตรวจสอบว่าไฟล์โมเดล ev_mobilenet_mobile.keras อยู่ในโฟลเดอร์เดียวกับ app.py ค่ะ")
        return None

model = load_ovasight_model()
class_label = ["Artifact", "Ev eggs"]

# ── 2. CORE ALGORITHM FUNCTIONS ──
def drawbox(img, label, a, b, c, d, color):
    text_color = (6, 64, 43)
    image = cv2.rectangle(img, (c, a), (d, b), color, 3)
    image = cv2.putText(image, label, (c, a - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
    return image

def compute_iou(box1, box2):
    y1 = max(box1[0], box2[0])
    y2 = min(box1[1], box2[1])
    x1 = max(box1[2], box2[2])
    x2 = min(box1[3], box2[3])
    inter_w = max(0, x2 - x1)
    inter_h = max(0, y2 - y1)
    inter_area = inter_w * inter_h
    box1_area = (box1[1] - box1[0]) * (box1[3] - box1[2])
    box2_area = (box2[1] - box2[0]) * (box2[3] - box2[2])
    union_area = box1_area + box2_area - inter_area
    if union_area == 0:
        return 0
    return inter_area / union_area

def nms(detections, iou_threshold):
    nms_dets = []
    for class_idx in set([d['class_idx'] for d in detections]):
        class_dets = [d for d in detections if d['class_idx'] == class_idx]
        class_dets = sorted(class_dets, key=lambda x: x['score'], reverse=True)
        keep = []
        while class_dets:
            curr = class_dets.pop(0)
            keep.append(curr)
            class_dets = [
                d for d in class_dets
                if compute_iou(curr['bbox'], d['bbox']) < iou_threshold
            ]
        nms_dets.extend(keep)
    return nms_dets

def merge_connected_boxes_by_class(detections, merge_iou_threshold):
    merged = []
    for class_idx in set([d['class_idx'] for d in detections]):
        class_dets = [d for d in detections if d['class_idx'] == class_idx]
        used = set()
        groups = []
        for i, det in enumerate(class_dets):
            if i in used:
                continue
            group = [det]
            used.add(i)
            changed = True
            while changed:
                changed = False
                for j, other in enumerate(class_dets):
                    if j in used:
                        continue
                    if any(compute_iou(d['bbox'], other['bbox']) > merge_iou_threshold for d in group):
                        group.append(other)
                        used.add(j)
                        changed = True
            groups.append(group)
        for group in groups:
            tops    = [d['bbox'][0] for d in group]
            bottoms = [d['bbox'][1] for d in group]
            lefts   = [d['bbox'][2] for d in group]
            rights  = [d['bbox'][3] for d in group]
            merged_box = [min(tops), max(bottoms), min(lefts), max(rights)]
            max_score  = max(d['score'] for d in group)
            merged.append({"bbox": merged_box, "class_idx": class_idx, "score": max_score})
    return merged

# ── 3. INTERACTIVE CONTROL PANEL ──
st.markdown("### 🎯 แผงควบคุมและจูนพารามิเตอร์โมเดล (Interactive Hyperparameters)")
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)

with ctrl_col1:
    threshold = st.slider("🎯 Confidence Threshold", 0.30, 0.99, 0.85, 0.05,
                          help="เกณฑ์คะแนนความมั่นใจขั้นต่ำในการระบุว่าเป็นไข่พยาธิ")
with ctrl_col2:
    nms_threshold = st.slider("⚡ NMS IoU Threshold", 0.10, 0.90, 0.30, 0.05,
                              help="เกณฑ์สำหรับคัดกรองกล่องที่ซ้อนทับกันเกินความจำเป็นออก")
with ctrl_col3:
    merge_iou_threshold = st.slider("🔗 Merge IoU Threshold", 0.0, 0.90, 0.15, 0.05,
                                    help="เกณฑ์ในการผสานวัตถุประเภทเดียวกันที่ซ้อนหรืออยู่ใกล้กันเข้าเป็นกล่องใหญ่เดียว")

st.write("---")

# ── 4. FILE UPLOADER & PROCESSING LAYER ──
uploaded_file = st.file_uploader("📂 เลือกไฟล์ภาพถ่ายสไลด์สก็อตเทปทวารหนัก (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if model is not None:
        with st.spinner('⏳ ระบบกำลังประมวลผลอัลกอริทึม Sliding Window และตรวจวิเคราะห์พยาธิวิทยา...'):
            start_time = time.time()

            box_size_y, box_size_x, step_size = 500, 500, 50
            resize_input_y, resize_input_x = 64, 64
            img_h, img_w = img.shape[:2]

            coords  = []
            patches = []

            for i in range(0, img_h - box_size_y + 1, step_size):
                for j in range(0, img_w - box_size_x + 1, step_size):
                    img_patch  = img[i:i+box_size_y, j:j+box_size_x]
                    brightness = np.mean(cv2.cvtColor(img_patch, cv2.COLOR_BGR2GRAY))
                    if brightness < 50:
                        continue
                    img_patch = cv2.resize(img_patch, (resize_input_x, resize_input_y), interpolation=cv2.INTER_AREA)
                    patches.append(img_patch)
                    coords.append((i, j))

            if len(patches) > 0:
                patches = np.array(patches)
                y_out   = model.predict(patches, batch_size=64, verbose=0)
                detections = []

                for idx, pred in enumerate(y_out):
                    for class_idx in range(len(class_label)):
                        score = pred[class_idx]
                        if score > threshold and class_idx != 0:
                            a, c = coords[idx]
                            b, d = a + box_size_y, c + box_size_x
                            detections.append({"bbox": [a, b, c, d], "score": float(score), "class_idx": class_idx})

                nms_detections = nms(detections, iou_threshold=nms_threshold)
                if merge_iou_threshold is not None and merge_iou_threshold > 0:
                    merged_detections = merge_connected_boxes_by_class(nms_detections, merge_iou_threshold=merge_iou_threshold)
                else:
                    merged_detections = nms_detections

                img_output = img.copy()
                colors     = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0)]
                total_eggs = 0

                for det in merged_detections:
                    a, b, c, d = det['bbox']
                    class_idx  = det['class_idx']
                    label      = f"{class_label[class_idx]}: {det['score']:.2f}"
                    color      = colors[class_idx % len(colors)]
                    img_output = drawbox(img_output, label, a, b, c, d, color)
                    if class_idx == 1:
                        total_eggs += 1

                inference_time = time.time() - start_time

                # ── 5. RESULTS SCREEN ──
                col_out1, col_out2 = st.columns(2)

                with col_out1:
                    st.markdown('<div style="font-size:16px; font-weight:700; margin-bottom:12px; color:var(--green-primary);">📋 สรุปผลการวินิจฉัยทางการแพทย์จากโมเดล</div>', unsafe_allow_html=True)

                    if total_eggs > 0:
                        st.markdown(f"""
                        <div class="m-card" style="border-left: 6px solid #e11d48; margin-bottom:15px;">
                            <div class="m-lbl" style="color:#e11d48; font-weight:700;">ผลวิเคราะห์ทางการแพทย์ (Verdict)</div>
                            <div class="m-val" style="color:#e11d48;">POSITIVE (พบการติดเชื้อ)</div>
                            <div style="font-size:14px; color:var(--text-muted); margin-top:6px;">ตรวจพบไข่พยาธิเข็มหมุด (Ev eggs) ทั้งหมดจำนวน <b>{total_eggs} ฟอง</b> บนภาพสไลด์แผ่นใส</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="m-card" style="border-left: 6px solid #0d9488; margin-bottom:15px;">
                            <div class="m-lbl" style="color:#0d9488; font-weight:700;">ผลวิเคราะห์ทางการแพทย์ (Verdict)</div>
                            <div class="m-val" style="color:#0d9488;">NEGATIVE (ไม่พบไข่พยาธิ)</div>
                            <div style="font-size:14px; color:var(--text-muted); margin-top:6px;">ไม่พบโครงสร้างสัณฐานวิทยาของตัวอ่อนหรือไข่พยาธิที่เกินเกณฑ์ความมั่นใจ</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="custom-box box-info">
                        <b>🔬 บันทึกพยาธิวิทยา (Clinical Diagnostics Metrics):</b><br>
                        * เวลาที่ใช้ประมวลผลอินเฟอเรนซ์: {inference_time:.2f} วินาที<br>
                        * จำนวนแผ่นภาพย่อยที่ถูกคัดกรอง: {len(patches)} ชิ้นภาพย่อย<br>
                        * ชนิดเป้าหมาย: <i>Enterobius vermicularis (Ev eggs)</i>
                    </div>
                    """, unsafe_allow_html=True)

                with col_out2:
                    st.markdown('<div style="font-size:16px; font-weight:700; margin-bottom:12px; color:var(--green-primary);">🔍 ภาพกราฟิกผลการตีกรอบพิกัดตรวจจับ (AI Inference)</div>', unsafe_allow_html=True)
                    st.image(cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB), use_container_width=True)

            else:
                st.warning("⚠️ ภาพถ่ายนี้มืดเกินไปหรือไม่มีพื้นที่สว่างเพียงพอสำหรับการทำ Sliding Window")
    else:
        st.warning("⚠️ ไม่สามารถประมวลผลรูปภาพได้ เนื่องจากโมเดลหลักยังไม่ได้ถูกโหลดเข้าสู่หน่วยความจำระบบ")

st.markdown('</div>', unsafe_allow_html=True)
footer()