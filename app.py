import streamlit as st
try:
    import cv2
except:
    cv2 = None
import numpy as np
from predict import predict_burn
from chatbot import get_chatbot_response




st.warning("⚠️ Model disabled (TensorFlow not available in deployment)")



st.set_page_config(page_title="LifeLine AI", page_icon="🔥", layout="centered", initial_sidebar_state="collapsed")

# ── THEME STATE
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── THEME TOGGLE BUTTONS
col_logo, col_right = st.columns([3, 2])
with col_logo:
    st.markdown("""
    <div style="
    font-family:'Syne',sans-serif;
    font-weight:800;
    font-size:22px;
    padding-top:12px;
    display:flex;
    align-items:center;
    gap:8px;
">
    <div style="width:10px;height:10px;background:#ff4e2a;border-radius:50%;animation:pulse 2s infinite;"></div>
    <span style="color:{TEXT} !important;">LifeLine AI</span>
</div>
    """, unsafe_allow_html=True)

with col_right:
    t_col1, t_col2, t_col3 = st.columns([1,1,1])
    with t_col2:
        if st.button("🌙 Dark" if st.session_state.theme == "light" else "☀️ Light"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()


if cv2 is None:
    st.warning("⚠️ OpenCV not loaded. Some features may not work.")


# ── THEME VARIABLES
if st.session_state.theme == "dark":
    BG          = "#07070f"
    BG2         = "rgba(255,255,255,0.03)"
    BG3         = "rgba(255,255,255,0.02)"
    TEXT        = "#f0ece4"
    TEXT_MUTED  = "rgba(240,236,228,0.48)"
    TEXT_DIM    = "rgba(240,236,228,0.3)"
    BORDER      = "rgba(255,255,255,0.07)"
    BORDER2     = "rgba(255,255,255,0.1)"
    INPUT_BG    = "rgba(255,255,255,0.04)"
    CARD_BG     = "rgba(255,255,255,0.03)"
    EMERG_BG    = "rgba(15,5,5,0.85)"
    MAP_BG      = "linear-gradient(135deg,#0a1e3a,#051428)"
    CHAT_BG     = "#0e0e1c"
else:
    BG          = "#f4f4f0"
    BG2         = "rgba(0,0,0,0.03)"
    BG3         = "rgba(0,0,0,0.02)"
    TEXT        = "#1a1a2e"
    TEXT_MUTED  = "rgba(26,26,46,0.55)"
    TEXT_DIM    = "rgba(26,26,46,0.38)"
    BORDER      = "rgba(0,0,0,0.08)"
    BORDER2     = "rgba(0,0,0,0.12)"
    INPUT_BG    = "rgba(0,0,0,0.04)"
    CARD_BG     = "#ffffff"
    EMERG_BG    = "rgba(255,240,240,0.85)"
    MAP_BG      = "linear-gradient(135deg,#dce8ff,#c8daff)"
    CHAT_BG     = "#ffffff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {BG} !important;
    color: {TEXT};
}}
.stApp {{ background: {BG} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 0 !important; max-width: 800px; }}
@keyframes pulse {{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:0.4;transform:scale(0.8)}}}}
.hero-section {{text-align:center;padding:48px 20px 40px;position:relative;overflow:hidden;}}
.hero-glow {{position:absolute;top:-20px;left:50%;transform:translateX(-50%);width:600px;height:320px;background:radial-gradient(ellipse,rgba(255,78,42,0.11) 0%,transparent 68%);pointer-events:none;}}
.hero-eyebrow {{display:inline-block;font-size:11px;font-weight:500;letter-spacing:3px;text-transform:uppercase;color:#ff7a5c;margin-bottom:20px;}}
.hero-title {{font-family:'Syne',sans-serif;font-size:52px;font-weight:800;line-height:1.04;letter-spacing:-2px;margin-bottom:18px;background:linear-gradient(155deg,#ff4e2a 0%,#ff9a7a 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.hero-sub {{font-size:16px;color:{TEXT_MUTED};max-width:420px;margin:0 auto;line-height:1.75;}}
.stats-bar {{display:flex;border:1px solid {BORDER};border-radius:16px;overflow:hidden;margin:32px 0;background:{BG3};}}
.stat-item {{flex:1;padding:18px 12px;text-align:center;border-right:1px solid {BORDER};}}
.stat-item:last-child{{border-right:none;}}
.stat-num {{font-family:'Syne',sans-serif;font-size:24px;font-weight:700;color:#ff7a5c;}}
.stat-label {{font-size:11px;color:{TEXT_DIM};margin-top:4px;}}
.section-eyebrow {{font-size:11px;font-weight:500;letter-spacing:2.5px;text-transform:uppercase;color:{TEXT_DIM};margin-bottom:14px;}}
.result-wrapper {{background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:28px;margin:24px 0;}}
.result-top {{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;}}
.burn-label {{font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:{TEXT};}}
.severity-pill {{padding:7px 18px;border-radius:100px;font-size:12px;font-weight:500;}}
.pill-green {{background:rgba(99,153,34,0.15);color:#97c459;border:1px solid rgba(99,153,34,0.3);}}
.pill-yellow {{background:rgba(186,117,23,0.15);color:#ef9f27;border:1px solid rgba(186,117,23,0.3);}}
.pill-red {{background:rgba(226,75,74,0.15);color:#e24b4a;border:1px solid rgba(226,75,74,0.3);}}
.conf-label {{font-size:12px;color:{TEXT_DIM};margin-bottom:8px;}}
.conf-bar-bg {{height:8px;background:{BORDER};border-radius:100px;overflow:hidden;}}
.conf-pct {{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:#ff7a5c;text-align:right;margin-top:6px;}}
.reco-box {{margin-top:22px;border-radius:14px;padding:18px 22px;}}
.reco-green {{background:rgba(99,153,34,0.07);border:1px solid rgba(99,153,34,0.2);}}
.reco-yellow {{background:rgba(186,117,23,0.07);border:1px solid rgba(186,117,23,0.2);}}
.reco-red {{background:rgba(226,75,74,0.07);border:1px solid rgba(226,75,74,0.2);}}
.reco-title {{font-size:10px;font-weight:500;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;}}
.reco-green .reco-title{{color:#97c459;}}.reco-yellow .reco-title{{color:#ef9f27;}}.reco-red .reco-title{{color:#e24b4a;}}
.reco-text {{font-size:14px;color:{TEXT_MUTED};line-height:1.75;}}
.emergency-section {{background:{EMERG_BG};border:1px solid rgba(226,75,74,0.25);border-radius:20px;padding:28px;margin:36px 0;}}
.emergency-title {{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#e24b4a;margin-bottom:4px;}}
.emergency-sub {{font-size:13px;color:{TEXT_DIM};margin-bottom:24px;}}
.emergency-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px;}}
.emer-btn {{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:22px 10px;border-radius:18px;text-decoration:none;transition:transform 0.18s;}}
.emer-btn:hover {{transform:translateY(-4px);}}
.emer-ambulance {{background:linear-gradient(160deg,rgba(226,75,74,0.18),rgba(160,40,40,0.08));border:1px solid rgba(226,75,74,0.38);}}
.emer-national {{background:linear-gradient(160deg,rgba(55,138,221,0.18),rgba(10,60,130,0.08));border:1px solid rgba(55,138,221,0.38);}}
.emer-fire {{background:linear-gradient(160deg,rgba(239,159,39,0.18),rgba(160,90,10,0.08));border:1px solid rgba(239,159,39,0.38);}}
.emer-icon {{font-size:22px;margin-bottom:10px;}}
.emer-num {{font-family:'Syne',sans-serif;font-size:32px;font-weight:800;margin-bottom:5px;}}
.emer-ambulance .emer-num{{color:#ff6b6b;}}.emer-national .emer-num{{color:#5aabff;}}.emer-fire .emer-num{{color:#ffbe4f;}}
.emer-name {{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:{TEXT_DIM};margin-bottom:8px;}}
.emer-tap {{font-size:10px;padding:3px 10px;border-radius:100px;font-weight:500;}}
.emer-ambulance .emer-tap{{background:rgba(226,75,74,0.15);color:#ff6b6b;}}.emer-national .emer-tap{{background:rgba(55,138,221,0.15);color:#5aabff;}}.emer-fire .emer-tap{{background:rgba(239,159,39,0.15);color:#ffbe4f;}}
.maps-btn-wrap {{border-radius:18px;overflow:hidden;border:1px solid rgba(55,138,221,0.3);background:{MAP_BG};text-decoration:none;display:block;transition:transform 0.18s;}}
.maps-btn-wrap:hover {{transform:translateY(-2px);}}
.maps-btn-inner {{display:flex;align-items:center;gap:18px;padding:20px 24px;}}
.maps-icon-circle {{width:58px;height:58px;border-radius:50%;background:rgba(55,138,221,0.2);border:1px solid rgba(55,138,221,0.4);display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0;}}
.maps-text-wrap {{flex:1;}}
.maps-title {{font-family:'Syne',sans-serif;font-size:17px;font-weight:800;color:{TEXT};margin-bottom:4px;}}
.maps-sub {{font-size:12px;color:{TEXT_MUTED};line-height:1.5;}}
.maps-arrow {{width:36px;height:36px;border-radius:50%;background:rgba(55,138,221,0.18);border:1px solid rgba(55,138,221,0.32);display:flex;align-items:center;justify-content:center;color:#5aabff;font-size:18px;flex-shrink:0;}}
.hiw-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:48px;}}
.hiw-step {{text-align:center;padding:0 8px;}}
.hiw-num {{width:44px;height:44px;border-radius:50%;border:1.5px solid rgba(255,78,42,0.35);display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:700;font-size:16px;color:#ff7a5c;margin:0 auto 14px;background:{BG};}}
.hiw-step h4 {{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;margin-bottom:7px;color:{TEXT};}}
.hiw-step p {{font-size:12px;color:{TEXT_DIM};line-height:1.65;}}
.burn-cards-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:48px;}}
.burn-info-card {{border-radius:16px;padding:22px;background:{CARD_BG};}}
.bic-first{{border:1px solid rgba(99,153,34,0.25);}}.bic-second{{border:1px solid rgba(186,117,23,0.25);}}.bic-third{{border:1px solid rgba(226,75,74,0.25);}}
.bic-dot {{width:10px;height:10px;border-radius:50%;margin-bottom:14px;}}
.bic-first .bic-dot{{background:#97c459;}}.bic-second .bic-dot{{background:#ef9f27;}}.bic-third .bic-dot{{background:#e24b4a;}}
.bic-title {{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;margin-bottom:9px;}}
.bic-first .bic-title{{color:#97c459;}}.bic-second .bic-title{{color:#ef9f27;}}.bic-third .bic-title{{color:#e24b4a;}}
.bic-text {{font-size:12px;color:{TEXT_DIM};line-height:1.7;}}
.disclaimer {{background:rgba(55,138,221,0.05);border:1px solid rgba(55,138,221,0.15);border-radius:12px;padding:14px 20px;font-size:12px;color:{TEXT_DIM};text-align:center;margin-bottom:20px;line-height:1.7;}}
.footer {{text-align:center;padding:24px 0 40px;border-top:1px solid {BORDER};font-size:12px;color:{TEXT_DIM};}}
.footer span {{color:#ff4e2a;}}
.stButton>button {{background:#ff4e2a!important;color:white!important;border:none!important;border-radius:100px!important;font-family:'DM Sans',sans-serif!important;font-weight:500!important;}}
.stButton>button:hover {{opacity:0.82!important;}}
div[data-testid="stFileUploader"] {{background:rgba(255,78,42,0.03)!important;border:1.5px dashed rgba(255,78,42,0.3)!important;border-radius:16px!important;}}


[data-testid="stChatMessage"] {{
    background: {CHAT_BG} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER};
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 10px !important;
}}

[data-testid="stChatMessage"] * {{
    color: {TEXT} !important;
}}

textarea {{
    color: {TEXT} !important;
}}



</style>
""", unsafe_allow_html=True)

# ── HERO
st.markdown("""
<div class="hero-section">
    <div class="hero-glow"></div>
    <div class="hero-eyebrow">AI-Powered Burn Detection</div>
    <div class="hero-title">Know Your Burn.<br>Act Fast. Stay Safe.</div>
    <div class="hero-sub">Upload a photo of the burn. Our AI identifies severity instantly and tells you exactly what to do next.</div>
</div>
""", unsafe_allow_html=True)

# ── STATS
st.markdown("""
<div class="stats-bar">
    <div class="stat-item"><div class="stat-num">10K+</div><div class="stat-label">Images Trained</div></div>
    <div class="stat-item"><div class="stat-num">3</div><div class="stat-label">Burn Classes</div></div>
    <div class="stat-item"><div class="stat-num">~94%</div><div class="stat-label">Model Accuracy</div></div>
    <div class="stat-item"><div class="stat-num">&lt;2s</div><div class="stat-label">Detection Time</div></div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD
st.markdown('<div class="section-eyebrow">📤 Upload Burn Image</div>', unsafe_allow_html=True)
label = None
uploaded_file = st.file_uploader("", type=["jpg","png","jpeg"], label_visibility="collapsed")

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    col_img, _ = st.columns([2,1])
    with col_img:
        st.image(image, caption="Uploaded Image", use_column_width=True)
    with st.spinner("🔍 Analyzing burn severity..."):
        label, confidence = predict_burn(image)
    if "First" in label:
        pill_class, severity_text, reco_class = "pill-green", "Minor Burn", "reco-green"
        reco_msg = "Cool under running water for 10–20 mins. Apply aloe vera gel. Cover loosely with a sterile bandage. Avoid ice directly on skin."
    elif "Second" in label:
        pill_class, severity_text, reco_class = "pill-yellow", "Moderate Burn", "reco-yellow"
        reco_msg = "Do not burst blisters. Clean gently with mild antiseptic. Apply sterile dressing. See a doctor within 24 hours. Call 108 if burn is larger than your palm."
    else:
        pill_class, severity_text, reco_class = "pill-red", "Severe — Call 108 Now", "reco-red"
        reco_msg = "Call 108 immediately. Do not remove burned clothing. Cover with a clean damp cloth. Keep person still and warm. Do NOT apply ice, butter, or toothpaste."
    bar_color = "#97c459" if "First" in label else "#ef9f27" if "Second" in label else "#e24b4a"
    st.markdown(f"""
    <div class="result-wrapper">
        <div class="result-top">
            <div class="burn-label">{label} Burn</div>
            <div class="severity-pill {pill_class}">{severity_text}</div>
        </div>
        <div class="conf-label">Confidence Score</div>
        <div class="conf-bar-bg"><div style="height:100%;width:{confidence:.1f}%;background:{bar_color};border-radius:100px;"></div></div>
        <div class="conf-pct">{confidence:.1f}%</div>
        <div class="reco-box {reco_class}">
            <div class="reco-title">Recommended First Aid</div>
            <div class="reco-text">{reco_msg}</div>
        </div>
    </div>""", unsafe_allow_html=True)
    if confidence < 50:
        st.error("⚠️ Low confidence — please consult a medical professional directly.")
    elif confidence < 70:
        st.warning("⚠️ Moderate confidence — results may need professional verification.")

# ── EMERGENCY
st.markdown("""
<div class="emergency-section">
    <div class="emergency-title">🚨 Emergency Contacts</div>
    <div class="emergency-sub">India helplines — tap any number to call instantly from your phone</div>
    <div class="emergency-grid">
        <a href="tel:108" class="emer-btn emer-ambulance"><div class="emer-icon">🚑</div><div class="emer-num">108</div><div class="emer-name">Ambulance</div><div class="emer-tap">Tap to Call</div></a>
        <a href="tel:112" class="emer-btn emer-national"><div class="emer-icon">🆘</div><div class="emer-num">112</div><div class="emer-name">National Emergency</div><div class="emer-tap">Tap to Call</div></a>
        <a href="tel:101" class="emer-btn emer-fire"><div class="emer-icon">🔥</div><div class="emer-num">101</div><div class="emer-name">Fire Brigade</div><div class="emer-tap">Tap to Call</div></a>
    </div>
    <a href="https://www.google.com/maps/search/burn+hospital+near+me" target="_blank" class="maps-btn-wrap">
        <div class="maps-btn-inner">
            <div class="maps-icon-circle">📍</div>
            <div class="maps-text-wrap">
                <div class="maps-title">Find Nearest Burn Hospital</div>
                <div class="maps-sub">Opens Google Maps · Shows hospitals near your current location</div>
            </div>
            <div class="maps-arrow">→</div>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# ── HOW IT WORKS
st.markdown('<div class="section-eyebrow" style="margin-top:48px;">How It Works</div>', unsafe_allow_html=True)
st.markdown("""
<div class="hiw-grid">
    <div class="hiw-step"><div class="hiw-num">1</div><h4>Upload Photo</h4><p>Take a clear photo in good lighting and upload it.</p></div>
    <div class="hiw-step"><div class="hiw-num">2</div><h4>AI Analyzes</h4><p>EfficientNet classifies burn degree with confidence score.</p></div>
    <div class="hiw-step"><div class="hiw-num">3</div><h4>Get Guidance</h4><p>Receive instant first aid steps and emergency contacts.</p></div>
</div>
""", unsafe_allow_html=True)

# ── BURN GUIDE
st.markdown('<div class="section-eyebrow">Burn Severity Guide</div>', unsafe_allow_html=True)
st.markdown("""
<div class="burn-cards-grid">
    <div class="burn-info-card bic-first"><div class="bic-dot"></div><div class="bic-title">First Degree</div><div class="bic-text">Outer skin only. Redness, minor swelling, mild pain. Heals in 3–5 days without scarring.</div></div>
    <div class="burn-info-card bic-second"><div class="bic-dot"></div><div class="bic-title">Second Degree</div><div class="bic-text">Deeper layers affected. Blisters, intense pain, wet look. Needs medical attention.</div></div>
    <div class="burn-info-card bic-third"><div class="bic-dot"></div><div class="bic-title">Third Degree</div><div class="bic-text">Full thickness. White or charred skin, possible numbness. Emergency care required immediately.</div></div>
</div>
""", unsafe_allow_html=True)

# ── DISCLAIMER + FOOTER
st.markdown("""
<div class="disclaimer">⚕️ LifeLine AI is for informational purposes only. Not a substitute for professional medical advice. In any emergency, call <strong>108</strong> immediately.</div>
<div class="footer">Built with <span>♥</span> for India &nbsp;·&nbsp; LifeLine AI &nbsp;·&nbsp; Not a substitute for medical advice</div>
""", unsafe_allow_html=True)

# ── CHATBOT
st.markdown('<div class="section-eyebrow" style="margin-top:32px;">🤖 LifeLine Assistant</div>', unsafe_allow_html=True)
st.caption("Ask anything about burns, first aid, or when to go to hospital")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm LifeLine Assistant 👋 Ask me anything about burns, first aid, or when to go to hospital."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask about burn treatment..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("Thinking..."):
        if uploaded_file is not None and label is not None:
            response = get_chatbot_response(f"My burn type is {label}. {prompt}")
        else:
            response = get_chatbot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
