import sys
from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from modules.resume_analyzer import analyze_resume


def process_resume(file_path):
    resume_path = Path(file_path)

    if not resume_path.exists():
        raise FileNotFoundError(
            f"File not found: {resume_path}"
        )

    if not resume_path.is_file():
        raise ValueError(
            f"Path is not a file: {resume_path}"
        )

    if resume_path.suffix.lower() not in [
        ".pdf",
        ".docx",
    ]:
        raise ValueError(
            "Only PDF and DOCX files are supported."
        )

    file_data = resume_path.read_bytes()
    filename = resume_path.name

    return analyze_resume(
        file_data,
        filename
    )


def print_section(title, items):
    print(f"\n{title}:")

    if items:
        for item in items:
            print(f"- {item}")
    else:
        print("Not found")


def main():
    print("===== Resume Analyzer =====")

    file_path = input(
        "Enter the full path of the resume file: "
    ).strip().strip('"')

    try:
        result = process_resume(file_path)

        print("\n===== Analysis Result =====")
        print(f"Name: {result['name']}")
        print(f"Email: {result['email']}")
        print(f"Phone: {result['phone']}")
        print(
            f"Resume Score: "
            f"{result['resume_score']}/100"
        )

        print_section(
            "Skills",
            result["skills"],
        )

        print_section(
            "Education",
            result["education"],
        )

        print_section(
            "Projects",
            result["projects"],
        )

        print_section(
            "Experience",
            result["experience"],
        )

        print_section(
            "Certifications",
            result["certifications"],
        )

        print_section(
            "Professional Summary",
            result["summary"],
        )

        print_section(
            "Missing Items",
            result["missing_items"],
        )

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()