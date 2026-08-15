import streamlit as st
import pandas as pd

from resume_extractor import extract_text_from_pdf
from candidate_parser import extract_candidate_info
from modules import job_matcher
from database import create_database, save_candidate, get_candidates


def extract_required_skills(job_description: str):
	return job_matcher.extract_job_skills(job_description)


def calculate_match_score(resume_skills, required_skills):
	if not required_skills:
		return 0

	resume_set = set([s.lower() for s in resume_skills])
	req_set = set([s.lower() for s in required_skills])
	matching = resume_set & req_set
	score = (len(matching) / len(req_set)) * 100
	return round(score)


def find_missing_skills(resume_skills, required_skills):
	resume_set = set([s.lower() for s in resume_skills])
	missing = [s for s in required_skills if s.lower() not in resume_set]
	return missing


def calculate_experience_score(years):
	try:
		y = float(years)
	except Exception:
		return 0

	if y <= 0:
		return 0
	if y >= 5:
		return 100
	return round((y / 5) * 100)


def calculate_final_score(skill_score, experience_score, skill_weight=0.7):
	return round(skill_score * skill_weight + experience_score * (1 - skill_weight))


create_database()

st.set_page_config(page_title="Recruiter Dashboard", page_icon="👨‍💼", layout="wide")

st.title("👨‍💼 Recruiter Dashboard")
st.write("AI-powered candidate screening and ranking")

st.sidebar.header("Recruiter")

job_title = st.sidebar.text_input("Job Title", "Machine Learning Engineer")

job_description = st.text_area(
	"Job Description",
	"Looking for a Machine Learning Engineer with Python, SQL, Machine Learning, Pandas, NumPy and AWS skills."
)

required_skills = extract_required_skills(job_description)

st.write("### 🎯 Required Skills")

if required_skills:
	st.write(", ".join(required_skills))
else:
	st.write("No required skills detected")

st.divider()

st.subheader("📄 Upload Candidate Resumes")

