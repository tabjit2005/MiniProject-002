import base64
from pathlib import Path

import streamlit as st

from diamond_utils import page_setup

page_setup(
    page_title="ผู้พัฒนา | MiniProject",
    page_icon="🧑‍💻",
    hero_title="🧑‍💻 ผู้พัฒนา",
    hero_subtitle="ข้อมูลผู้จัดทำ MiniProject",
)

st.markdown("""
<style>
.profile-photo-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 1.4rem;
}
.profile-photo-wrap img {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 3px solid transparent;
    background:
        linear-gradient(#0B1330, #0B1330) padding-box,
        linear-gradient(135deg, #7DD3FC, #38BDF8, #D4AF37) border-box;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.25);
    object-fit: cover;
}

.profile-card h2 {
    color: #EAF2FB;
    font-weight: 700;
    font-size: 1.4rem;
    margin: 0 0 1rem 0;
    text-align: center;
}
.info-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 4px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.95rem;
}
.info-row:first-of-type { border-top: none; }
.info-row span.label { color: #9FB4CE; }
.info-row span.value { font-weight: 600; color: #7DD3FC; }
</style>
""", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 1, 1])
with mid:
    photo_path = Path(__file__).resolve().parent.parent / "assets" / "2.jpg"
    if photo_path.exists():
        photo_b64 = base64.b64encode(photo_path.read_bytes()).decode()
        st.markdown(
            f'<div class="profile-photo-wrap"><img src="data:image/jpeg;base64,{photo_b64}"></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="diamond-card profile-card">
            <h2>กมลวรรณ ทับจิต</h2>
            <div class="info-row"><span class="label">รหัสนักศึกษา</span><span class="value">664245002</span></div>
            <div class="info-row"><span class="label">หมู่เรียน</span><span class="value">Sec. 66/43</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="sparkle-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
st.caption("Made with Streamlit · Machine Learning Projects")
