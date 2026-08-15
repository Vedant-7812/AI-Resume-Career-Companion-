from pathlib import Path

from modules.resume_analyzer import analyze_resume


def process_resume(file_path):
    resume_path = Path(file_path)

    if not resume_path.exists():
        raise FileNotFoundError(
            f"File not found: {resume_path}"
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


def main():
    print("===== Resume Analyzer =====")

    file_path = input(
        "Resume file cha full path enter kara: "
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

        print("\nSkills:")
        if result["skills"]:
            for skill in result["skills"]:
                print(f"- {skill}")
        else:
            print("Not found")

        print("\nMissing Items:")
        if result["missing_items"]:
            for item in result["missing_items"]:
                print(f"- {item}")
        else:
            print("No missing items")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()