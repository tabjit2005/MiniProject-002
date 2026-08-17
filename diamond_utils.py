"""Shared helpers for loading the diamond price model and preparing inputs."""

from pathlib import Path

import pandas as pd
import streamlit as st

MODEL_PATH = Path(__file__).parent / "models" / "diamond_price_model.pkl"

CUT_LEVELS = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
COLOR_LEVELS = ["D", "E", "F", "G", "H", "I", "J"]  # best -> worst
CLARITY_LEVELS = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]  # best -> worst

FEATURE_COLUMNS = [
    "cut", "color", "clarity", "carat", "depth", "table", "x", "y", "z", "volume", "ratio",
]

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.hero {
    padding: 2.2rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.6rem;
    background: linear-gradient(120deg, #0B1330 0%, #132444 45%, #0E3550 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -40%; right: -10%;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(56,189,248,0.25) 0%, rgba(56,189,248,0) 70%);
}
.hero h1 {
    font-weight: 700;
    font-size: 2.2rem;
    margin: 0 0 0.35rem 0;
    background: linear-gradient(90deg, #EAF2FB 0%, #7DD3FC 60%, #D4AF37 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero p { color: #B9C7DD; font-size: 1.02rem; margin: 0; }
.hero h1 a { display: none !important; }

.diamond-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    box-shadow: 0 4px 18px rgba(0,0,0,0.25);
}

.price-result {
    text-align: center;
    padding: 1.8rem 1rem;
    border-radius: 18px;
    background: linear-gradient(145deg, #0F2542 0%, #0B3A52 100%);
    border: 1px solid rgba(212, 175, 55, 0.35);
}
.price-result .label { color: #9FB4CE; font-size: 0.95rem; letter-spacing: 0.04em; text-transform: uppercase; }
.price-result .value {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #7DD3FC 0%, #D4AF37 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.sparkle-divider {
    text-align: center;
    color: #38BDF8;
    opacity: 0.55;
    letter-spacing: 0.6rem;
    margin: 0.6rem 0 1.4rem 0;
    font-size: 0.85rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1330 0%, #0E1D3D 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.15);
}

[data-testid="stSidebarNav"] {
    padding-top: 6px;
}
[data-testid="stSidebarNav"]::before {
    content: "MINIPROJECT";
    display: block;
    margin: 14px 16px 12px 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #7DD3FC 0%, #D4AF37 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
[data-testid="stSidebarNav"] a {
    margin: 2px 10px;
    padding: 10px 14px !important;
    border-radius: 10px;
    color: #B9C7DD !important;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    transition: all .2s ease;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(56, 189, 248, 0.1);
    color: #EAF2FB !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(90deg, rgba(56,189,248,0.15), rgba(212,175,55,0.08));
    color: #7DD3FC !important;
    box-shadow: inset 3px 0 0 #38BDF8;
}

/* เปลี่ยนข้อความเมนู sidebar เป็นภาษาไทย */
[data-testid="stSidebarNav"] li:nth-child(1) a * { display: none !important; }
[data-testid="stSidebarNav"] li:nth-child(1) a::after { content: "💎 หน้าหลัก"; display: inline-block; font-size: 1rem !important; }
[data-testid="stSidebarNav"] li:nth-child(2) a * { display: none !important; }
[data-testid="stSidebarNav"] li:nth-child(2) a::after { content: "📊 รายละเอียดโปรเจกต์"; display: inline-block; font-size: 1rem !important; }
[data-testid="stSidebarNav"] li:nth-child(3) a * { display: none !important; }
[data-testid="stSidebarNav"] li:nth-child(3) a::after { content: "🧑‍💻 ผู้พัฒนา"; display: inline-block; font-size: 1rem !important; }
</style>
"""


def page_setup(page_title, page_icon, hero_title, hero_subtitle):
    """Configure the page and inject the shared diamond theme + hero header.

    Must be the first Streamlit call in each page script (classic pages/
    multipage apps run every page as an independent script, so the theme
    can't just be injected once in app.py).
    """
    st.set_page_config(
        page_title=page_title, page_icon=page_icon,
        layout="wide", initial_sidebar_state="expanded",
    )
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero"><h1>{hero_title}</h1><p>{hero_subtitle}</p></div>',
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner="กำลังโหลดโมเดล...")
def load_model():
    import pickle

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def build_features(carat, cut, color, clarity, depth, table, x, y, z):
    """Assemble a single-row DataFrame with the engineered columns the model expects."""
    volume = x * y * z
    ratio = x / y if y else 0.0
    row = {
        "cut": cut, "color": color, "clarity": clarity,
        "carat": carat, "depth": depth, "table": table,
        "x": x, "y": y, "z": z,
        "volume": volume, "ratio": ratio,
    }
    return pd.DataFrame([row], columns=FEATURE_COLUMNS), volume, ratio


def predict_price(model, carat, cut, color, clarity, depth, table, x, y, z):
    df, volume, ratio = build_features(carat, cut, color, clarity, depth, table, x, y, z)
    price = float(model.predict(df)[0])
    return price, volume, ratio
