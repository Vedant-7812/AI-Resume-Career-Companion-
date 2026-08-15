import sqlite3


DB_NAME = "recruiter.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            skills TEXT,
            experience REAL,
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

    conn.commit()

    conn.close()


def save_candidate(candidate):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            name,
            email,
            skills,
            experience,
            education,
            skill_score,
            experience_score,
            match_score,
            missing_skills,
            status,
            notes,
            resume
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

    conn.commit()

    conn.close()


def get_candidates():

    conn = sqlite3.connect(DB_NAME)

    data = conn.execute("""
        SELECT *
        FROM candidates
        ORDER BY match_score DESC
    """).fetchall()

    conn.close()

    return data