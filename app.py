import streamlit as st

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="CareerAI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

/* =========================================================
   MAIN BACKGROUND
   ========================================================= */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.13), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(124,58,237,0.12), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(37,99,235,0.10), transparent 30%),
        linear-gradient(135deg, #f8faff 0%, #eef3ff 50%, #faf8ff 100%);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 0;
    max-width: 1400px;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 50% 0%, rgba(99,102,241,0.20), transparent 35%),
        linear-gradient(180deg, #0b1020 0%, #111827 45%, #0b1020 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
    box-shadow: 8px 0 35px rgba(15,23,42,0.15);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.3rem;
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}

/* =========================================================
   LOGO
   ========================================================= */

.logo-box {
    text-align: center;
    padding: 12px 5px 22px 5px;
}

.logo-icon {
    font-size: 50px;
    margin-bottom: 4px;
    filter: drop-shadow(0 0 15px rgba(129,140,248,0.65));
    animation: floatLogo 3s ease-in-out infinite;
}

@keyframes floatLogo {

    0%, 100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-5px);
    }

}

.logo-title {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: 1px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #c7d2fe,
        #a5b4fc
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-subtitle {
    font-size: 13px;
    color: #a5b4fc !important;
    margin-top: 5px;
}

/* =========================================================
   DIVIDER
   ========================================================= */

.divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(148,163,184,0.25),
        transparent
    );
    margin: 5px 0 20px 0;
}

/* =========================================================
   NAVIGATION
   ========================================================= */

.nav-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #94a3b8 !important;
    margin-bottom: 10px;
}

[data-testid="stSidebar"] .stRadio > label {
    color: #cbd5e1 !important;
    font-weight: 600;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 5px;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    border-radius: 12px;
    padding: 10px 12px;
    margin: 2px 0;
    border: 1px solid transparent;
    transition: all 0.25s ease;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: linear-gradient(
        90deg,
        rgba(99,102,241,0.25),
        rgba(124,58,237,0.12)
    );

    border: 1px solid rgba(129,140,248,0.20);

    transform: translateX(5px);
}

[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #818cf8;
}

/* =========================================================
   PROJECT CARD
   ========================================================= */

.project-card {
    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.16),
            rgba(124,58,237,0.08)
        );

    border: 1px solid rgba(129,140,248,0.22);

    padding: 16px;

    border-radius: 16px;

    margin-top: 10px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.15),
        inset 0 1px 0 rgba(255,255,255,0.05);

    transition: all 0.25s ease;
}

.project-card:hover {
    transform: translateY(-3px);

    border-color: rgba(129,140,248,0.4);

    box-shadow:
        0 15px 35px rgba(79,70,229,0.18);
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 55px 30px 35px 30px;
    text-align: center;
    position: relative;
}

.hero::before {
    content: "";

    position: absolute;

    width: 300px;
    height: 300px;

    background: rgba(99,102,241,0.12);

    filter: blur(90px);

    border-radius: 50%;

    top: 20px;
    left: 50%;

    transform: translateX(-50%);

    z-index: -1;
}

.hero-icon {
    font-size: 70px;
    margin-bottom: 8px;

    filter: drop-shadow(
        0 8px 20px rgba(79,70,229,0.25)
    );

    animation: rocketFloat 3s ease-in-out infinite;
}

@keyframes rocketFloat {

    0%, 100% {
        transform: translateY(0) rotate(-2deg);
    }

    50% {
        transform: translateY(-9px) rotate(2deg);
    }

}

.hero-title {
    font-size: 58px;
    font-weight: 900;
    letter-spacing: -1px;

    background: linear-gradient(
        90deg,
        #4338ca,
        #7c3aed,
        #2563eb,
        #4f46e5
    );

    background-size: 250% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: gradientMove 5s linear infinite;

    margin-bottom: 12px;
}

@keyframes gradientMove {

    0% {
        background-position: 0% center;
    }

    100% {
        background-position: 250% center;
    }

}

.hero-subtitle {
    font-size: 19px;

    color: #64748b;

    max-width: 720px;

    margin: auto;

    line-height: 1.7;
}

/* =========================================================
   FEATURE CONTAINER
   ========================================================= */

.feature-container {
    display: flex;

    gap: 22px;

    justify-content: center;

    margin: 25px auto 0 auto;

    max-width: 1000px;
}

/* =========================================================
   FEATURE CARDS
   ========================================================= */

.feature-card {

    width: 220px;

    min-height: 190px;

    padding: 28px 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.90),
            rgba(255,255,255,0.62)
        );

    backdrop-filter: blur(18px);

    -webkit-backdrop-filter: blur(18px);

    border: 1px solid rgba(148,163,184,0.22);

    border-radius: 22px;

    text-align: center;

    box-shadow:
        0 12px 35px rgba(15,23,42,0.07),
        inset 0 1px 0 rgba(255,255,255,0.8);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;

    position: relative;

    overflow: hidden;
}

.feature-card::before {

    content: "";

    position: absolute;

    top: 0;

    left: -100%;

    width: 100%;

    height: 2px;

    background: linear-gradient(
        90deg,
        transparent,
        #6366f1,
        #8b5cf6,
        transparent
    );

    transition: left 0.5s ease;
}

