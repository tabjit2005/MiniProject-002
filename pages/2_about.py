import streamlit as st

from diamond_utils import page_setup

page_setup(
    page_title="About",
    page_icon="👤",
    hero_title="👤 About",
    hero_subtitle="เกี่ยวกับเว็บแอปพลิเคชันนี้",
)

st.markdown('<div class="diamond-card">', unsafe_allow_html=True)
st.markdown(
    """
### ✨ เกี่ยวกับแอปนี้

**Diamond Price Predictor** เป็นเว็บแอปพลิเคชันสำหรับ **ประเมินราคาเพชร**
จากคุณสมบัติทางกายภาพ (4C: Carat, Cut, Color, Clarity และขนาดของเพชร)
โดยใช้โมเดล Machine Learning ที่ผ่านการฝึกสอนไว้ล่วงหน้า

จุดประสงค์ของโปรเจกต์นี้คือการสาธิตการนำโมเดลที่ฝึกด้วย **scikit-learn**
มาต่อยอดเป็นเว็บแอปพลิเคชันที่ใช้งานได้จริง ด้วย **Streamlit** และ deploy ขึ้น
**Streamlit Community Cloud**

#### 🛠️ เทคโนโลยีที่ใช้
- **Streamlit** — สร้าง Web UI
- **scikit-learn** — Pipeline / ColumnTransformer / HistGradientBoostingRegressor
- **pandas / numpy** — จัดการและแปลงข้อมูล

#### 📌 วิธีใช้งาน
1. ไปที่หน้าแรกของเว็บ (Diamond Price Predictor)
2. กรอกคุณสมบัติของเพชร (carat, cut, color, clarity, depth, table, ขนาด x/y/z)
3. กดปุ่ม **"ทำนายราคา"** เพื่อดูราคาประเมินเป็นสกุลเงิน USD

> ราคาที่ได้เป็นเพียงการประมาณจากรูปแบบทางสถิติของข้อมูล ไม่ใช่ราคาประเมินจริงจากผู้เชี่ยวชาญ
    """
)
st.markdown("</div>", unsafe_allow_html=True)
