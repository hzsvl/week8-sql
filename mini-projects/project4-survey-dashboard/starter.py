import csv
import sqlite3

# --- STEP 1: CREATE DATABASE ---
conn = sqlite3.connect("survey.db")
db = conn.cursor()

db.execute("""
CREATE TABLE IF NOT EXISTS responses (
    student_id TEXT,
    faculty TEXT,
    year INTEGER,
    satisfaction INTEGER,
    favourite_tool TEXT,
    comments TEXT
)
""")

# --- STEP 2: LOAD CSV FILES ---
csv_files = [
    "faculty_science.csv",
    "faculty_arts.csv",
    "faculty_business.csv"
]

for filename in csv_files:
    faculty_name = filename.split("_")[1].split(".")[0].capitalize()

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute("""
            INSERT INTO responses VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row["student_id"],
                faculty_name,
                int(row["year"]),
                int(row["satisfaction"]),
                row["favourite_tool"],
                row["comments"]
            ))

conn.commit()
print("Database loaded successfully.\n")

# --- DASHBOARD ---
print("=" * 30)
print("UNIVERSITY SURVEY DASHBOARD")
print("=" * 30)

# --- Query 1 ---
print("\n1. Total Responses by Faculty")
rows = db.execute("""
SELECT faculty, COUNT(*) 
FROM responses 
GROUP BY faculty 
ORDER BY faculty
""").fetchall()

total = 0
for faculty, count in rows:
    print(f"{faculty:<12} {count}")
    total += count

print(f"{'TOTAL':<12} {total}")

# --- Query 2 ---
print("\n2. Average Satisfaction by Year of Study")
rows = db.execute("""
SELECT year, ROUND(AVG(satisfaction), 1)
FROM responses
GROUP BY year
ORDER BY year
""").fetchall()

for year, avg in rows:
    print(f"Year {year}: {avg} / 5")

# --- Query 3 ---
print("\n3. Favourite Tool Popularity")
rows = db.execute("""
SELECT favourite_tool, COUNT(*)
FROM responses
GROUP BY favourite_tool
ORDER BY COUNT(*) DESC
""").fetchall()

for tool, count in rows:
    print(f"{tool:<15} {count}")

# --- Query 4 ---
print("\n4. Faculty Comparison")
print(f"{'Faculty':<12} | {'Avg Satisfaction':<18} | Most Popular Tool")
print("-" * 55)

faculties = ["Arts", "Business", "Science"]

for faculty in faculties:
    avg = db.execute("""
    SELECT ROUND(AVG(satisfaction),1)
    FROM responses
    WHERE faculty = ?
    """, (faculty,)).fetchone()[0]

    tool = db.execute("""
    SELECT favourite_tool, COUNT(*) as n
    FROM responses
    WHERE faculty = ?
    GROUP BY favourite_tool
    ORDER BY n DESC
    LIMIT 1
    """, (faculty,)).fetchone()[0]

    print(f"{faculty:<12} | {avg:<18} | {tool}")

# --- Query 5 ---
print()
try:
    min_score = int(input("Enter minimum satisfaction score (1-5): "))
except:
    min_score = 4

rows = db.execute("""
SELECT student_id, faculty, year, favourite_tool
FROM responses
WHERE satisfaction >= ?
ORDER BY faculty, year
""", (min_score,)).fetchall()

print(f"\nStudents with satisfaction >= {min_score}:")
if not rows:
    print("No results found.")
else:
    for r in rows:
        print(f"{r[0]} | {r[1]} | Year {r[2]} | {r[3]}")

# --- CLEANUP ---
conn.close()
