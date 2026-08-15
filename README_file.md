# AI Resume Career Companion

## Member 2 Contribution: Resume Analyzer Module

### Project Overview

AI Resume Career Companion is a resume analysis system that extracts important information from a candidate's resume and provides a basic resume score with missing information.

The system supports PDF and DOCX resume files.

---

## My Role as Member 2

As Member 2, I worked on the Resume Analyzer module of the project.

My main responsibility was to develop the backend logic that reads a resume, extracts useful information, identifies resume sections, calculates a score, and displays missing details.

---

## Work Completed

I worked on the following features:

- PDF resume text extraction.
- DOCX resume text extraction.
- Candidate name detection.
- Email address detection.
- Phone number detection.
- Technical skill detection.
- Education section detection.
- Projects section detection.
- Experience and internship section detection.
- Certifications section detection.
- Professional summary detection.
- Resume score calculation.
- Missing information detection.
- Command-line testing.
- Code organization using Python modules.
- GitHub integration and project upload.

---

## Technologies Used

- Python
- PyMuPDF
- python-docx
- Regular Expressions
- pathlib
- argparse
- Git
- GitHub

---

## Resume Analyzer Features

### 1. PDF Support

The analyzer extracts selectable text from PDF resumes using PyMuPDF.

### 2. DOCX Support

The analyzer reads paragraphs from DOCX resumes using python-docx.

### 3. Contact Information Detection

The analyzer detects:

- Candidate name
- Email address
- Phone number

### 4. Technical Skills Detection

The analyzer checks for commonly used technical skills such as:

- Python
- SQL
- Java
- C++
- JavaScript
- React
- Node.js
- Pandas
- NumPy
- Machine Learning
- TensorFlow
- AWS
- Docker
- Git
- MySQL
- MongoDB
- Flask
- Django
- REST API
- OpenCV
- NLP

### 5. Resume Section Detection

The analyzer identifies the following sections:

- Education
- Projects
- Experience
- Certifications
- Professional Summary

The system also recognizes alternative headings.

For example:

- Academic Background is treated as Education.
- Personal Projects is treated as Projects.
- Work Experience is treated as Experience.
- Career Objective is treated as Summary.

### 6. Resume Score

The analyzer calculates a score out of 100 based on the availability of important resume information.

The score considers:

- Name
- Email
- Phone number
- Technical skills
- Education
- Projects
- Experience
- Certifications
- Professional summary

### 7. Missing Information

The analyzer displays missing items such as:

- Email
- Phone number
- Professional summary
- Education
- Projects
- Experience
- Certifications
- Technical skills

---

## System Workflow

```text
PDF or DOCX Resume
        |
        v
Text Extraction
        |
        v
Name, Email and Phone Detection
        |
        v
Technical Skills Detection
        |
        v
Resume Section Detection
        |
        v
Resume Score Calculation
        |
        v
Missing Information Report
```

---

## Project Structure

```text
Hackethon/
|
|-- modules/
|   |-- __init__.py
|   |-- resume_analyzer.py
|
|-- pages/
|   |-- __init__.py
|   |-- resume_analyzer_page.py
|
|-- README.md
|-- .gitignore
```

---

## Installation

Open PowerShell inside the project folder and run:

```powershell
cd C:\Users\USER\Hackethon
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install pymupdf python-docx
```

---

## Running the Resume Analyzer

Run the analyzer using:

```powershell
python -m pages.resume_analyzer_page
```

The program will ask for the full path of the resume:

```text
Resume file cha full path enter kara:
```

Enter the path of a PDF or DOCX resume.

Example:

```text
C:\Users\USER\Downloads\Resume.pdf
```

Another example:

```text
C:\Users\USER\Downloads\My Resume.docx
```

---

## Expected Output

```text
===== Analysis Result =====

Name: Candidate Name
Email: candidate@example.com
Phone: 9876543210
Resume Score: 80/100

Skills:
- Python
- SQL
- JavaScript

Missing Items:
- Certifications
```

---

## Important Note

The current version uses rule-based text analysis and predefined skills. It is not a trained machine-learning model yet.

In future versions, the following features can be added:

- Job description matching.
- AI-based resume suggestions.
- Skill-gap analysis.
- ATS compatibility checking.
- Career recommendations.
- Machine-learning or LLM-based resume feedback.

---

## My Contribution Summary

I developed the Resume Analyzer backend, implemented PDF and DOCX file processing, extracted resume information, detected technical skills and sections, calculated the resume score, identified missing information, tested the module, and integrated the work into the GitHub repository.

---

## Team Contribution

- Member 1: Project planning and main application development.
- Member 2: Resume Analyzer module and resume analysis backend.
- Other members: User interface, career recommendations, testing, and documentation.

---

## Future Scope

The system can be improved by adding:

- A graphical user interface.
- Database storage.
- User login.
- Job recommendation system.
- Resume comparison with job descriptions.
- Cloud deployment.
- Advanced AI-based suggestions.

---

## Conclusion

The Resume Analyzer module helps users understand the quality and completeness of their resumes. It extracts important information, calculates a basic score, and identifies missing resume sections.