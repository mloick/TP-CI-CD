students = []
student_id_counter = 1


def reset_db():
    global students, student_id_counter
    students = [
        {
            "id": 1,
            "firstName": "Alice",
            "lastName": "Martin",
            "email": "alice@example.com",
            "grade": 15.0,
            "field": "informatique",
        },
        {
            "id": 2,
            "firstName": "Bob",
            "lastName": "Dubois",
            "email": "bob@example.com",
            "grade": 12.5,
            "field": "mathématiques",
        },
        {
            "id": 3,
            "firstName": "Charlie",
            "lastName": "Roux",
            "email": "charlie@example.com",
            "grade": 18.0,
            "field": "physique",
        },
        {
            "id": 4,
            "firstName": "Diana",
            "lastName": "Lefebvre",
            "email": "diana@example.com",
            "grade": 9.5,
            "field": "chimie",
        },
        {
            "id": 5,
            "firstName": "Eve",
            "lastName": "David",
            "email": "eve@example.com",
            "grade": 20.0,
            "field": "informatique",
        },
    ]
    student_id_counter = 6


# Initialize at startup
reset_db()
