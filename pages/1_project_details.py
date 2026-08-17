"""หน้ารายละเอียดโปรเจกต์ — จัดรูปแบบสำหรับใช้พูดนำเสนอ"""

from pathlib import Path

import pandas as pd
import streamlit as st

from diamond_utils import page_setup

ASSETS = Path(__file__).resolve().parents[1] / "assets"

page_setup(
    page_title="รายละเอียดโปรเจกต์ | MiniProject",
    page_icon="📊",
    hero_title="Diamond Price Prediction",
    hero_subtitle="ทำนายราคาเพชรจากคุณลักษณะทางกายภาพ ด้วย Histogram-based Gradient Boosting",
)

_PAGE_CSS = """
<style>
.step {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #38BDF8;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
}
.step .no {
    color: #D4AF37;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
}
.step .head { color: #EAF2FB; font-weight: 600; font-size: 1.02rem; margin: 0.15rem 0 0.3rem 0; }
.step .body { color: #9FB4CE; font-size: 0.92rem; line-height: 1.6; margin: 0; }

.stat {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 14px;
    padding: 1.1rem 1rem;
    text-align: center;
}
.stat .num {
    font-size: 1.9rem; font-weight: 700;
    background: linear-gradient(90deg, #7DD3FC 0%, #D4AF37 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.stat .cap { color: #9FB4CE; font-size: 0.85rem; letter-spacing: 0.03em; }
</style>
"""
st.markdown(_PAGE_CSS, unsafe_allow_html=True)


# ── ตัวช่วยเล็ก ๆ ────────────────────────────────────────────────
def stat(col, num, cap):
    col.markdown(f'<div class="stat"><div class="num">{num}</div>'
                 f'<div class="cap">{cap}</div></div>', unsafe_allow_html=True)


def step(no, head, body):
    st.markdown(f'<div class="step"><div class="no">{no}</div>'
                f'<div class="head">{head}</div><div class="body">{body}</div></div>',
                unsafe_allow_html=True)


def figure(name, caption):
    path = ASSETS / name
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(f"วางไฟล์ `{name}` ไว้ในโฟลเดอร์ `assets/` เพื่อแสดงกราฟ")


st.markdown('<div class="sparkle-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "1 · ปัญหา & Dataset",
    "2 · Data Preprocessing",
    "3 · ทฤษฎีของโมเดล",
    "4 · ผลการประเมิน",
])

# ══════════════ 1 ══════════════
with tab1:
    st.subheader("โจทย์ที่แก้")
    st.markdown(
        "**Supervised Learning — Regression** ทำนาย `price` (ตัวแปรต่อเนื่อง หน่วย USD) "
        "จากคุณลักษณะของเพชร 9 ตัว"
    )

    c1, c2, c3, c4 = st.columns(4)
    stat(c1, "53,940", "จำนวนแถว")
    stat(c2, "9", "Features")
    stat(c3, "3", "ตัวแปร Categorical")
    stat(c4, "$18,823", "ราคาสูงสุด")

    st.markdown("#### ทำไมถึงเลือก Dataset นี้")
    a, b = st.columns(2)
    with a:
        step("01", "มีทั้งตัวเลขและหมวดหมู่",
             "ได้ฝึกทำ encoding จริง ไม่ใช่แค่ scale ตัวเลขอย่างเดียว")
        step("02", "Categorical มีลำดับ",
             "cut / color / clarity เรียงตามมาตรฐาน GIA → ได้ตัดสินใจว่าจะใช้ ordinal หรือ one-hot")
    with b:
        step("03", "ข้อมูลไม่สะอาด",
             "มีมิติ x/y/z = 0 ซึ่งเป็นไปไม่ได้, เพชรกว้าง 58.9 มม., และแถวซ้ำ 146 แถว "
             "→ บังคับให้ต้องทำ preprocessing จริงจัง")
        step("04", "ตรวจสอบผลลัพธ์ได้",
             "หลัก 4C ของวงการเพชรบอกว่าน้ำหนักควรสำคัญที่สุด ใช้เช็คได้ว่าโมเดลเรียนถูกทาง")

# ══════════════ 2 ══════════════
with tab2:
    st.subheader("5 ขั้นตอน")

    a, b = st.columns(2)
    with a:
        step("01", "Data Cleaning",
             "ลบแถวซ้ำ 146 แถว · แปลง x/y/z = 0 เป็น NaN (ไม่ลบทิ้ง เพราะโมเดลจัดการ missing ได้เอง) "
             "· ตัด outlier ที่ผิดหลักกายภาพ")
        step("02", "Feature Encoding",
             "OrdinalEncoder ตามลำดับคุณภาพจริง เช่น I1 &lt; SI2 &lt; … &lt; IF "
             "เลือกแทน one-hot เพราะลำดับมีความหมายต่อราคา และลดจาก 20 คอลัมน์เหลือ 3")
        step("03", "Feature Engineering",
             "เพิ่ม volume = x·y·z และ ratio = x/y (ความสมมาตรของหน้าเพชร)")
    with b:
        step("04", "Target Transformation",
             "ใช้ log1p(price) → ความเบ้ลดจาก 1.62 เหลือ 0.12 "
             "ทำให้ loss ไม่ถูกครอบงำโดยเพชรราคาแพงไม่กี่เม็ด")
        step("05", "Data Splitting",
             "Train / Test = 80 / 20 และกันอีก 10% ของ train ไว้ทำ early stopping")

        st.markdown("###### ผลลัพธ์จำนวนแถว")
        st.markdown(
            '<div class="step"><p class="body" style="font-size:1.05rem;">'
            '53,940 &nbsp;→&nbsp; <span style="color:#7DD3FC">53,794</span> '
            '<span style="font-size:.8rem">(ลบซ้ำ)</span> &nbsp;→&nbsp; '
            '<span style="color:#D4AF37">53,785</span> '
            '<span style="font-size:.8rem">(ตัด outlier)</span></p></div>',
            unsafe_allow_html=True)

    figure("fig3_preprocessing.png", "ซ้าย–กลาง: ผลของ log1p · ขวา: outlier ที่ตรวจพบ")

