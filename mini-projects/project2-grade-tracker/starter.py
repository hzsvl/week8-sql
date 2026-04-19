import csv

scores = []
grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

highest = {"name": "", "score": -1}
lowest = {"name": "", "score": 101}

with open("grades.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["name"]
        score = int(row["score"])

        # append score
        scores.append(score)

        # highest
        if score > highest["score"]:
            highest["score"] = score
            highest["name"] = name

        # lowest
        if score < lowest["score"]:
            lowest["score"] = score
            lowest["name"] = name

        # grade letter
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        grade_counts[grade] += 1

# average
average = sum(scores) / len(scores)

# print
print("=== Quiz Grade Summary ===")
print(f"Total students: {len(scores)}")
print(f"Average score: {average:.1f}")
print(f"Highest score: {highest['name']} ({highest['score']})")
print(f"Lowest score: {lowest['name']} ({lowest['score']})")

print("\nGrade distribution:")
for grade, count in grade_counts.items():
    print(f"{grade}: {count}")
