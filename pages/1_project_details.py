import streamlit as st

from diamond_utils import page_setup

page_setup(
    page_title="Project Info",
    page_icon="📊",
    hero_title="📊 Project Info",
    hero_subtitle="รายละเอียดของข้อมูล โมเดล และสถาปัตยกรรมที่ใช้ในโปรเจกต์",
)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="diamond-card">', unsafe_allow_html=True)
    st.markdown(
        """
#### 🗂️ Dataset
- **Diamonds dataset** — ข้อมูลเพชรประมาณ **53,940 เม็ด**
- คุณสมบัติ: `carat`, `cut`, `color`, `clarity`, `depth`, `table`, `x`, `y`, `z`, `price`
- Feature วิศวกรรมเพิ่มเติม:
  - `volume = x × y × z`
  - `ratio = x / y`

#### 🎯 Target
- `price` — ราคาเพชรเป็นสกุลเงิน **USD**
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="diamond-card">', unsafe_allow_html=True)
    st.markdown(
        """
#### 🧪 Model Evaluation *(โดยประมาณ)*
| Metric | ค่า |
|---|---|
| MAPE | ~5.4% |
| RMSE | ~$473 |

> ตัวเลขนี้เป็นการประเมินภายในของทีมพัฒนาเว็บแอป โดยเปรียบเทียบผลทำนายกับข้อมูลทั้งชุด
> ไม่ใช่ metric ที่รายงานอย่างเป็นทางการจากขั้นตอนฝึกสอนโมเดล และไม่ได้แยก held-out test set
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="diamond-card">', unsafe_allow_html=True)
    st.markdown(
        """
#### 🧠 Model Architecture

```
Pipeline
├── prep: ColumnTransformer
│   ├── ord: OrdinalEncoder
│   │        cut / color / clarity
│   └── num: passthrough
│            carat, depth, table,
│            x, y, z, volume, ratio
└── model: TransformedTargetRegressor
             transformer: log1p / expm1
             regressor: HistGradientBoostingRegressor
```

**Hyperparameters หลักของ HistGradientBoostingRegressor**
- `learning_rate` = 0.06
- `max_iter` = 800
- `max_leaf_nodes` = 31
- `min_samples_leaf` = 20
- `l2_regularization` = 1.0
- `early_stopping` = True
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="diamond-card">', unsafe_allow_html=True)
    st.markdown(
        """
#### 📏 Ordinal Encoding

โมเดลเข้ารหัส categorical feature ตามลำดับคุณภาพ (แย่ → ดี):

- **Cut:** Fair &lt; Good &lt; Very Good &lt; Premium &lt; Ideal
- **Color:** J &lt; I &lt; H &lt; G &lt; F &lt; E &lt; D
- **Clarity:** I1 &lt; SI2 &lt; SI1 &lt; VS2 &lt; VS1 &lt; VVS2 &lt; VVS1 &lt; IF
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)
