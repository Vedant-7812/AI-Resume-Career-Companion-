# ============================================================
# IMPORTS
# ============================================================

import os
import tempfile

import speech_recognition as sr
import pyttsx3
import sounddevice as sd

from scipy.io.wavfile import write

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


# ============================================================
# ENVIRONMENT / AI MODEL
# ============================================================

# Load variables from .env
load_dotenv()

# Initialize Groq Llama model
model = init_chat_model(
    "groq:llama-3.1-8b-instant"
)


# ============================================================
# CAREER PROFILES
# ============================================================

CAREER_PROFILES = {

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Pandas"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Statistics"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Docker"
    ],

    "AI/ML Engineer": [
        "Python",
        "Mathematics",
        "Statistics",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "NLP",
        "Computer Vision",
        "Docker"
    ],

    "Python Developer": [
        "Python",
        "OOP",
        "SQL",
        "Git",
        "APIs"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "APIs"
    ]
}


# ============================================================
# PROJECT SUGGESTIONS
# ============================================================

PROJECT_SUGGESTIONS = {

    "Data Scientist": [
        "Customer Churn Prediction",
        "House Price Prediction",
        "Sentiment Analysis"
    ],

    "Data Analyst": [
        "Sales Dashboard",
        "Customer Analysis",
        "Business Analytics Dashboard"
    ],

    "Machine Learning Engineer": [
        "Recommendation System",
        "Image Classification",
        "Fraud Detection System"
    ],

    "AI/ML Engineer": [
        "AI Resume Analyzer",
        "Sentiment Analysis using NLP",
        "Image Classification using Deep Learning",
        "AI Chatbot",
        "Recommendation System"
    ],

    "Python Developer": [
        "Expense Tracker",
        "Quiz Application",
        "REST API Project"
    ],

    "Web Developer": [
        "Portfolio Website",
        "E-Commerce Website",
        "Student Management Website"
    ]
}


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

INTERVIEW_QUESTIONS = {

    "Data Scientist": [
        "What is supervised learning?",
        "What is hypothesis testing?",
        "Explain feature selection.",
        "What is cross-validation?",
        "How do you handle missing data?"
    ],

    "Data Analyst": [
        "What is data cleaning?",
        "What is SQL?",
        "What is data visualization?",
        "What is a KPI?",
        "What is an Excel Pivot Table?"
    ],

    "Machine Learning Engineer": [
        "What is overfitting?",
        "What is cross-validation?",
        "Explain feature engineering.",
        "What is deep learning?",
        "What is model deployment?"
    ],

    "AI/ML Engineer": [
        "Explain supervised and unsupervised learning.",
        "What is overfitting and how can you prevent it?",
        "Explain neural networks.",
        "What is the difference between TensorFlow and PyTorch?",
        "How would you deploy a machine learning model?"
    ],

    "Python Developer": [
        "What is OOP?",
        "What are Python decorators?",
        "What is exception handling?",
        "What are Python modules?",
        "What is an API?"
    ],

    "Web Developer": [
        "What is HTML?",
        "What is CSS?",
        "What is JavaScript?",
        "What is an API?",
        "What is responsive web design?"
    ]
}


# ============================================================
# CAREER MATCHING
# ============================================================

def calculate_match(
    user_skills,
    required_skills
):
    """
    Calculate percentage match between
    user's skills and required skills.
    """

    user_skills_lower = {
        skill.lower()
        for skill in user_skills
    }

    required_skills_lower = {
        skill.lower()
        for skill in required_skills
    }

    if not required_skills_lower:
        return 0

    matched_skills = (
        user_skills_lower.intersection(
            required_skills_lower
        )
    )

    percentage = (
        len(matched_skills)
        / len(required_skills_lower)
    ) * 100

    return round(
        percentage,
        2
    )


# ============================================================
# CAREER RECOMMENDATION
# ============================================================