# ══════════════ 3 ══════════════
with tab3:
    st.subheader("Histogram-based Gradient Boosting")
    st.markdown("โมเดลสร้างคำตอบแบบ **บวกสะสม** — ต้นไม้แต่ละต้นไม่ได้ทำนายราคา "
                "แต่ทำนาย *ความผิดพลาดที่เหลือ* ของต้นก่อนหน้า")
    st.latex(r"F_M(x) = F_0 + \eta \sum_{m=1}^{M} h_m(x)")

    c1, c2, c3, c4 = st.columns(4)
    stat(c1, "555", "จำนวนต้นไม้")
    stat(c2, "0.06", "Learning rate")
    stat(c3, "31", "Leaves ต่อต้น")
    stat(c4, "255", "Histogram bins")

    a, b = st.columns([1.1, 1])
    with a:
        st.markdown("###### ตัวอย่างจริง — เพชร 0.23 กะรัต (ราคาจริง \\$326)")
        st.dataframe(
            pd.DataFrame({
                "ขั้น": ["เริ่มต้น", "+ 1 ต้น", "+ 10 ต้น", "+ 50 ต้น", "+ 100 ต้น", "+ 555 ต้น"],
                "ราคาที่ทำนาย": ["$2,407", "$2,196", "$1,206", "$479", "$403", "$387"],
            }),
            hide_index=True, use_container_width=True,
        )
        st.caption("เริ่มจากค่าเฉลี่ยของข้อมูลทั้งหมด แล้วค่อย ๆ ไต่ลงมาทีละก้าวเล็ก ๆ")
    with b:
        step("ทำไมถึงเร็ว", "Histogram binning",
             "ทุก feature ถูกย่อเหลือไม่เกิน 255 ถัง การหาจุดตัดจึงดูแค่ 255 ค่า "
             "แทนที่จะไล่ดูทั้ง 53,785 ค่า → เทรนเร็วกว่า RandomForest 26 เท่า")
        step("ทำไมไม่ Overfit", "Regularization 3 ชั้น",
             "learning rate เล็ก · L2 บนค่า leaf · early stopping หยุดที่ต้นที่ 570 จาก 800")

    figure("fig4_learning_importance.png",
           "ซ้าย: Learning curve และจุด early stopping · ขวา: ความสำคัญของแต่ละ feature")

# ══════════════ 4 ══════════════
with tab4:
    st.subheader("เปรียบเทียบ 3 โมเดล")

    df = pd.DataFrame({
        "Model": ["Ridge (baseline)", "RandomForest", "HistGradientBoosting ★"],
        "R²": [0.9432, 0.9808, 0.9825],
        "RMSE ($)": [933, 542, 518],
        "MAE ($)": [439, 259, 256],
        "ขนาดไฟล์ (MB)": [0.004, 492.26, 2.38],
        "เวลาเทรน (วิ)": [0.15, 68.7, 2.7],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    stat(c1, "0.9825", "R² บน Test set")
    stat(c2, "$256", "ค่าคลาดเคลื่อนเฉลี่ย")
    stat(c3, "2.38 MB", "ขนาดโมเดล")

    st.markdown(
        '<div class="step"><div class="no">จุดชี้ขาด</div>'
        '<div class="head">RandomForest แม่นใกล้เคียงกัน แต่ไฟล์ใหญ่ 492 MB</div>'
        '<div class="body">เกินขีดจำกัด 100 MB ไป 5 เท่า จึง deploy ไม่ได้ '
        'ส่วน HistGradientBoosting เก็บแค่หมายเลขถังแบบ 8-bit เลยเหลือเพียง 2.38 MB '
        'และยังแม่นกว่าเล็กน้อยด้วย</div></div>',
        unsafe_allow_html=True)

    st.markdown("###### ความน่าเชื่อถือของผล")
    st.markdown(
        "Cross-validation 5-fold ได้ **R² = 0.9824 ± 0.0008** — "
        "ค่าเบี่ยงเบนต่ำมาก ยืนยันว่าผลไม่ได้มาจากการแบ่งข้อมูลที่บังเอิญดี"
    )

    figure("fig1_model_comparison.png", "เปรียบเทียบ 4 มิติ — สังเกตแกนขนาดไฟล์เป็น log scale")
    figure("fig2_residual.png", "ซ้าย: ค่าจริงเทียบค่าทำนาย · กลาง–ขวา: การกระจายของ residual")

st.markdown('<div class="sparkle-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
st.caption("ชุดข้อมูล: diamonds (53,940 แถว) · โมเดล: HistGradientBoostingRegressor · scikit-learn 1.8.0")