uploaded_files = st.file_uploader("Upload multiple PDF resumes", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
	st.success(f"{len(uploaded_files)} resumes uploaded successfully!")

	candidate_data = []
	st.subheader("👥 Candidates")

	for file in uploaded_files:
		text = extract_text_from_pdf(file)
		candidate_info = extract_candidate_info(text)

		match_score = calculate_match_score(candidate_info.get("Skills", []), required_skills)
		missing_skills = find_missing_skills(candidate_info.get("Skills", []), required_skills)
		experience_score = calculate_experience_score(candidate_info.get("Experience", 0))
		final_score = calculate_final_score(match_score, experience_score)

		candidate_data.append({
			"Name": candidate_info.get("Name", "Not Found"),
			"Email": candidate_info.get("Email", "Not Found"),
			"Skills": ", ".join(candidate_info.get("Skills", [])),
			"Experience": candidate_info.get("Experience", 0),
			"Education": ", ".join(candidate_info.get("Education", [])),
			"Skill Score": match_score,
			"Experience Score": experience_score,
			"Match Score": final_score,
			"Missing Skills": ", ".join(missing_skills),
			"Status": "Pending",
			"Notes": "",
			"Resume": file.name,
		})

		with st.expander(file.name):
			st.write("### Candidate Information")
			st.write("**Name:**", candidate_info.get("Name", "Not Found"))
			st.write("**Email:**", candidate_info.get("Email", "Not Found"))
			st.write("**Skills:**")
			if candidate_info.get("Skills"):
				st.write(", ".join(candidate_info.get("Skills")))
			else:
				st.write("No skills detected")

			st.write("**Experience:**")
			st.write(f"{candidate_info.get('Experience', 0)} years")

			st.write("**Education:**")
			if candidate_info.get("Education"):
				st.write(", ".join(candidate_info.get("Education")))
			else:
				st.write("Education not detected")

	candidate_df = pd.DataFrame(candidate_data)

	st.subheader("📈 Recruitment Summary")
	total_candidates = len(candidate_df)
	average_score = round(candidate_df["Match Score"].mean(), 2) if total_candidates > 0 else 0
	top_score = candidate_df["Match Score"].max() if total_candidates > 0 else 0

	col1, col2, col3 = st.columns(3)
	with col1:
		st.metric("Total Candidates", total_candidates)
	with col2:
		st.metric("Average Match", f"{average_score}%")
	with col3:
		st.metric("Top Match", f"{top_score}%")

	candidate_df = candidate_df.sort_values(by="Match Score", ascending=False).reset_index(drop=True)
	candidate_df.index = candidate_df.index + 1
	candidate_df.index.name = "Rank"

	st.subheader("📊 Candidate Overview")
	st.dataframe(candidate_df, use_container_width=True)
	st.divider()

	st.subheader("👤 Candidate Review")
	selected_candidate = st.selectbox("Select Candidate", candidate_df["Name"]) if total_candidates > 0 else None

	if selected_candidate:
		selected_data = candidate_df[candidate_df["Name"] == selected_candidate].iloc[0]

		col1, col2 = st.columns(2)
		with col1:
			st.write("### 👤 Personal Information")
			st.write("**Name:**", selected_data["Name"])
			st.write("**Email:**", selected_data["Email"])
			st.write("**Experience:**", f"{selected_data['Experience']} years")
			st.write("**Education:**", selected_data["Education"])
		with col2:
			st.write("### 📊 Candidate Score")
			st.metric("Overall Match", f"{selected_data['Match Score']}%")
			st.metric("Skill Score", f"{selected_data['Skill Score']}%")
			st.metric("Experience Score", f"{selected_data['Experience Score']}%")

			st.write("### 📝 Recruiter Decision")
			decision = st.radio("Candidate Status", ["Pending", "Shortlisted", "Rejected"], horizontal=True)
			notes = st.text_area("Recruiter Notes", placeholder="Add notes about this candidate...")

			if st.button("💾 Save Decision"):
				selected_candidate_data = {
					"Name": selected_data["Name"],
					"Email": selected_data["Email"],
					"Skills": selected_data["Skills"],
					"Experience": selected_data["Experience"],
					"Education": selected_data["Education"],
					"Skill Score": selected_data["Skill Score"],
					"Experience Score": selected_data["Experience Score"],
					"Match Score": selected_data["Match Score"],
					"Missing Skills": selected_data["Missing Skills"],
					"Status": decision,
					"Notes": notes,
					"Resume": selected_data["Resume"],
				}

				save_candidate(selected_candidate_data)
				st.success(f"{selected_candidate} saved successfully!")

st.divider()

st.subheader("📚 Recruitment History")
saved_candidates = get_candidates()

if saved_candidates:
	history_data = []
	for candidate in saved_candidates:
		history_data.append({
			"Name": candidate[1],
			"Email": candidate[2],
			"Match Score": candidate[8],
			"Status": candidate[10],
			"Notes": candidate[11],
			"Resume": candidate[12],
		})

	history_df = pd.DataFrame(history_data)
	st.dataframe(history_df, use_container_width=True)
else:
	st.info("No recruitment decisions saved yet.")

st.subheader("⭐ Shortlisted Candidates")
shortlisted = [c for c in saved_candidates if c[10] == "Shortlisted"] if saved_candidates else []

if shortlisted:
	shortlisted_data = []
	for candidate in shortlisted:
		shortlisted_data.append({
			"Name": candidate[1],
			"Email": candidate[2],
			"Match Score": candidate[8],
			"Experience": candidate[4],
			"Education": candidate[5],
		})

	shortlisted_df = pd.DataFrame(shortlisted_data)
	st.dataframe(shortlisted_df, use_container_width=True)
else:
	st.info("No candidates have been shortlisted yet.")

