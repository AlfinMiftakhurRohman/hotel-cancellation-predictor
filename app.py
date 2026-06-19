import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="HotelSight",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    * { font-family: 'Outfit', sans-serif; }

    .stApp {
        background: linear-gradient(160deg, #06080f 0%, #0c1222 30%, #111a2e 60%, #0a1628 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080d19 0%, #0e1525 50%, #121c33 100%);
        border-right: 1px solid rgba(100,160,255,0.06);
    }
    [data-testid="stSidebar"] * { color: #a0b4d0 !important; }

    h1 { color: #f1f5f9 !important; font-weight: 800 !important; }
    h2 { color: #e8edf5 !important; font-weight: 700 !important; }
    h3 { color: #e2e8f0 !important; font-weight: 600 !important; }
    h4, h5 { color: #dbe4f0 !important; font-weight: 600 !important; }
    p, span, label, li, div { color: #c8d6e5 !important; }

    .hero {
        background: linear-gradient(135deg, rgba(56,120,220,0.12) 0%, rgba(120,80,220,0.08) 50%, rgba(56,120,220,0.05) 100%);
        border: 1px solid rgba(100,160,255,0.1);
        border-radius: 24px;
        padding: 48px 44px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: '';
        position: absolute;
        top: -60%;
        right: -15%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(80,140,255,0.06) 0%, transparent 65%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #7cb8ff, #a78bfa, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 10px 0;
        line-height: 1.1;
    }
    .hero-sub {
        font-size: 17px !important;
        color: #8fa8c8 !important;
        margin: 0;
        max-width: 600px;
        line-height: 1.6;
    }

    .glass {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 28px;
        backdrop-filter: blur(8px);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass:hover {
        border-color: rgba(100,160,255,0.18);
        box-shadow: 0 8px 40px rgba(50,100,200,0.08);
    }

    .glass-title {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #7cb8ff !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0 0 14px 0;
    }
    .glass-body {
        font-size: 14.5px !important;
        color: #a0b4d0 !important;
        line-height: 1.75;
        margin: 0;
    }
    .glass-body b { color: #d0dff0 !important; }

    .m-card {
        background: linear-gradient(135deg, rgba(60,130,246,0.08), rgba(100,160,255,0.03));
        border: 1px solid rgba(100,160,255,0.1);
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .m-card:hover {
        transform: translateY(-4px);
        border-color: rgba(100,160,255,0.3);
        box-shadow: 0 12px 30px rgba(50,100,220,0.12);
    }
    .m-label {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        color: #7090b0 !important;
        margin: 0;
    }
    .m-value {
        font-size: 36px !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
        margin: 8px 0 0 0;
        background: linear-gradient(135deg, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .res-cancel {
        background: linear-gradient(135deg, rgba(220,50,50,0.12), rgba(180,30,30,0.06));
        border: 1px solid rgba(248,113,113,0.25);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
    }
    .res-cancel h2 {
        font-size: 26px !important;
        color: #fca5a5 !important;
        margin: 0 0 8px 0;
    }
    .res-cancel p { color: #fecaca !important; font-size: 15px !important; }

    .res-safe {
        background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(20,140,70,0.06));
        border: 1px solid rgba(74,222,128,0.25);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
    }
    .res-safe h2 {
        font-size: 26px !important;
        color: #86efac !important;
        margin: 0 0 8px 0;
    }
    .res-safe p { color: #bbf7d0 !important; font-size: 15px !important; }

    .risk-box {
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        transition: all 0.2s ease;
    }
    .risk-box:hover { transform: translateY(-2px); }
    .risk-high {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.2);
    }
    .risk-med {
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.2);
    }
    .risk-low {
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.2);
    }
    .risk-label { font-size: 11px !important; color: #708090 !important; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
    .risk-val { font-size: 22px !important; font-weight: 700 !important; color: #e2e8f0 !important; margin: 6px 0; }
    .risk-level-high { font-size: 12px !important; color: #f87171 !important; margin: 0; font-weight: 500; }
    .risk-level-med { font-size: 12px !important; color: #fbbf24 !important; margin: 0; font-weight: 500; }
    .risk-level-low { font-size: 12px !important; color: #4ade80 !important; margin: 0; font-weight: 500; }

    .model-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.1));
        border: 1px solid rgba(100,160,255,0.2);
        color: #93c5fd !important;
        padding: 6px 16px;
        border-radius: 24px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.8px;
        margin: 2px;
    }

    .sep {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(100,160,255,0.12), transparent);
        margin: 32px 0;
    }

    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stSlider > div > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #3b82f6, #7c3aed) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        box-shadow: 0 8px 30px rgba(59,130,246,0.35) !important;
    }

    .footer {
        text-align: center;
        padding: 40px 0 20px;
        font-size: 11px !important;
        color: #3a4a5c !important;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():
    rf = joblib.load("hotel_model_rf.pkl")
    sc = joblib.load("hotel_scaler.pkl")
    ft = joblib.load("feature_columns.pkl")
    mt = joblib.load("model_metrics.pkl")
    return rf, sc, ft, mt

try:
    model, scaler, feature_cols, metrics_df = load_model()
    model_loaded = True
except:
    model_loaded = False


# =====================================================
# HELPERS
# =====================================================

def prepare_input(raw):
    df = pd.DataFrame([raw])
    df["total_stay"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df["total_guests"] = df["adults"] + df["children"] + df["babies"]
    df["revenue_estimate"] = df["adr"] * df["total_stay"]

    top = ['PRT','GBR','FRA','ESP','DEU','ITA','IRL','BEL','BRA','NLD']
    df["country_grouped"] = df["country"].apply(lambda x: x if x in top else "Other")

    df = df.drop(columns=[
        "stays_in_weekend_nights","stays_in_week_nights",
        "adults","children","babies","country"
    ], errors='ignore')

    df_enc = pd.get_dummies(df, drop_first=True)
    out = pd.DataFrame(columns=feature_cols, data=np.zeros((1, len(feature_cols))))
    for c in df_enc.columns:
        if c in out.columns:
            out[c] = df_enc[c].values
    return out


def dark_layout(fig, title="", h=400):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color='#d0dff0', family='Outfit')),
        height=h,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#8fa8c8'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.03)', zerolinecolor='rgba(255,255,255,0.03)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.03)', zerolinecolor='rgba(255,255,255,0.03)'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8fa8c8'))
    )
    return fig


def gauge(prob):
    if prob < 0.3:
        c, lab = "#22c55e", "RISIKO RENDAH"
    elif prob < 0.6:
        c, lab = "#f59e0b", "RISIKO SEDANG"
    else:
        c, lab = "#ef4444", "RISIKO TINGGI"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={'suffix':'%', 'font':{'size':50, 'color':c, 'family':'JetBrains Mono'}},
        title={'text':lab, 'font':{'size':13, 'color':c, 'family':'Outfit'}},
        gauge={
            'axis':{'range':[0,100], 'tickwidth':0, 'tickfont':{'color':'#3a4a5c'}},
            'bar':{'color':c, 'thickness':0.25},
            'bgcolor':'rgba(255,255,255,0.02)',
            'borderwidth':0,
            'steps':[
                {'range':[0,30], 'color':'rgba(34,197,94,0.06)'},
                {'range':[30,60], 'color':'rgba(245,158,11,0.06)'},
                {'range':[60,100], 'color':'rgba(239,68,68,0.06)'},
            ],
        }
    ))
    fig.update_layout(
        height=260, margin=dict(t=50,b=10,l=30,r=30),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown(
        '<div style="text-align:center; padding:24px 0 16px; border-bottom:1px solid rgba(100,160,255,0.06);">'
        '<p style="font-size:28px !important; font-weight:800 !important; '
        'background:linear-gradient(135deg,#7cb8ff,#a78bfa); '
        '-webkit-background-clip:text; -webkit-text-fill-color:transparent; '
        'margin:0; letter-spacing:-1px;">HotelSight</p>'
        '<p style="font-size:10px !important; letter-spacing:4px; '
        'text-transform:uppercase; opacity:0.35; margin:6px 0 0;">Prediction System</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    page = st.radio(
        "nav", ["About Model", "Prediksi", "Validasi Eksternal"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center; padding:8px 0;">'
        '<span class="model-badge">Random Forest</span> '
        '<span class="model-badge">Neural Network</span><br><br>'
        '<span class="model-badge">scikit-learn</span> '
        '<span class="model-badge">Streamlit</span>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        '<p style="text-align:center; font-size:10px !important; opacity:0.3; line-height:1.8;">'
        'Big Data Analytics<br>Kelompok 07<br>FEB Universitas Jember<br>2026</p>',
        unsafe_allow_html=True
    )


# =====================================================
# ABOUT MODEL
# =====================================================

if page == "About Model":

    st.markdown(
        '<div class="hero">'
        '<p class="hero-title">HotelSight</p>'
        '<p class="hero-sub">Sistem prediksi pembatalan reservasi hotel '
        'berbasis Machine Learning. Dilatih dengan 119.390 data reservasi '
        'dari dua hotel di Portugal, periode 2015 hingga 2017.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown(
            '<div class="glass">'
            '<p class="glass-title">Model yang Digunakan</p>'
            '<p class="glass-body">'
            'Kami melatih dua algoritma dan membandingkan hasilnya:<br><br>'
            '<b>1. Random Forest</b> (200 trees, balanced class weight)<br>'
            'Algoritma ensemble yang bekerja dengan menggabungkan ratusan '
            'decision tree. Dipilih sebagai <b>model utama</b> karena '
            'memberikan performa terbaik di seluruh metrik evaluasi.<br><br>'
            '<b>2. Neural Network / MLP</b> (128-64 neuron)<br>'
            'Multilayer Perceptron dengan dua hidden layer sebagai '
            'pembanding. Mampu menangkap pola nonlinier, namun '
            'performanya sedikit di bawah Random Forest pada dataset ini.<br><br>'
            'Validasi dilakukan dengan <b>10-Fold Stratified Cross Validation</b> '
            'untuk memastikan hasil yang konsisten.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="glass">'
            '<p class="glass-title">Dataset</p>'
            '<p class="glass-body">'
            '<b>Sumber:</b> Hotel Booking Demand (Kaggle)<br>'
            '<b>Penulis:</b> Nuno Antonio et al. (2019)<br>'
            '<b>Total:</b> 119.390 reservasi<br>'
            '<b>Tingkat Cancel:</b> sekitar 37%<br>'
            '<b>Periode:</b> Juli 2015 - Agustus 2017<br>'
            '<b>Hotel:</b> City Hotel dan Resort Hotel<br>'
            '<b>Lokasi:</b> Portugal'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="glass">'
            '<p class="glass-title">Preprocessing</p>'
            '<p class="glass-body">'
            'Missing value handling &bull; '
            'Duplicate removal &bull; '
            'Feature engineering &bull; '
            'Country grouping (177 &#8594; 11) &bull; '
            'One-Hot Encoding &bull; '
            'StandardScaler'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    if model_loaded:
        st.markdown('<hr class="sep">', unsafe_allow_html=True)

        rf = metrics_df[metrics_df["Model"] == "Random Forest"].iloc[0]
        nn = metrics_df[metrics_df["Model"] == "Neural Network"].iloc[0]
        names = ["Accuracy","Precision","Recall","F1-Score","AUC","MCC"]

        st.markdown("### Performa pada Test Set")
        st.markdown(
            '<p style="font-size:13px; color:#6080a0 !important; margin-bottom:20px;">'
            'Random Forest dipilih sebagai model utama. Semua skor dihitung pada 20% data uji.</p>',
            unsafe_allow_html=True
        )

        st.markdown("##### Random Forest (Model Utama)")
        cols = st.columns(6)
        for i, m in enumerate(names):
            with cols[i]:
                st.markdown(
                    f'<div class="m-card"><p class="m-label">{m}</p>'
                    f'<p class="m-value">{rf[m]:.3f}</p></div>',
                    unsafe_allow_html=True
                )

        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        st.markdown("##### Neural Network (Pembanding)")
        cols2 = st.columns(6)
        for i, m in enumerate(names):
            with cols2[i]:
                st.markdown(
                    f'<div class="m-card"><p class="m-label">{m}</p>'
                    f'<p class="m-value">{nn[m]:.3f}</p></div>',
                    unsafe_allow_html=True
                )

        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Random Forest', x=names,
            y=[rf[m] for m in names],
            marker_color='#3b82f6',
            text=[f"{rf[m]:.3f}" for m in names],
            textposition='outside', textfont=dict(color='#7cb8ff', size=13)
        ))
        fig.add_trace(go.Bar(
            name='Neural Network', x=names,
            y=[nn[m] for m in names],
            marker_color='#8b5cf6',
            text=[f"{nn[m]:.3f}" for m in names],
            textposition='outside', textfont=dict(color='#c4b5fd', size=13)
        ))
        fig = dark_layout(fig, "Perbandingan Random Forest vs Neural Network", 440)
        fig.update_layout(barmode='group', yaxis_range=[0, 1.18])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("File model tidak ditemukan. Jalankan notebook terlebih dahulu untuk men-generate file .pkl.")


# =====================================================
# PREDIKSI
# =====================================================

elif page == "Prediksi":

    st.markdown(
        '<div class="hero">'
        '<p class="hero-title">Prediksi Reservasi</p>'
        '<p class="hero-sub">Masukkan data reservasi di bawah ini. '
        'Sistem akan menganalisis menggunakan model Random Forest '
        'dan memberikan estimasi kemungkinan pembatalan.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    if not model_loaded:
        st.error("Model belum tersedia.")
        st.stop()

    with st.form("predict"):

        st.markdown("##### Hotel dan Kamar")
        a1, a2, a3, a4 = st.columns(4)
        with a1: hotel = st.selectbox("Tipe Hotel", ["City Hotel","Resort Hotel"])
        with a2: room = st.selectbox("Tipe Kamar", ["A","B","C","D","E","F","G","H","L","P"])
        with a3: meal = st.selectbox("Paket Makan", ["BB","HB","FB","SC","Undefined"])
        with a4: deposit = st.selectbox("Tipe Deposit", ["No Deposit","Non Refund","Refundable"])

        st.markdown("##### Detail Pemesanan")
        b1, b2, b3, b4 = st.columns(4)
        with b1: lead_time = st.number_input("Lead Time (hari)", 0, 800, 100)
        with b2: arrival_month = st.slider("Bulan Kedatangan", 1, 12, 6)
        with b3: wkend = st.number_input("Malam Weekend", 0, 10, 1)
        with b4: wkday = st.number_input("Malam Weekday", 0, 20, 2)

        st.markdown("##### Tamu")
        c1, c2, c3, c4 = st.columns(4)
        with c1: n_adults = st.number_input("Dewasa", 1, 10, 2)
        with c2: n_child = st.number_input("Anak-anak", 0, 10, 0)
        with c3: n_baby = st.number_input("Bayi", 0, 5, 0)
        with c4: repeated = st.selectbox("Tamu Berulang", ["Tidak","Ya"])

        st.markdown("##### Riwayat dan Channel")
        d1, d2, d3, d4 = st.columns(4)
        with d1: prev_c = st.number_input("Riwayat Cancel", 0, 30, 0)
        with d2: prev_nc = st.number_input("Riwayat Tidak Cancel", 0, 50, 0)
        with d3: mkt = st.selectbox("Market Segment", ["Online TA","Offline TA/TO","Direct","Corporate","Groups","Complementary","Aviation"])
        with d4: dist = st.selectbox("Distribution Channel", ["TA/TO","Direct","Corporate","GDS"])

        st.markdown("##### Lainnya")
        e1, e2, e3, e4, e5 = st.columns(5)
        with e1: cust = st.selectbox("Tipe Customer", ["Transient","Transient-Party","Contract","Group"])
        with e2: adr = st.number_input("ADR (harga/malam)", 0.0, 5000.0, 100.0)
        with e3: spec = st.number_input("Special Requests", 0, 10, 0)
        with e4: park = st.number_input("Parking Spaces", 0, 5, 0)
        with e5: changes = st.number_input("Perubahan Booking", 0, 20, 0)

        f1, f2, f3 = st.columns(3)
        with f1: country = st.selectbox("Negara Asal", ["PRT","GBR","FRA","ESP","DEU","ITA","IRL","BEL","BRA","NLD","Other"])
        with f2: agent = st.selectbox("Via Agen Travel", ["Tidak","Ya"])
        with f3: wait = st.number_input("Waiting List (hari)", 0, 400, 0)

        go_btn = st.form_submit_button("Analisis Reservasi", use_container_width=True)

    if go_btn:
        raw = {
            "hotel": hotel, "lead_time": lead_time,
            "stays_in_weekend_nights": wkend, "stays_in_week_nights": wkday,
            "adults": n_adults, "children": n_child, "babies": n_baby,
            "meal": meal, "country": country, "market_segment": mkt,
            "distribution_channel": dist,
            "is_repeated_guest": 1 if repeated == "Ya" else 0,
            "previous_cancellations": prev_c,
            "previous_bookings_not_canceled": prev_nc,
            "reserved_room_type": room, "booking_changes": changes,
            "deposit_type": deposit, "days_in_waiting_list": wait,
            "customer_type": cust, "adr": adr,
            "required_car_parking_spaces": park,
            "total_of_special_requests": spec,
            "is_agent_booking": 1 if agent == "Ya" else 0,
            "arrival_month": arrival_month,
        }

        X_in = prepare_input(raw)
        pred = model.predict(X_in)[0]
        prob = model.predict_proba(X_in)[0]

        st.markdown('<hr class="sep">', unsafe_allow_html=True)

        rc1, rc2 = st.columns([1, 1])

        with rc1:
            if pred == 1:
                st.markdown(
                    '<div class="res-cancel">'
                    '<h2>DIPREDIKSI CANCEL</h2>'
                    '<p>Reservasi ini memiliki risiko tinggi untuk dibatalkan.</p>'
                    '</div>', unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="res-safe">'
                    '<h2>DIPREDIKSI AMAN</h2>'
                    '<p>Reservasi ini diprediksi akan berjalan sesuai rencana.</p>'
                    '</div>', unsafe_allow_html=True
                )

        with rc2:
            st.plotly_chart(gauge(prob[1]), use_container_width=True)

        st.markdown("##### Faktor Risiko")
        fc1, fc2, fc3, fc4 = st.columns(4)

        def risk_card(label, value, level):
            if level == "high":
                cls, lcls = "risk-high", "risk-level-high"
                ltxt = "Risiko Tinggi"
            elif level == "med":
                cls, lcls = "risk-med", "risk-level-med"
                ltxt = "Risiko Sedang"
            else:
                cls, lcls = "risk-low", "risk-level-low"
                ltxt = "Risiko Rendah"
            return (
                f'<div class="risk-box {cls}">'
                f'<p class="risk-label">{label}</p>'
                f'<p class="risk-val">{value}</p>'
                f'<p class="{lcls}">{ltxt}</p>'
                f'</div>'
            )

        with fc1:
            lvl = "high" if lead_time > 200 else "med" if lead_time > 60 else "low"
            st.markdown(risk_card("Lead Time", f"{lead_time} hari", lvl), unsafe_allow_html=True)
        with fc2:
            lvl = "high" if deposit == "No Deposit" else "low"
            st.markdown(risk_card("Deposit", deposit, lvl), unsafe_allow_html=True)
        with fc3:
            lvl = "high" if prev_c > 0 else "low"
            st.markdown(risk_card("Riwayat Cancel", f"{prev_c}x", lvl), unsafe_allow_html=True)
        with fc4:
            lvl = "high" if spec == 0 else "low"
            st.markdown(risk_card("Special Requests", str(spec), lvl), unsafe_allow_html=True)

        st.markdown(
            '<p style="font-size:12px; color:#506070 !important; text-align:center; margin-top:24px;">'
            'Prediksi menggunakan model Random Forest (200 trees, balanced)</p>',
            unsafe_allow_html=True
        )


# =====================================================
# VALIDASI EKSTERNAL
# =====================================================

elif page == "Validasi Eksternal":

    st.markdown(
        '<div class="hero">'
        '<p class="hero-title">Validasi Eksternal</p>'
        '<p class="hero-sub">Uji kemampuan generalisasi model dengan data '
        'dari sumber yang berbeda. Upload dataset reservasi hotel, '
        'lalu sistem akan otomatis menyesuaikan format dan menghitung performa model.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    if not model_loaded:
        st.error("Model belum tersedia.")
        st.stop()

    v1, v2 = st.columns([3, 2])

    with v1:
        st.markdown(
            '<div class="glass">'
            '<p class="glass-title">Cara Kerja</p>'
            '<p class="glass-body">'
            '<b>1.</b> Upload file CSV yang memiliki kolom booking hotel '
            '(lead_time, no_of_adults, avg_price_per_room, booking_status, dll).<br>'
            '<b>2.</b> Sistem melakukan mapping kolom secara otomatis ke format '
            'yang dibutuhkan model Random Forest.<br>'
            '<b>3.</b> Model memprediksi seluruh baris data.<br>'
            '<b>4.</b> Hasil prediksi dibandingkan dengan label aktual untuk '
            'menghitung Accuracy, Precision, Recall, F1, AUC, dan MCC.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with v2:
        st.markdown(
            '<div class="glass">'
            '<p class="glass-title">Catatan Penting</p>'
            '<p class="glass-body">'
            'Beberapa fitur yang digunakan model '
            '(deposit_type, distribution_channel, customer_type, booking_changes) '
            'mungkin tidak tersedia di dataset yang di-upload. '
            'Fitur tersebut akan diisi dengan nilai default. '
            'Performa mungkin lebih rendah dari test set asli, '
            'dan itu adalah hal yang wajar dalam external validation.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload dataset (.csv)", type="csv")

    if uploaded is not None:
        df_ext = pd.read_csv(uploaded)
        st.success(f"Dataset dimuat: {df_ext.shape[0]:,} baris, {df_ext.shape[1]} kolom")

        with st.expander("Preview Data"):
            st.dataframe(df_ext.head(10), use_container_width=True)

        if st.button("Jalankan Validasi", type="primary", use_container_width=True):

            with st.spinner("Mapping kolom dan menjalankan prediksi..."):

                dm = pd.DataFrame()
                dm["hotel"] = "City Hotel"
                dm["lead_time"] = df_ext.get("lead_time", 0)
                dm["stays_in_weekend_nights"] = df_ext.get("no_of_weekend_nights", 0)
                dm["stays_in_week_nights"] = df_ext.get("no_of_week_nights", 0)
                dm["adults"] = df_ext.get("no_of_adults", 2)
                dm["children"] = df_ext.get("no_of_children", 0)
                dm["babies"] = 0
                dm["is_repeated_guest"] = df_ext.get("repeated_guest", 0)
                dm["previous_cancellations"] = df_ext.get("no_of_previous_cancellations", 0)
                dm["previous_bookings_not_canceled"] = df_ext.get("no_of_previous_bookings_not_canceled", 0)
                dm["adr"] = df_ext.get("avg_price_per_room", 0)
                dm["required_car_parking_spaces"] = df_ext.get("required_car_parking_space", 0)
                dm["total_of_special_requests"] = df_ext.get("no_of_special_requests", 0)
                dm["booking_changes"] = 0
                dm["days_in_waiting_list"] = 0
                dm["is_agent_booking"] = 0

                mm = {"Meal Plan 1":"BB","Meal Plan 2":"HB","Meal Plan 3":"FB","Not Selected":"SC"}
                dm["meal"] = df_ext.get("type_of_meal_plan","SC").map(mm).fillna("SC")

                rm = {"Room_Type 1":"A","Room_Type 2":"B","Room_Type 3":"C","Room_Type 4":"D","Room_Type 5":"E","Room_Type 6":"F","Room_Type 7":"G"}
                dm["reserved_room_type"] = df_ext.get("room_type_reserved","A").map(rm).fillna("A")

                sm = {"Online":"Online TA","Offline":"Offline TA/TO","Corporate":"Corporate","Aviation":"Aviation","Complementary":"Complementary"}
                dm["market_segment"] = df_ext.get("market_segment_type","Online TA").map(sm).fillna("Online TA")

                dm["deposit_type"] = "No Deposit"
                dm["distribution_channel"] = "TA/TO"
                dm["customer_type"] = "Transient"
                dm["country"] = "Other"
                dm["arrival_month"] = df_ext.get("arrival_month", 6)

                dm["total_stay"] = dm["stays_in_weekend_nights"] + dm["stays_in_week_nights"]
                dm["total_guests"] = dm["adults"] + dm["children"] + dm["babies"]
                dm["revenue_estimate"] = dm["adr"] * dm["total_stay"]
                dm["country_grouped"] = "Other"

                dp = dm.drop(columns=["stays_in_weekend_nights","stays_in_week_nights","adults","children","babies","country"])
                de = pd.get_dummies(dp, drop_first=True)
                da = pd.DataFrame(columns=feature_cols, data=np.zeros((len(de), len(feature_cols))))
                for c in de.columns:
                    if c in da.columns:
                        da[c] = de[c].values

                smap = {"Canceled":1, "Not_Canceled":0}
                yt = df_ext["booking_status"].map(smap).values
                yp = model.predict(da)
                ypr = model.predict_proba(da)[:,1]

            st.markdown('<hr class="sep">', unsafe_allow_html=True)
            st.markdown("### Hasil Evaluasi")
            st.markdown(
                '<p style="font-size:13px; color:#6080a0 !important; margin-bottom:20px;">'
                'Performa model Random Forest pada data eksternal</p>',
                unsafe_allow_html=True
            )

            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, matthews_corrcoef, confusion_matrix

            acc = accuracy_score(yt, yp)
            pre = precision_score(yt, yp, zero_division=0)
            rec = recall_score(yt, yp, zero_division=0)
            f1v = f1_score(yt, yp, zero_division=0)
            try: aucv = roc_auc_score(yt, ypr)
            except: aucv = 0.0
            mccv = matthews_corrcoef(yt, yp)

            em = {"Accuracy":acc,"Precision":pre,"Recall":rec,"F1-Score":f1v,"AUC":aucv,"MCC":mccv}
            cols = st.columns(6)
            for i, (n, v) in enumerate(em.items()):
                with cols[i]:
                    st.markdown(
                        f'<div class="m-card"><p class="m-label">{n}</p>'
                        f'<p class="m-value">{v:.3f}</p></div>',
                        unsafe_allow_html=True
                    )

            st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

            vc1, vc2 = st.columns(2)

            with vc1:
                cm = confusion_matrix(yt, yp)
                fig_cm = go.Figure(data=go.Heatmap(
                    z=cm, x=["Not Cancel","Cancel"], y=["Not Cancel","Cancel"],
                    colorscale=[[0,'#080d19'],[0.5,'#1e3a8a'],[1,'#3b82f6']],
                    text=cm, texttemplate="%{text:,}",
                    textfont={"size":20,"color":"white","family":"JetBrains Mono"},
                    showscale=False
                ))
                fig_cm = dark_layout(fig_cm, "Confusion Matrix", 420)
                fig_cm.update_layout(xaxis_title="Predicted", yaxis_title="Actual", yaxis=dict(autorange='reversed'))
                st.plotly_chart(fig_cm, use_container_width=True)

            with vc2:
                ro = metrics_df[metrics_df["Model"]=="Random Forest"].iloc[0]
                cn = ["Accuracy","Precision","Recall","F1-Score","AUC"]

                fig_c = go.Figure()
                fig_c.add_trace(go.Bar(
                    name="Test Set Asli", x=cn,
                    y=[ro[m] for m in cn], marker_color='#3b82f6',
                    text=[f"{ro[m]:.3f}" for m in cn],
                    textposition="outside", textfont=dict(color='#7cb8ff', size=12)
                ))
                fig_c.add_trace(go.Bar(
                    name="Data Eksternal", x=cn,
                    y=[em[m] for m in cn], marker_color='#f59e0b',
                    text=[f"{em[m]:.3f}" for m in cn],
                    textposition="outside", textfont=dict(color='#fcd34d', size=12)
                ))
                fig_c = dark_layout(fig_c, "Test Set Asli vs Data Eksternal", 420)
                fig_c.update_layout(barmode='group', yaxis_range=[0,1.18])
                st.plotly_chart(fig_c, use_container_width=True)

            st.markdown("##### Distribusi Probabilitas Prediksi")
            fig_d = go.Figure()
            fig_d.add_trace(go.Histogram(
                x=ypr[yt==0], name="Aktual: Not Cancel",
                marker_color='rgba(34,197,94,0.5)', nbinsx=50, opacity=0.75
            ))
            fig_d.add_trace(go.Histogram(
                x=ypr[yt==1], name="Aktual: Cancel",
                marker_color='rgba(239,68,68,0.5)', nbinsx=50, opacity=0.75
            ))
            fig_d = dark_layout(fig_d, "", 350)
            fig_d.update_layout(barmode='overlay', xaxis_title="Probabilitas Cancel", yaxis_title="Jumlah")
            st.plotly_chart(fig_d, use_container_width=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown('<p class="footer">HotelSight v1.0</p>', unsafe_allow_html=True)