.feature-card:hover::before {
    left: 100%;
}

.feature-card:hover {

    transform: translateY(-9px) scale(1.02);

    border-color: rgba(99,102,241,0.30);

    box-shadow:
        0 20px 45px rgba(79,70,229,0.14),
        0 0 25px rgba(99,102,241,0.06);
}

/* =========================================================
   FEATURE ICON
   ========================================================= */

.feature-icon {

    font-size: 40px;

    margin-bottom: 13px;

    filter: drop-shadow(
        0 5px 10px rgba(79,70,229,0.15)
    );

    transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {

    transform:
        scale(1.15)
        translateY(-3px);
}

/* =========================================================
   FEATURE TEXT
   ========================================================= */

.feature-title {

    font-weight: 800;

    font-size: 17px;

    color: #1e293b;
}

.feature-text {

    font-size: 13px;

    color: #64748b;

    margin-top: 7px;

    line-height: 1.5;
}

/* =========================================================
   SELECTED PAGE
   ========================================================= */

.selected-page {

    text-align: center;

    margin: 38px auto 0 auto;

    padding: 12px 22px;

    width: fit-content;

    color: #64748b;

    font-size: 14px;

    background: rgba(255,255,255,0.55);

    border: 1px solid rgba(148,163,184,0.18);

    border-radius: 30px;

    backdrop-filter: blur(10px);

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);
}

.selected-page b {
    color: #4f46e5;
}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align: center;

    color: #94a3b8;

    font-size: 13px;

    margin-top: 60px;

    padding: 18px 0 25px 0;
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .hero-title {
        font-size: 45px;
    }

    .hero-subtitle {
        font-size: 17px;
    }

    .feature-container {
        flex-wrap: wrap;
    }

    .feature-card {
        width: 45%;
    }

}

@media (max-width: 600px) {

    .hero {
        padding-top: 35px;
    }

    .hero-icon {
        font-size: 55px;
    }

    .hero-title {
        font-size: 38px;
    }

    .feature-container {
        flex-direction: column;
        align-items: center;
    }

    .feature-card {
        width: 90%;
    }

}

</style>
""", unsafe_allow_html=True)


# SIDEBAR


st.sidebar.markdown("""
<div class="logo-box">
<div class="logo-icon">🚀</div>
<div class="logo-title">CareerAI</div>
<div class="logo-subtitle">Your AI Career Companion</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    '<div class="divider"></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="nav-label">MAIN MENU</div>',
    unsafe_allow_html=True
)

# NAVIGATION


page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 My Profile",
        "📄 Resume Analyzer",
        "🎯 Job Matcher",
        "📊 Skill Analytics",
        "🗺️ Career Roadmap",
        "🤖 AI Career Assistant",
        "🎤 Mock Interview",
        "📚 Job Explorer",
        "🧑‍💼 Recruiter Dashboard",
        "📈 My Progress"
    ],
    label_visibility="collapsed"
)


# SIDEBAR BOTTOM


st.sidebar.markdown(
    '<div class="divider"></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("""
<div class="project-card">

<div style="
font-size:11px;
font-weight:700;
letter-spacing:1.5px;
color:#94a3b8;
">
CURRENT PROJECT
</div>

<div style="
font-size:16px;
font-weight:700;
margin-top:7px;
">
🚀 Hackathon Edition
</div>

<div style="
font-size:12px;
color:#94a3b8;
margin-top:6px;
">
AI-powered career platform
</div>

</div>
""", unsafe_allow_html=True)


# MAIN SCREEN


st.markdown("""
<div class="hero">
<div class="hero-icon">🚀</div>

<div class="hero-title">CareerAI</div>

<div class="hero-subtitle">
An intelligent career companion that helps students
build better resumes, discover opportunities,
improve their skills and prepare for interviews.
</div>

</div>
""", unsafe_allow_html=True)


# FEATURE PREVIEW


st.markdown("""
<div class="feature-container">

<div class="feature-card">

<div class="feature-icon">📄</div>

<div class="feature-title">
Smart Resume
</div>

<div class="feature-text">
Analyze and improve your resume
</div>

</div>


<div class="feature-card">

<div class="feature-icon">🎯</div>

<div class="feature-title">
Job Matching
</div>

<div class="feature-text">
Find jobs that match your skills
</div>

</div>


<div class="feature-card">

<div class="feature-icon">🗺️</div>

<div class="feature-title">
Career Roadmap
</div>

<div class="feature-text">
Know what skills to learn next
</div>

</div>


<div class="feature-card">

<div class="feature-icon">🤖</div>

<div class="feature-title">
AI Assistant
</div>

<div class="feature-text">
Get personalized career guidance
</div>

</div>

</div>
""", unsafe_allow_html=True)

# SELECTED PAGE MESSAGE


st.markdown(
f"""
<div class="selected-page">
Selected: <b>{page}</b>
</div>
""",
unsafe_allow_html=True
)


# FOOTER

st.markdown("""
<div class="footer">
🚀 CareerAI &nbsp;•&nbsp;
AI Resume & Career Companion &nbsp;•&nbsp;
Hackathon Edition
</div>
""", unsafe_allow_html=True)