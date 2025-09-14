import requests
import json

# Add test classrooms
classrooms = [
    {
        "id": "S1",
        "name": "Room 101",
        "capacity": 50,
        "equipment": "Projector, Whiteboard",
        "status": "available"
    },
    {
        "id": "S2",
        "name": "Room 102",
        "capacity": 30,
        "equipment": "Whiteboard",
        "status": "available"
    },
    {
        "id": "S3",
        "name": "Computer Lab",
        "capacity": 25,
        "equipment": "Computers, Projector",
        "status": "available"
    }
]

for classroom in classrooms:
    try:
        response = requests.post(
            "http://localhost:8003/api/classrooms",
            json=classroom
        )
        print(f"Added classroom {classroom['id']}: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to add classroom {classroom['id']}: {e}")

# Verify classrooms were added
try:
    response = requests.get("http://localhost:8003/api/classrooms")
    print(f"\nCurrent classrooms: {response.status_code}")
    if response.status_code == 200:
        classrooms = response.json()
        for classroom in classrooms:
            print(f"  - {classroom['id']}: {classroom['name']} (Capacity: {classroom['capacity']})")
except Exception as e:
    print(f"Failed to fetch classrooms: {e}")