def recommend_careers(
    user_skills
):
    """
    Recommend careers based on
    the user's current skills.
    """

    recommendations = {}

    for career, required_skills in CAREER_PROFILES.items():

        score = calculate_match(
            user_skills,
            required_skills
        )

        recommendations[career] = score

    recommendations = dict(
        sorted(
            recommendations.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return recommendations


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def find_skill_gap(
    user_skills,
    target_role
):
    """
    Find skills missing for target career.
    """

    user_skills_lower = {
        skill.lower()
        for skill in user_skills
    }

    required_skills = CAREER_PROFILES.get(
        target_role,
        []
    )

    missing_skills = []

    for skill in required_skills:

        if skill.lower() not in user_skills_lower:

            missing_skills.append(
                skill
            )

    return missing_skills


# ============================================================
# LEARNING ROADMAP
# ============================================================

def generate_learning_roadmap(
    user_skills,
    target_role
):
    """
    Generate learning roadmap according
    to missing skills and target career.
    """

    missing_skills = find_skill_gap(
        user_skills,
        target_role
    )

    roadmap = []

    for skill in missing_skills:

        roadmap.append(
            f"Learn {skill}"
        )

    roadmap.append(
        "Build practical projects"
    )

    roadmap.append(
        "Practice technical interviews"
    )

    roadmap.append(
        "Improve your resume and LinkedIn profile"
    )

    return roadmap


# ============================================================
# PROJECT SUGGESTIONS
# ============================================================

def suggest_projects(
    target_role
):
    """
    Suggest projects according to target career.
    """

    return PROJECT_SUGGESTIONS.get(
        target_role,
        [
            "Build a practical project related "
            "to your target career."
        ]
    )


# ============================================================
# INTERVIEW PREPARATION
# ============================================================

def get_interview_questions(
    target_role
):
    """
    Return interview questions according
    to target career.
    """

    return INTERVIEW_QUESTIONS.get(
        target_role,
        [
            "Tell me about yourself.",
            "Why are you interested in this career?"
        ]
    )


# ============================================================
# RESUME IMPROVEMENT
# ============================================================

def get_resume_improvement(
    resume_data
):
    """
    Give resume improvement suggestions.

    Member 5 can pass Resume Analyzer
    data to this function.
    """

    suggestions = []

    # Professional summary
    if not resume_data.get(
        "summary"
    ):

        suggestions.append(
            "Add a professional summary."
        )

    # Projects
    if not resume_data.get(
        "projects"
    ):

        suggestions.append(
            "Add relevant projects."
        )

    # Experience
    if not resume_data.get(
        "experience"
    ):

        suggestions.append(
            "Add internship or work experience."
        )

    # Certifications
    if not resume_data.get(
        "certifications"
    ):

        suggestions.append(
            "Add relevant certifications."
        )

    # Skills
    if not resume_data.get(
        "skills"
    ):

        suggestions.append(
            "Add relevant technical skills."
        )

    # If everything exists
    if not suggestions:

        suggestions.append(
            "Your resume looks complete. "
            "Focus on measurable achievements."
        )

    return suggestions


# ============================================================
# RESUME DATA INTEGRATION
# ============================================================

def get_user_profile(
    resume_data
):
    """
    Extract user skills from Resume Analyzer.
    """

    user_skills = resume_data.get(
        "skills",
        []
    )

    return user_skills


# ============================================================
# COMPLETE CAREER ANALYSIS
# ============================================================

def get_career_analysis(
    resume_data,
    target_role=None
):
    """
    Complete Member 4 analysis.
    """

    user_skills = resume_data.get(
        "skills",
        []
    )

    # Career recommendations
    career_recommendations = recommend_careers(
        user_skills
    )

    # Select best career
    if target_role is None:

        if career_recommendations:

            target_role = max(
                career_recommendations,
                key=career_recommendations.get
            )

        else:

            target_role = "Data Scientist"

    # Skill gap
    missing_skills = find_skill_gap(
        user_skills,
        target_role
    )

    # Roadmap
    roadmap = generate_learning_roadmap(
        user_skills,
        target_role
    )

    # Projects
    projects = suggest_projects(
        target_role
    )

    # Interview
    interview_questions = get_interview_questions(
        target_role
    )

    # Resume improvements
    resume_improvements = get_resume_improvement(
        resume_data
    )

    return {

        "user_skills":
            user_skills,

        "career_recommendations":
            career_recommendations,

        "target_role":
            target_role,

        "missing_skills":
            missing_skills,

        "learning_roadmap":
            roadmap,

        "project_suggestions":
            projects,

        "interview_questions":
            interview_questions,

        "resume_improvements":
            resume_improvements
    }


# ============================================================
# VOICE INPUT
# ============================================================

def listen_to_user(
    duration=7
):
    """
    Record user's voice using microphone.
    """

    sample_rate = 16000

    print(
        "\n🎤 Listening... Speak now!"
    )

    temp_audio_path = None

    try:

        # Record audio
        recording = sd.rec(
            int(
                duration
                * sample_rate
            ),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        # Wait until recording finishes
        sd.wait()

        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:

            temp_audio_path = (
                temp_file.name
            )

        # Save recording
        write(
            temp_audio_path,
            sample_rate,
            recording
        )

        # Speech recognition
        recognizer = sr.Recognizer()

        with sr.AudioFile(
            temp_audio_path
        ) as source:

            audio = recognizer.record(
                source
            )

        try:

            text = recognizer.recognize_google(
                audio
            )

            return text.strip()

        except sr.UnknownValueError:

            print(
                "❌ Sorry, I could not understand your voice."
            )

            return ""

        except sr.RequestError:

            print(
                "❌ Speech recognition service "
                "is unavailable."
            )

            return ""

    except Exception as error:

        print(
            f"❌ Microphone error: {error}"
        )

        return ""

    finally:

        # Delete temporary WAV file
        if (
            temp_audio_path
            and os.path.exists(
                temp_audio_path
            )
        ):

            try:

                os.remove(
                    temp_audio_path
                )

            except Exception:
                pass


# ============================================================
# VOICE OUTPUT
# ============================================================

def speak_answer(
    text
):
    """
    Convert AI answer into speech.

    A new speech engine is created for every
    answer to make continuous voice output
    more reliable.
    """

    engine = None

    try:

        # Create a fresh engine
        engine = pyttsx3.init()

        # Speech speed
        engine.setProperty(
            "rate",
            165
        )

        # Maximum volume
        engine.setProperty(
            "volume",
            1.0
        )

        # Speak answer
        engine.say(
            text
        )

        engine.runAndWait()

        # Stop engine
        engine.stop()

    except Exception as error:

        print(
            f"❌ Voice output error: {error}"
        )

    finally:

        # Release engine
        if engine is not None:

            try:
                del engine
            except Exception:
                pass


# ============================================================
# AI CAREER CHATBOT
# ============================================================

def ask_career_ai(
    question,
    user_skills,
    target_role
):
    """
    AI-powered career assistant.

    Handles:
    - Skills
    - Career guidance
    - Projects
    - Resume
    - Interview
    - Learning roadmap
    - AI/ML questions
    """

    user_question = (
        question
        .strip()
        .lower()
    )

    # ========================================================
    # GREETINGS
    # ========================================================

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if user_question in greetings:

        return (
            "Hi! 👋 How can I help you "
            "with your career?"
        )

    # ========================================================
    # PREPARE USER SKILLS
    # ========================================================

    skills_text = ", ".join(
        user_skills
    )

    # ========================================================
    # AI PROMPT
    # ========================================================

    prompt = f"""
You are an AI Career Assistant.

User's Current Skills:
{skills_text}

User's Target Career:
{target_role}

User's Question:
{question}

Your job is to answer the user's actual question.

IMPORTANT RESPONSE RULES:

1. Answer ONLY the question asked.
2. Do not greet the user.
3. Do not introduce yourself.
4. Do not repeat the question.
5. Personalize the answer using the user's skills.
6. Consider the user's target career.
7. Keep the answer medium length.
8. Do not make the answer too short.
9. Do not make the answer unnecessarily long.
10. Normally use 3-5 sentences.
11. If bullets are better, use maximum 5 bullets.
12. Give practical and useful advice.
13. Do not add unrelated information.
14. Do not repeat the same point.
15. Do not create a complete roadmap unless the user asks for one.

SPECIAL INSTRUCTIONS:

If the user asks:
"What skills should I learn?"
Recommend the most useful next skills based on
their current skills and target career.

If the user asks:
"How can I become an AI/ML Engineer?"
Give the most important next steps based on
their current skills.

If the user asks:
"What projects should I build?"
Give 3 useful project ideas relevant to their target career.

If the user asks:
"How can I improve my resume?"
Give the most important resume improvements.

If the user asks:
"How should I prepare for an interview?"
Give practical interview preparation advice.

If the user asks for a learning roadmap:
Give a clear step-by-step roadmap.
Keep it reasonably detailed but not excessively long.

If the user asks about a technical topic:
Explain it clearly at beginner-friendly level
and connect it to their career where useful.

FINAL RULE:
Answer the user's question directly.
Keep the response useful, natural and medium length.
"""

    # ========================================================
    # GET AI RESPONSE
    # ========================================================

    try:

        response = model.invoke(
            prompt
        )

        return response.content.strip()

    except Exception as error:

        return (
            "Sorry, I could not generate a response "
            "right now.\n"
            f"Error: {error}"
        )


# ============================================================
# DISPLAY CAREER ANALYSIS
# ============================================================

def display_career_analysis(
    user_skills,
    target_role
):
    """
    Display Member 4 features in terminal.
    """

    # Career recommendations

    print(
        "\n========== CAREER RECOMMENDATIONS =========="
    )

    recommendations = recommend_careers(
        user_skills
    )

    for career, score in recommendations.items():

        print(
            f"{career}: {score}%"
        )

    # Recommended career

    print(
        "\n========== RECOMMENDED CAREER =========="
    )

    print(
        f"🎯 Recommended Role: {target_role}"
    )

    # Skill gap

    print(
        "\n========== SKILL GAP =========="
    )

    missing_skills = find_skill_gap(
        user_skills,
        target_role
    )

    if missing_skills:

        for skill in missing_skills:

            print(
                f"❌ {skill}"
            )

    else:

        print(
            "✅ No major skill gaps found."
        )

    # Learning roadmap

    print(
        "\n========== LEARNING ROADMAP =========="
    )

    roadmap = generate_learning_roadmap(
        user_skills,
        target_role
    )

    for number, step in enumerate(
        roadmap,
        start=1
    ):

        print(
            f"{number}. {step}"
        )

    # Project suggestions

    print(
        "\n========== PROJECT SUGGESTIONS =========="
    )

    projects = suggest_projects(
        target_role
    )

    for project in projects:

        print(
            f"• {project}"
        )

    # Interview preparation

    print(
        "\n========== INTERVIEW PREPARATION =========="
    )

    questions = get_interview_questions(
        target_role
    )

    for number, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"{number}. {question}"
        )


# ============================================================
# CHATBOT
# ============================================================

def run_chatbot(
    user_skills,
    target_role
):
    """
    Run continuous AI career chatbot.

    Type Mode:
        User can ask multiple questions.

    Voice Mode:
        User can ask multiple questions continuously.

    Exit:
        Type or say exit/quit/bye/close.

    Choice 3:
        Completely exits the chatbot.
    """

    # ========================================================
    # OUTER LOOP
    # ========================================================

    while True:

        print(
            "\n"
            + "=" * 55
        )

        print(
            "        🤖 AI CAREER CHATBOT"
        )

        print(
            "=" * 55
        )

        print(
            "\nChoose how you want to communicate:"
        )

        print(
            "1. ⌨️ Type"
        )

        print(
            "2. 🎤 Voice"
        )

        print(
            "3. ❌ Exit Program"
        )

        # ====================================================
        # ASK CHOICE
        # ====================================================

        while True:

            choice = input(
                "\nEnter choice (1/2/3): "
            ).strip()

            if choice in {
                "1",
                "2",
                "3"
            }:

                break

            print(
                "❌ Please enter 1, 2 or 3."
            )

        # ====================================================
        # EXIT PROGRAM
        # ====================================================

        if choice == "3":

            print(
                "\n👋 Goodbye! See you soon."
            )

            break

        # ====================================================
        # TYPE MODE
        # ====================================================

        if choice == "1":

            print(
                "\n⌨️ Type Mode Started!"
            )

            print(
                "Type 'exit' to stop Type Mode."
            )

            while True:

                question = input(
                    "\n⌨️ You: "
                ).strip()

                # Empty input
                if not question:
                    continue

                # Exit Type Mode
                if question.lower() in {
                    "exit",
                    "quit",
                    "bye",
                    "close"
                }:

                    print(
                        "\n👋 Type chat ended."
                    )

                    break

                # Get AI answer
                answer = ask_career_ai(
                    question,
                    user_skills,
                    target_role
                )

                # Display answer
                print(
                    "\n🤖 AI:"
                )

                print(
                    answer
                )

        # ====================================================
        # VOICE MODE
        # ====================================================

        elif choice == "2":

            print(
                "\n🎤 Voice Mode Started!"
            )

            print(
                "Speak your question."
            )

            print(
                "Say 'exit' to stop Voice Mode."
            )

            # ------------------------------------------------
            # IMPORTANT:
            # This loop keeps Voice Mode active.
            # No input() is used inside this loop.
            # ------------------------------------------------

            while True:

                # --------------------------------------------
                # LISTEN TO USER
                # --------------------------------------------

                question = listen_to_user(
                    duration=7
                )

                # --------------------------------------------
                # IF NOTHING UNDERSTOOD
                # --------------------------------------------

                if not question:

                    print(
                        "⚠️ I couldn't understand."
                    )

                    print(
                        "🎤 Please try again..."
                    )

                    continue

                # --------------------------------------------
                # DISPLAY RECOGNIZED QUESTION
                # --------------------------------------------

                print(
                    f"\n🎤 You: {question}"
                )

                # --------------------------------------------
                # CHECK VOICE EXIT
                # --------------------------------------------

                if question.lower().strip() in {
                    "exit",
                    "quit",
                    "bye",
                    "close"
                }:

                    print(
                        "\n👋 Voice chat ended."
                    )

                    break

                # --------------------------------------------
                # GET AI RESPONSE
                # --------------------------------------------

                answer = ask_career_ai(
                    question,
                    user_skills,
                    target_role
                )

                # --------------------------------------------
                # DISPLAY AI RESPONSE
                # --------------------------------------------

                print(
                    "\n🤖 AI:"
                )

                print(
                    answer
                )

                # --------------------------------------------
                # SPEAK AI RESPONSE
                # --------------------------------------------

                print(
                    "\n🔊 Speaking..."
                )

                speak_answer(
                    answer
                )

                # --------------------------------------------
                # AUTOMATICALLY LISTEN AGAIN
                # --------------------------------------------

                print(
                    "\n🎤 Listening for your next question..."
                )

                # Loop automatically returns to
                # listen_to_user()
                # No typing/input() happens here.


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print(
        "\n"
    )

    print(
        "=" * 60
    )

    print(
        "          🤖 AI CAREER ASSISTANT"
    )

    print(
        "=" * 60
    )

    # ========================================================
    # TEMPORARY TEST USER SKILLS
    # ========================================================

    user_skills = [

        "Python",
        "SQL",
        "Pandas",
        "Machine Learning"
    ]

    # ========================================================
    # FIND BEST CAREER
    # ========================================================

    recommendations = recommend_careers(
        user_skills
    )

    target_role = max(
        recommendations,
        key=recommendations.get
    )

    # ========================================================
    # DISPLAY ALL MEMBER 4 FEATURES
    # ========================================================

    display_career_analysis(
        user_skills,
        target_role
    )

    # ========================================================
    # SAMPLE RESUME DATA
    # ========================================================

    sample_resume_data = {

        "summary": "",

        "projects": [
            "Student Productivity Prediction"
        ],

        "experience": [
            "AI/ML Internship"
        ],

        "certifications": [],

        "skills": user_skills
    }

    print(
        "\n========== RESUME IMPROVEMENT =========="
    )

    improvements = get_resume_improvement(
        sample_resume_data
    )

    for suggestion in improvements:

        print(
            f"• {suggestion}"
        )

    # ========================================================
    # START CHATBOT
    # ========================================================

    run_chatbot(
        user_skills,
        target_role
    )