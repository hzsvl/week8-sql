import csv

counts = {}

with open("../../week1/favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        language = row["language"]

        if language in counts:
            counts[language] += 1
        else:
            counts[language] = 1

# sort by popularity
sorted_languages = sorted(counts, key=counts.get, reverse=True)

# print results
for language in sorted_languages:
    print(f"{language}: {counts[language]}")
