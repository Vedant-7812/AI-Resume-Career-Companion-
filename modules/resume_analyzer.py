import io
import re

import pymupdf
from docx import Document


SKILLS = [
    "Python",
    "SQL",
    "Java",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "Git",
    "Excel",
    "Power BI",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "Flask",
    "Django",
    "FastAPI",
    "Angular",
    "Vue.js",
    "PHP",
    "Kotlin",
    "Swift",
    "R",
    "Linux",
    "Firebase",
    "GitHub",
    "REST API",
    "OpenCV",
    "NLP",
    "Computer Vision",
]


SECTION_ALIASES = {
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
        "educational background",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
        "work history",
        "employment history",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "courses",
        "licenses",
    ],
    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "objective",
        "career objective",
        "profile",
        "about me",
    ],
}


def clean_line(line):
    line = line.replace("\u00a0", " ")
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def extract_text(file_data, filename):
    filename = filename.lower()

    if filename.endswith(".pdf"):
        with pymupdf.open(
            stream=file_data,
            filetype="pdf",
        ) as pdf:
            pages = []

            for page in pdf:
                text = page.get_text(
                    "text",
                    sort=True,
                )

                if text:
                    pages.append(text)

        text = "\n".join(pages).strip()

        if not text:
            raise ValueError(
                "No selectable text found in the PDF."
            )

        return text

    if filename.endswith(".docx"):
        document = Document(
            io.BytesIO(file_data)
        )

        paragraphs = []

        for paragraph in document.paragraphs:
            line = clean_line(
                paragraph.text
            )

            if line:
                paragraphs.append(line)

        text = "\n".join(
            paragraphs
        ).strip()

        if not text:
            raise ValueError(
                "No text found in the DOCX file."
            )

        return text

    raise ValueError(
        "Only PDF and DOCX files are supported."
    )


def find_name(text):
    lines = [
        clean_line(line)
        for line in text.splitlines()
        if clean_line(line)
    ]

    ignored = [
        "resume",
        "curriculum vitae",
        "cv",
        "email",
        "phone",
        "mobile",
        "linkedin",
        "github",
        "summary",
        "profile",
        "objective",
    ]

    for line in lines[:10]:
        if "@" in line:
            continue

        if re.search(
            r"\+?\d[\d\s().-]{7,}",
            line,
        ):
            continue

        if any(
            word in line.lower()
            for word in ignored
        ):
            continue

        if 1 <= len(line.split()) <= 5:
            return line

    return "Unknown"


def find_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    if match:
        return match.group(0)

    return "Not found"


def find_phone(text):
    patterns = [
        r"\+91[\s-]?\d{10}",
        r"\+91[\s-]?\d{5}[\s-]?\d{5}",
        r"\b\d{10}\b",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
        )

        if match:
            return match.group(0)

    return "Not found"


def find_skills(text):
    found_skills = []
    lower_text = text.lower()

    for skill in SKILLS:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            lower_text,
        ):
            found_skills.append(skill)

    return found_skills


def normalize_heading(line):
    line = clean_line(line).lower()

    line = re.sub(
        r"^[^a-zA-Z]+",
        "",
        line,
    )

    line = re.sub(
        r"[:\-|]+$",
        "",
        line,
    )

    return line.strip()


def find_section(text, section_name):
    lines = text.splitlines()

    wanted_headings = SECTION_ALIASES.get(
        section_name,
        [section_name],
    )

    all_headings = []

    for aliases in SECTION_ALIASES.values():
        all_headings.extend(aliases)

    result = []
    collecting = False

    for raw_line in lines:
        line = clean_line(raw_line)

        if not line:
            continue

        heading = normalize_heading(line)

        if heading in wanted_headings:
            collecting = True
            continue

        if (
            collecting
            and heading in all_headings
        ):
            break

        if collecting:
            result.append(line)

    return result


def calculate_score(data):
    score = 0

    if data["name"] != "Unknown":
        score += 10

    if data["email"] != "Not found":
        score += 5

    if data["phone"] != "Not found":
        score += 5

    if data["skills"]:
        score += 15

    if data["education"]:
        score += 15

    if data["projects"]:
        score += 15

    if data["experience"]:
        score += 15

    if data["certifications"]:
        score += 5

    if data["summary"]:
        score += 10

    return min(score, 100)


def get_missing_items(data):
    missing = []

    if data["email"] == "Not found":
        missing.append("Email")

    if data["phone"] == "Not found":
        missing.append("Phone number")

    if not data["summary"]:
        missing.append("Professional summary")

    if not data["education"]:
        missing.append("Education")

    if not data["projects"]:
        missing.append("Projects")

    if not data["experience"]:
        missing.append(
            "Experience or internship"
        )

    if not data["certifications"]:
        missing.append("Certifications")

    if not data["skills"]:
        missing.append("Technical skills")

    return missing


def analyze_resume(file_data, filename):
    text = extract_text(
        file_data,
        filename,
    )

    data = {
        "name": find_name(text),
        "email": find_email(text),
        "phone": find_phone(text),
        "skills": find_skills(text),
        "education": find_section(
            text,
            "education",
        ),
        "projects": find_section(
            text,
            "projects",
        ),
        "experience": find_section(
            text,
            "experience",
        ),
        "certifications": find_section(
            text,
            "certifications",
        ),
        "summary": find_section(
            text,
            "summary",
        ),
        "raw_text": text,
    }

    data["resume_score"] = calculate_score(
        data
    )

    data["missing_items"] = get_missing_items(
        data
    )

    return data