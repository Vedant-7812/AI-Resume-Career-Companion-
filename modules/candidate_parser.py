import re


SKILL_LIST = [
    "Python",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "AWS",
    "Docker",
    "Kubernetes",
    "Git",
    "MongoDB",
    "MySQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Java",
    "C++",
    "C"
]


def extract_name(text):

    lines = text.strip().split("\n")

    for line in lines[:10]:

        line = line.strip()

        if line and "@" not in line and len(line) < 50:

            return line

    return "Not Found"


def extract_email(text):

    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILL_LIST:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_experience(text):

    pattern = r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)'

    matches = re.findall(
        pattern,
        text.lower()
    )

    if matches:

        return max(
            [float(x) for x in matches]
        )

    return 0


def extract_education(text):

    education_keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "M.Tech",
        "M.E",
        "Master",
        "MBA",
        "BCA",
        "MCA",
        "PhD"
    ]

    found_education = []

    text_lower = text.lower()

    for education in education_keywords:

        if education.lower() in text_lower:

            found_education.append(education)

    return found_education


def extract_candidate_info(text):

    candidate = {

        "Name": extract_name(text),

        "Email": extract_email(text),

        "Skills": extract_skills(text),

        "Experience": extract_experience(text),

        "Education": extract_education(text)

    }

    return candidate