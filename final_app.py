import io
import re
import os
import sqlite3
import tempfile
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# PAGE CONFIGURATION (MUST BE VERY FIRST STREAMLIT CALL)
# ============================================================
st.set_page_config(
    page_title="CareerAI - Smart Career Assistant",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# SAFE OPTIONAL IMPORTS
# ============================================================
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from langchain.chat_models import init_chat_model
except ImportError:
    init_chat_model = None

try:
    import sounddevice as sd
    from scipy.io.wavfile import write
    import speech_recognition as sr
except Exception:
    sd = None
    write = None
    sr = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


# ============================================================
# DATABASE SETUP
# ============================================================
DB_NAME = "careerai.db"

def create_database():
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                skills TEXT,
                experience TEXT,
                education TEXT,
                skill_score REAL,
                experience_score REAL,
                match_score REAL,
                missing_skills TEXT,
                status TEXT,
                notes TEXT,
                resume TEXT
            )
        """)
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Database error: {e}")

def save_candidate(candidate):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO candidates (
            name, email, skills, experience, education,
            skill_score, experience_score, match_score,
            missing_skills, status, notes, resume
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate["Name"],
        candidate["Email"],
        candidate["Skills"],
        candidate["Experience"],
        candidate["Education"],
        candidate["Skill Score"],
        candidate["Experience Score"],
        candidate["Match Score"],
        candidate["Missing Skills"],
        candidate["Status"],
        candidate["Notes"],
        candidate["Resume"]
    ))
    connection.commit()
    connection.close()

def get_candidates():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY match_score DESC")
    data = cursor.fetchall()
    connection.close()
    return data

create_database()


# ============================================================
# RESUME ANALYZER ENGINE
# ============================================================
SKILLS = [
    "Python", "SQL", "Java", "C++", "C#", "JavaScript", "TypeScript",
    "HTML", "CSS", "React", "Node.js", "Pandas", "NumPy", "Matplotlib",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "Scikit-learn", "AWS", "Azure", "Docker", "Kubernetes", "Git",
    "Excel", "Power BI", "MongoDB", "MySQL", "PostgreSQL", "NLP",
    "Computer Vision", "Flask", "Django"
]

SECTION_ALIASES = {
    "education": ["education", "academic background", "qualifications", "educational background"],
    "projects": ["projects", "academic projects", "personal projects", "project"],
    "experience": ["experience", "work experience", "professional experience", "internship", "work history"],
    "certifications": ["certifications", "certificates", "courses", "licenses"],
    "summary": ["summary", "professional summary", "career summary", "objective", "profile", "about me"]
}

def clean_line(line):
    line = line.replace("\u00a0", " ")
    line = re.sub(r"\s+", " ", line)
    return line.strip()

def extract_resume_text(uploaded_file):
    data = uploaded_file.getvalue()
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        if fitz is None:
            raise ImportError("PyMuPDF is not installed. Run: `pip install pymupdf`")
        document = fitz.open(stream=data, filetype="pdf")
        pages = [page.get_text("text", sort=True) for page in document]
        document.close()
        text = "\n".join(pages).strip()
        if not text:
            raise ValueError("No readable text found in this PDF.")
        return text

    if filename.endswith(".docx"):
        if Document is None:
            raise ImportError("python-docx is not installed. Run: `pip install python-docx`")
        document = Document(io.BytesIO(data))
        paragraphs = [clean_line(p.text) for p in document.paragraphs if clean_line(p.text)]
        text = "\n".join(paragraphs).strip()
        if not text:
            raise ValueError("No text found in this DOCX file.")
        return text

    raise ValueError("Only PDF and DOCX files are supported.")

def find_name(text):
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    ignored = ["resume", "curriculum vitae", "email", "phone", "mobile", "linkedin", "github"]
    for line in lines[:10]:
        lower_line = line.lower()
        if len(line.split()) <= 6 and "@" not in line and not any(w in lower_line for w in ignored):
            return line
    return "Unknown"

def find_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else "Not found"

def find_skills(text):
    found = []
    lower_text = text.lower()
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, lower_text):
            found.append(skill)
    return found

def normalize_heading(line):
    line = clean_line(line).lower()
    line = re.sub(r"^[^a-zA-Z]+", "", line)
    line = re.sub(r"[:\-|]+$", "", line)
    return line.strip()

def find_section(text, section_name):
    lines = text.splitlines()
    wanted = SECTION_ALIASES.get(section_name, [section_name])
    all_headings = [alias for aliases in SECTION_ALIASES.values() for alias in aliases]
    result, collecting = [], False

    for raw_line in lines:
        line = clean_line(raw_line)
        if not line:
            continue
        heading = normalize_heading(line)
        if heading in wanted:
            collecting = True
            continue
        if collecting and heading in all_headings:
            break
        if collecting:
            result.append(line)
    return result

def calculate_resume_score(data):
    score = 0
    if data["name"] != "Unknown": score += 10
    if data["email"] != "Not found": score += 5
    if data["skills"]: score += 20
    if data["education"]: score += 20
    if data["projects"]: score += 20
    if data["experience"]: score += 15
    if data["certifications"]: score += 5
    if data["summary"]: score += 5
    return min(score, 100)

def get_missing_items(data):
    missing = []
    if data["email"] == "Not found": missing.append("Email")
    if not data["summary"]: missing.append("Professional Summary")
    if not data["education"]: missing.append("Education")
    if not data["projects"]: missing.append("Projects")
    if not data["experience"]: missing.append("Experience or Internship")
    if not data["certifications"]: missing.append("Certifications")
    if not data["skills"]: missing.append("Technical Skills")
    return missing

def analyze_resume(uploaded_file):
    text = extract_resume_text(uploaded_file)
    data = {
        "name": find_name(text),
        "email": find_email(text),
        "skills": find_skills(text),
        "education": find_section(text, "education"),
        "projects": find_section(text, "projects"),
        "experience": find_section(text, "experience"),
        "certifications": find_section(text, "certifications"),
        "summary": find_section(text, "summary"),
        "raw_text": text
    }
    data["resume_score"] = calculate_resume_score(data)
    data["missing_items"] = get_missing_items(data)
    return data


# ============================================================
# JOB MATCHER ENGINE
# ============================================================
SKILL_ALIASES = {
    "python": "Python", "java": "Java", "c++": "C++", "javascript": "JavaScript",
    "js": "JavaScript", "typescript": "TypeScript", "machine learning": "Machine Learning",
    "ml": "Machine Learning", "deep learning": "Deep Learning", "dl": "Deep Learning",
    "artificial intelligence": "Artificial Intelligence", "ai": "Artificial Intelligence",
    "nlp": "NLP", "natural language processing": "NLP", "tensorflow": "TensorFlow",
    "pytorch": "PyTorch", "scikit-learn": "Scikit-learn", "pandas": "Pandas",
    "numpy": "NumPy", "sql": "SQL", "mysql": "MySQL", "postgresql": "PostgreSQL",
    "mongodb": "MongoDB", "docker": "Docker", "kubernetes": "Kubernetes", "git": "Git",
    "aws": "AWS", "azure": "Azure", "power bi": "Power BI", "excel": "Excel"
}

def normalize_skill(skill):
    if not isinstance(skill, str): return None
    return SKILL_ALIASES.get(skill.strip().lower(), skill.strip().title())

def normalize_skills(skills):
    return sorted({normalize_skill(s) for s in (skills or []) if normalize_skill(s)})

def extract_job_skills(job_description):
    if not job_description: return []
    text = job_description.lower()
    found = set()
    for alias in sorted(SKILL_ALIASES.keys(), key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        if re.search(pattern, text):
            found.add(SKILL_ALIASES[alias])
    return sorted(found)

def analyze_job_match(resume_data, job_description):
    resume_skills = normalize_skills(resume_data.get("skills", []))
    job_skills = extract_job_skills(job_description)
    resume_set, job_set = set(resume_skills), set(job_skills)
    matching = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    score = round((len(matching) / len(job_skills) * 100)) if job_skills else 0
    return {
        "match_score": score,
        "matching_skills": matching,
        "missing_skills": missing
    }

def calculate_experience_score(experience):
    try:
        years = float(re.findall(r"\d+(?:\.\d+)?", str(experience))[0]) if re.findall(r"\d+(?:\.\d+)?", str(experience)) else float(experience)
    except Exception:
        years = 0
    return round(min(years / 5 * 100, 100))


# ============================================================
# CAREER ASSISTANT & CHAT ENGINE
# ============================================================
CAREER_PROFILES = {
    "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas"],
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI", "Statistics"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "Docker"],
    "AI/ML Engineer": ["Python", "Mathematics", "Statistics", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Docker"],
    "Python Developer": ["Python", "OOP", "SQL", "Git", "APIs"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "Git", "APIs"]
}

PROJECT_SUGGESTIONS = {
    "Data Scientist": ["Customer Churn Prediction", "House Price Prediction", "Sentiment Analysis"],
    "Data Analyst": ["Sales Dashboard", "Customer Analytics", "Business Analytics Dashboard"],
    "Machine Learning Engineer": ["Recommendation System", "Image Classification", "Fraud Detection System"],
    "AI/ML Engineer": ["AI Resume Analyzer", "Sentiment Analysis using NLP", "RAG-based AI Chatbot"],
    "Python Developer": ["Expense Tracker API", "Quiz Application", "RESTful CRUD Backend"],
    "Web Developer": ["Interactive Portfolio", "E-Commerce Web Application", "Task Management Portal"]
}

INTERVIEW_QUESTIONS = {
    "Data Scientist": ["What is supervised vs unsupervised learning?", "Explain cross-validation.", "How do you handle missing data?"],
    "Data Analyst": ["What is data cleaning?", "Explain SQL JOINs.", "What is a KPI Dashboard?"],
    "Machine Learning Engineer": ["What is overfitting and how do you prevent it?", "Explain gradient descent.", "How do you deploy models?"],
    "AI/ML Engineer": ["Explain transformer architectures.", "TensorFlow vs PyTorch trade-offs?", "How do you optimize LLM latency?"],
    "Python Developer": ["Explain decorators and generators.", "How does Python garbage collection work?", "What is REST API design?"],
    "Web Developer": ["What is the CSS Box Model?", "Explain asynchronous JavaScript (Promises/Async-Await).", "What is responsive web design?"]
}

def find_skill_gap(user_skills, target_role):
    user_skills_lower = {s.lower() for s in user_skills}
    required = CAREER_PROFILES.get(target_role, [])
    return [skill for skill in required if skill.lower() not in user_skills_lower]

def ask_career_ai(question, user_skills, target_role):
    # Rule-based fast greeting
    if question.strip().lower() in {"hi", "hello", "hey", "hii"}:
        return "Hi! 👋 How can I help you with your career path, skills, or interview preparation today?"

    # Attempt LangChain / Groq inference safely
    api_key = os.getenv("GROQ_API_KEY")
    if init_chat_model and api_key:
        try:
            model = init_chat_model("groq:llama-3.1-8b-instant", api_key=api_key)
            prompt = (
                f"You are an expert AI Career Assistant.\n"
                f"User's Skills: {', '.join(user_skills) if user_skills else 'None'}\n"
                f"Target Role: {target_role}\n"
                f"Question: {question}\n\n"
                f"Rules: Answer concisely in 3-5 sentences or up to 4 action-oriented bullets. No robotic greetings."
            )
            response = model.invoke(prompt)
            return response.content
        except Exception:
            pass

    # Built-in offline fallback if API/Keys are not ready
    missing = find_skill_gap(user_skills, target_role)
    return (
        f"**Advice for {target_role}:**\n"
        f"- **Current Skills:** {', '.join(user_skills) if user_skills else 'None detected'}\n"
        f"- **Missing Core Skills:** {', '.join(missing) if missing else 'All core skills acquired!'}\n"
        f"- **Recommended Projects:** {', '.join(PROJECT_SUGGESTIONS.get(target_role, [])[:2])}"
    )


# ============================================================
# STREAMLIT UI
# ============================================================
if "user_skills" not in st.session_state:
    st.session_state.user_skills = ["Python", "SQL"]
if "target_role" not in st.session_state:
    st.session_state.target_role = "Data Scientist"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your AI Career Advisor. Ask me anything about skill gaps, project ideas, or interview questions."}
    ]

st.title("🚀 CareerAI - Smart Resume Analyzer & Career Assistant")

tabs = st.tabs([
    "📄 Resume Analyzer & Job Matcher",
    "🤖 AI Career Chatbot",
    "🎯 Career Pathways & Roadmaps",
    "📊 Database"
])

# TAB 1
with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader("Upload PDF / DOCX", type=["pdf", "docx"])
        exp_input = st.number_input("Years of Experience", 0.0, 40.0, 1.0, 0.5)

    with c2:
        st.subheader("Job Description")
        job_desc = st.text_area("Paste Job Requirements...", height=150)

    if uploaded_file and st.button("Analyze Resume", type="primary"):
        try:
            with st.spinner("Processing..."):
                parsed = analyze_resume(uploaded_file)
                match = analyze_job_match(parsed, job_desc)
                exp_score = calculate_experience_score(exp_input)
                final_score = round(match["match_score"] * 0.8 + exp_score * 0.2)

                if parsed["skills"]:
                    st.session_state.user_skills = parsed["skills"]

            st.divider()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Resume Completeness", f"{parsed['resume_score']}%")
            m2.metric("Skill Match", f"{match['match_score']}%")
            m3.metric("Experience Score", f"{exp_score}%")
            m4.metric("Total Score", f"{final_score}%")

            st.write(f"**Identified Name:** {parsed['name']} | **Email:** {parsed['email']}")
            st.write(f"**Skills Detected:** {', '.join(parsed['skills']) if parsed['skills'] else 'None'}")

            save_candidate({
                "Name": parsed["name"], "Email": parsed["email"],
                "Skills": ", ".join(parsed["skills"]), "Experience": f"{exp_input} yrs",
                "Education": "\n".join(parsed["education"]), "Skill Score": match["match_score"],
                "Experience Score": exp_score, "Match Score": final_score,
                "Missing Skills": ", ".join(match["missing_skills"]),
                "Status": "Reviewed", "Notes": "Web Submission", "Resume": parsed["raw_text"][:500]
            })
            st.success("Resume processed and saved to database!")
        except Exception as err:
            st.error(f"Error parsing resume: {err}")

# TAB 2
with tabs[1]:
    st.subheader("💬 AI Career Advisor")
    
    with st.expander("⚙️ Current Context", expanded=False):
        st.session_state.target_role = st.selectbox("Target Role", list(CAREER_PROFILES.keys()))
        st.write(f"**Active Skills:** {', '.join(st.session_state.user_skills)}")

    # Render History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if user_input := st.chat_input("Ask a question about your career, interview prep, or skills..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            reply = ask_career_ai(user_input, st.session_state.user_skills, st.session_state.target_role)
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# TAB 3
with tabs[2]:
    st.subheader("🎯 Career Pathways & Preparation")
    role_choice = st.selectbox("Select Role to Inspect", list(CAREER_PROFILES.keys()), key="role_inspect")
    missing_items = find_skill_gap(st.session_state.user_skills, role_choice)

    st.write(f"**Required Skills:** {', '.join(CAREER_PROFILES[role_choice])}")
    st.write(f"**Missing Skills for You:** {', '.join(missing_items) if missing_items else 'None! You meet all core requirements.'}")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 💡 Recommended Projects")
        for proj in PROJECT_SUGGESTIONS.get(role_choice, []):
            st.markdown(f"- {proj}")
    with col_r:
        st.markdown("#### ❓ Typical Interview Questions")
        for q in INTERVIEW_QUESTIONS.get(role_choice, []):
            st.markdown(f"- {q}")

# TAB 4
with tabs[3]:
    st.subheader("📊 Candidate Database")
    records = get_candidates()
    if records:
        cols = ["ID", "Name", "Email", "Skills", "Exp", "Edu", "Skill Score", "Exp Score", "Match Score", "Missing Skills", "Status", "Notes", "Resume"]
        df = pd.DataFrame(records, columns=cols)
        st.dataframe(df[["ID", "Name", "Email", "Match Score", "Status", "Skills", "Missing Skills"]], use_container_width=True)
    else:
        st.info("No candidate records found in the database yet. Upload resumes to populate the database.")