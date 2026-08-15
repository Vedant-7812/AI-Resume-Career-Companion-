import streamlit as st
from modules.job_matcher import analyze_job_match


st.title("🎯 Job Matcher")

st.write("Compare your resume with a job description and find your skill gap.")

# Get resume information from Member 2
resume_data = st.session_state.get("resume_data")

if not resume_data:
    st.info("Please upload and analyze your resume first from the Resume Analyzer page.")

else:
    st.success(
        f"Resume loaded for {resume_data.get('name', 'Candidate')}"
    )

    st.markdown("---")

    job_description = st.text_area(
        "📋 Paste Job Description",
        height=220,
        placeholder="Paste the job description here..."
    )

    if st.button("🔍 Check Match"):

        if not job_description.strip():
            st.warning("Please paste a job description first.")

        else:
            result = analyze_job_match(
                resume_data,
                job_description
            )

            st.success("Job analysis completed!")

            st.markdown("---")

            # Match score
            st.subheader("🎯 Overall Match")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Match Score",
                    f"{result['match_score']}%"
                )

            with col2:
                st.metric(
                    "Matching Skills",
                    len(result["matching_skills"])
                )

            with col3:
                st.metric(
                    "Missing Skills",
                    len(result["missing_skills"])
                )

            st.progress(result["match_score"] / 100)

            st.markdown("---")

            # Matching and missing skills
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matching Skills")

                if result["matching_skills"]:
                    for skill in result["matching_skills"]:
                        st.write(f"✓ {skill}")
                else:
                    st.write("No matching skills found.")

            with col2:
                st.subheader("❌ Missing Skills")

                if result["missing_skills"]:
                    for skill in result["missing_skills"]:
                        st.write(f"✗ {skill}")
                else:
                    st.success("You have all the required skills!")

            st.markdown("---")

            # Important keywords
            st.subheader("🔑 Important Job Keywords")

            if result["important_keywords"]:
                for keyword in result["important_keywords"]:
                    st.write(f"• {keyword}")
            else:
                st.write("No important keywords found.")

            st.markdown("---")

            # Recommended skills
            st.subheader("📚 Skills Recommended to Learn")

            if result["recommended_skills"]:

                for item in result["recommended_skills"]:

                    if item["priority"] == "High":
                        st.error(
                            f"🔴 {item['skill']} - High Priority"
                        )
                    else:
                        st.warning(
                            f"🟡 {item['skill']} - Medium Priority"
                        )

            else:
                st.success("No additional skills recommended.")

            st.markdown("---")

            # Resume skills
            st.subheader("👤 Your Resume Skills")

            if result["resume_skills"]:
                st.write(
                    ", ".join(result["resume_skills"])
                )
            else:
                st.write("No skills found in the resume.")

            # Job skills
            st.subheader("💼 Skills Required for This Job")

            if result["job_skills"]:
                st.write(
                    ", ".join(result["job_skills"])
                )
            else:
                st.write("No known technical skills found in the job description.")