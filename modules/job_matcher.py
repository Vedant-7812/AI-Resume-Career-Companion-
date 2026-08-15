import re

# Dictionary to map different variations/aliases to standard skill names
SKILL_ALIASES = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",
    "natural language processing": "NLP",
    "nlp": "NLP",
    "computer vision": "Computer Vision",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "oracle": "Oracle",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "react.js": "React",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "flask": "Flask",
    "django": "Django",
    "rest api": "REST API",
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "git": "Git",
    "github": "GitHub",
    "jenkins": "Jenkins",
    "linux": "Linux",
    "excel": "Excel",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "spark": "Apache Spark",
    "hadoop": "Hadoop"
}

# Key in-demand skills to flag as high priority for learning
HIGH_PRIORITY_SKILLS = {
    "Python",
    "Java",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "SQL",
    "AWS",
    "Azure",
    "Google Cloud",
    "TensorFlow",
    "PyTorch",
    "Docker",
    "Kubernetes"
}

# Soft skills and general domain keywords
IMPORTANT_KEYWORDS = [
    "experience",
    "internship",
    "teamwork",
    "leadership",
    "communication",
    "problem solving",
    "problem-solving",
    "analytical",
    "development",
    "testing",
    "deployment",
    "api",
    "database",
    "cloud",
    "research",
    "management"
]


# Normalize a single skill name to a standard format
def normalize_skill(skill):
    if not skill or not isinstance(skill, str):
        return None
    cleaned = skill.strip().lower()
    return SKILL_ALIASES.get(cleaned, skill.strip().title())


# Clean and deduplicate a list of skills
def normalize_skills(skills):
    if not skills:
        return []
    result = set()
    for s in skills:
        norm = normalize_skill(s)
        if norm:
            result.add(norm)
    return sorted(result)


# Find technical skills mentioned in the job description text
def extract_job_skills(job_description):
    if not job_description or not isinstance(job_description, str):
        return []

    text = job_description.lower()
    found_skills = set()

    # Match longer phrases first so substrings do not get picked up early
    sorted_aliases = sorted(SKILL_ALIASES.keys(), key=len, reverse=True)

    for alias in sorted_aliases:
        # Regex boundary check that works with punctuation symbols like C++ or .js
        pattern = r"(?:(?<=\W)|(?<=\A))" + re.escape(alias) + r"(?:(?=\W)|(?=\Z))"
        if re.search(pattern, text):
            found_skills.add(SKILL_ALIASES[alias])

    return sorted(found_skills)


# Find soft skills and general keywords in the job description
def extract_important_keywords(job_description):
    if not job_description or not isinstance(job_description, str):
        return []

    text = job_description.lower()
    found_keywords = set()

    for kw in IMPORTANT_KEYWORDS:
        pattern = r"(?:(?<=\W)|(?<=\A))" + re.escape(kw.lower()) + r"(?:(?=\W)|(?=\Z))"
        if re.search(pattern, text):
            # Clean up hyphenated words for display
            clean_kw = kw.replace("-", " ").title()
            found_keywords.add(clean_kw)

    return sorted(found_keywords)


# Compare skills extracted from resume against job requirements
def compare_skills(resume_skills, job_skills):
    resume_set = set(normalize_skills(resume_skills))
    job_set = set(normalize_skills(job_skills))

    matching = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    return matching, missing


# Calculate overall match percentage based on required job skills
def calculate_match_score(matching_skills, job_skills):
    if not job_skills:
        return 0
    score = (len(matching_skills) / len(job_skills)) * 100
    return round(score)


# Check priority level for a missing skill
def get_skill_priority(skill):
    if skill in HIGH_PRIORITY_SKILLS:
        return "High"
    return "Medium"


# Generate learning recommendations for missing skills sorted by priority
def recommend_skills(missing_skills):
    recommendations = []
    for skill in missing_skills:
        recommendations.append({
            "skill": skill,
            "priority": get_skill_priority(skill)
        })

    # Sort high priority first, then alphabetically
    recommendations.sort(key=lambda x: (0 if x["priority"] == "High" else 1, x["skill"]))
    return recommendations


# Main function to analyze resume against job description (Used by Member 1 & Member 4)
def analyze_job_match(resume_data, job_description):
    if not isinstance(resume_data, dict):
        resume_data = {}

    # Extract skills passed from Member 2
    raw_resume_skills = resume_data.get("skills", [])
    resume_skills = normalize_skills(raw_resume_skills)

    # Extract skills from job description text
    job_skills = extract_job_skills(job_description)

    # Compare skills and calculate match score
    matching_skills, missing_skills = compare_skills(resume_skills, job_skills)
    match_score = calculate_match_score(matching_skills, job_skills)

    # Extract keywords and generate recommendations
    important_keywords = extract_important_keywords(job_description)
    recommended_skills = recommend_skills(missing_skills)

    return {
        "name": resume_data.get("name", "Unknown"),
        "email": resume_data.get("email", "Not available"),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "important_keywords": important_keywords,
        "recommended_skills": recommended_skills
    }


# Format candidate result into a dictionary suitable for recruiter table (Used by Member 5)
def create_candidate_result(resume_data, job_description):
    result = analyze_job_match(resume_data, job_description)

    return {
        "Name": result["name"],
        "Email": result["email"],
        "Skills": ", ".join(result["resume_skills"]),
        "Match Score": result["match_score"],
        "Missing Skills": ", ".join(result["missing_skills"])
    }


# Rank candidates in descending order based on match score (Used by Member 5)
def rank_candidates(candidates):
    return sorted(
        candidates,
        key=lambda candidate: candidate.get("Match Score", 0),
        reverse=True
    )


# Quick test run
if __name__ == "__main__":
    sample_resume = {
        "name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "skills": ["Python", "SQL", "Pandas", "Machine Learning", "Git"]
    }

    sample_job = """
    Looking for a Machine Learning Engineer with experience in Python, SQL, 
    Machine Learning, TensorFlow, AWS, Docker, and Git. 
    Good communication and problem solving skills required.
    """

    # Test detailed analysis for UI
    result = analyze_job_match(sample_resume, sample_job)
    print("Candidate:", result["name"])
    print("Match Score:", result["match_score"], "%")
    print("Matching Skills:", result["matching_skills"])
    print("Missing Skills:", result["missing_skills"])
    print("Recommended:", result["recommended_skills"])

    # Test recruiter ranking
    candidate_row = create_candidate_result(sample_resume, sample_job)
    ranked = rank_candidates([candidate_row])
    print("Ranked List:", ranked)