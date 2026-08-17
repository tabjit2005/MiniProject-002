import streamlit as st

from diamond_utils import CLARITY_LEVELS, COLOR_LEVELS, CUT_LEVELS, load_model, page_setup, predict_price

page_setup(
    page_title="Diamond Price Predictor",
    page_icon="💎",
    hero_title="💎 Diamond Price Predictor",
    hero_subtitle=(
        "กรอกคุณสมบัติของเพชรเพื่อประเมินราคาด้วยโมเดล Machine Learning "
        "(HistGradientBoostingRegressor) ที่ฝึกจากข้อมูลเพชรกว่า 53,000 เม็ด"
    ),
)

try:
    model = load_model()
except FileNotFoundError:
    st.error("ไม่พบไฟล์โมเดลที่ `models/diamond_price_model.pkl` กรุณาตรวจสอบว่าไฟล์อยู่ในตำแหน่งที่ถูกต้อง")
    st.stop()

left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown('<div class="diamond-card">', unsafe_allow_html=True)
    st.subheader("✏️ คุณสมบัติของเพชร")

    c1, c2 = st.columns(2)
    with c1:
        carat = st.number_input(
            "Carat (กะรัต)", min_value=0.20, max_value=5.50, value=0.70, step=0.01,
            help="น้ำหนักของเพชร หน่วยกะรัต",
        )
        cut = st.selectbox("Cut (การเจียระไน)", CUT_LEVELS, index=CUT_LEVELS.index("Ideal"))
        color = st.selectbox(
            "Color (สี)", COLOR_LEVELS, index=COLOR_LEVELS.index("G"),
            help="D = ไร้สีที่สุด (ดีที่สุด) ... J = มีสีเหลืองอ่อนมากที่สุด",
        )
        clarity = st.selectbox(
            "Clarity (ความสะอาด)", CLARITY_LEVELS, index=CLARITY_LEVELS.index("SI1"),
            help="IF = ไม่มีตำหนิ (ดีที่สุด) ... I1 = มีตำหนิชัดเจน",
        )
    with c2:
        depth = st.number_input(
            "Depth % (ความลึก)", min_value=43.0, max_value=79.0, value=61.8, step=0.1,
            help="สัดส่วนความลึก = z / mean(x, y) x 100",
        )
        table = st.number_input(
            "Table % (หน้าเพชร)", min_value=43.0, max_value=95.0, value=57.0, step=0.1,
            help="ความกว้างของหน้าเพชรเทียบกับจุดกว้างที่สุด",
        )
        x = st.number_input("Length x (มม.)", min_value=0.10, max_value=11.00, value=5.70, step=0.01)
        y = st.number_input("Width y (มม.)", min_value=0.10, max_value=11.00, value=5.71, step=0.01)
        z = st.number_input("Depth z (มม.)", min_value=0.10, max_value=8.50, value=3.53, step=0.01)

    st.markdown("</div>", unsafe_allow_html=True)

    predict_clicked = st.button("🔮 ทำนายราคา", type="primary", use_container_width=True)

with right:
    if predict_clicked:
        if y == 0:
            st.error("ค่า Width (y) ต้องไม่เป็น 0")
        else:
            price, volume, ratio = predict_price(model, carat, cut, color, clarity, depth, table, x, y, z)
            st.markdown(
                f"""
                <div class="price-result">
                    <div class="label">ราคาประเมิน (USD)</div>
                    <div class="value">${price:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(f"คำนวณจาก volume ≈ {volume:.2f} mm³ และ ratio (x/y) ≈ {ratio:.2f}")

            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Carat", f"{carat:.2f}")
            m2.metric("Cut", cut)
            m3.metric("Clarity", clarity)
    else:
        st.markdown(
            """
            <div class="diamond-card" style="text-align:center; padding: 3rem 1.5rem;">
                <div style="font-size:3rem;">💎</div>
                <p style="color:#9FB4CE; margin-top:0.6rem;">
                    กรอกข้อมูลด้านซ้ายแล้วกดปุ่ม<br>"ทำนายราคา" เพื่อดูผลลัพธ์
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="sparkle-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
st.caption(
    "โมเดลนี้ใช้เพื่อการศึกษาเท่านั้น ราคาที่ได้เป็นการประมาณจากรูปแบบในข้อมูลฝึกสอน "
    "ไม่ใช่ราคาประเมินจากผู้เชี่ยวชาญด้านอัญมณีจริง"
)
