import csv

# --- Step 1: Set up all data structures before the loop ---
room_counts = {}      # room_name -> number of events
type_counts = {}      # event_type -> number of events
day_attendees = {}    # date -> total attendees that day
all_events = []       # list of row dicts

# --- Step 2: Single pass through the CSV ---
with open("bookings.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        room = row["room"]
        event_type = row["event_type"]
        date = row["date"]
        attendees = int(row["attendees"])

        # update room_counts
        if room in room_counts:
            room_counts[room] += 1
        else:
            room_counts[room] = 1

        # update type_counts
        if event_type in type_counts:
            type_counts[event_type] += 1
        else:
            type_counts[event_type] = 1

        # update day_attendees
        day_attendees[date] = day_attendees.get(date, 0) + attendees

        # append original row
        all_events.append(row)

# --- Step 3: Find the busiest day ---
busiest_day = max(day_attendees, key=day_attendees.get)
busiest_count = day_attendees[busiest_day]

# --- Step 4: Filter large events (> 50 attendees) and sort by attendees desc ---
large_events = [row for row in all_events if int(row["attendees"]) > 50]
large_events_sorted = sorted(
    large_events,
    key=lambda row: int(row["attendees"]),
    reverse=True
)

# --- Step 5: Print the report ---
print("=== Community Centre Booking Report ===")

print("\nBookings by Room:")
for room in sorted(room_counts):
    print(f"  {room}: {room_counts[room]}")

print("\nBookings by Event Type:")
for etype in sorted(type_counts):
    print(f"  {etype}: {type_counts[etype]}")

print(f"\nBusiest Day: {busiest_day} ({busiest_count} attendees)")

print("\nLarge Events (> 50 attendees):")
for row in large_events_sorted:
    print(f"  {row['date']} | {row['room']} | {row['event_type']} | {row['attendees']} attendees")
