import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Database Tables:")
for table in tables:
    print(f"  - {table[0]}")

print("\nTable Contents:")

# Check lectures table
print("\nLectures Table:")
cursor.execute("SELECT COUNT(*) FROM lectures;")
count = cursor.fetchone()[0]
print(f"  Total lectures: {count}")

if count > 0:
    cursor.execute("SELECT id, data FROM lectures LIMIT 3;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  ID: {row[0]}")
        try:
            data = json.loads(row[1])
            print(f"    Lecture: {data.get('lenda_e_rreg', 'N/A')}")
            print(f"    Professor: {data.get('prof_rreg', 'N/A')}")
        except:
            print("    Data: [Error parsing JSON]")

# Check classrooms table
print("\nClassrooms Table:")
cursor.execute("SELECT COUNT(*) FROM classrooms;")
count = cursor.fetchone()[0]
print(f"  Total classrooms: {count}")

# Check time_slots table
print("\nTime Slots Table:")
cursor.execute("SELECT COUNT(*) FROM time_slots;")
count = cursor.fetchone()[0]
print(f"  Total time slots: {count}")

# Check schedules table
print("\nSchedules Table:")
cursor.execute("SELECT COUNT(*) FROM schedules;")
count = cursor.fetchone()[0]
print(f"  Total schedules: {count}")

# Check schedule_versions table
print("\nSchedule Versions Table:")
cursor.execute("SELECT COUNT(*) FROM schedule_versions;")
count = cursor.fetchone()[0]
print(f"  Total versions: {count}")

conn.close()

print("\nDatabase inspection complete.")