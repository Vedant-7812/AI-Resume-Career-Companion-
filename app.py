import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="CareerAI - UI Layout",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerAI - Smart Career Assistant & Resume Analyzer")

# ============================================================
# MAIN TABS INTERFACE
# ============================================================
tabs = st.tabs([
    "📄 Resume Analyzer & Job Matcher",
    "🤖 AI Career Chatbot",
    "🎯 Career Pathways & Roadmaps",
    "📊 Candidate Database"
])

# ------------------------------------------------------------
# TAB 1: RESUME ANALYZER & JOB MATCHER
# ------------------------------------------------------------
with tabs[0]:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Candidate Details")
        st.file_uploader("Upload Resume (PDF / DOCX)", type=["pdf", "docx"])
        st.number_input("Years of Experience", min_value=0.0, max_value=40.0, value=1.0, step=0.5)

    with col2:
        st.subheader("Job Description")
        st.text_area("Paste Job Description here...", height=170, placeholder="Enter the target job posting details...")

    st.button("Analyze Resume & Match Job", type="primary")

    st.divider()

    # Results Section Layout (Placeholders)
    st.subheader("Analysis Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Resume Completeness", "0%")
    m2.metric("Skill Match", "0%")
    m3.metric("Experience Score", "0%")
    m4.metric("Overall Match", "0%")

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("#### Candidate Profile")
        st.write("**Name:** —")
        st.write("**Email:** —")
        st.write("**Detected Skills:** —")

    with res_col2:
        st.markdown("#### Skill Gap Analysis")
        st.write("**Matching Skills:** —")
        st.write("**Missing Skills:** —")

# ------------------------------------------------------------
# TAB 2: AI CAREER CHATBOT
# ------------------------------------------------------------
with tabs[1]:
    st.subheader("💬 AI Career Advisor")

    with st.expander("⚙️ Assistant Settings", expanded=False):
        role_list = ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "AI/ML Engineer", "Python Developer", "Web Developer"]
        st.selectbox("Target Role for Advice", role_list)

    # Chat history layout
    with st.chat_message("assistant"):
        st.markdown("Hello! I am your AI Career Advisor. Ask me anything about skill gaps, project ideas, or interview questions.")

    st.chat_input("Type your question here...")

# ------------------------------------------------------------
# TAB 3: CAREER PATHWAYS & ROADMAPS
# ------------------------------------------------------------
with tabs[2]:
    st.subheader("🎯 Career Pathways & Skill Requirements")
    selected_role = st.selectbox("Explore Target Role", ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "AI/ML Engineer", "Python Developer", "Web Developer"], key="pathway_role")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🗺️ Learning Roadmap")
        st.markdown("- Step 1: Core Fundamentals")
        st.markdown("- Step 2: Advanced Topics")
        st.markdown("- Step 3: Practical Projects")

        st.markdown("#### 💡 Recommended Projects")
        st.markdown("- Project Idea 1")
        st.markdown("- Project Idea 2")

    with c2:
        st.markdown("#### ❓ Key Interview Questions")
        st.markdown("- Question 1")
        st.markdown("- Question 2")

# ------------------------------------------------------------
# TAB 4: CANDIDATE DATABASE
# ------------------------------------------------------------
with tabs[3]:
    st.subheader("📊 Stored Candidates")
    st.info("No candidates recorded in the table yet.")
