import pytest
from src.app import app
import src.data as data_store


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        data_store.reset_db()
        yield client


# 1. GET /students
def test_get_students(client):
    res = client.get("/students")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 5


# 2. GET /students/:id (Success)
def test_get_student_success(client):
    res = client.get("/students/1")
    assert res.status_code == 200
    assert res.get_json()["firstName"] == "Alice"


# 3. GET /students/:id (Not Found)
def test_get_student_not_found(client):
    res = client.get("/students/999")
    assert res.status_code == 404


# 4. GET /students/:id (Invalid ID)
def test_get_student_invalid_id(client):
    res = client.get("/students/abc")
    assert res.status_code == 400


# 5. POST /students (Success)
def test_create_student_success(client):
    new_student = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "grade": 14.5,
        "field": "informatique",
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 201
    assert res.get_json()["id"] == 6


# 6. POST /students (Missing fields)
def test_create_student_missing_fields(client):
    res = client.post("/students", json={"firstName": "John"})
    assert res.status_code == 400


# 7. POST /students (firstName < 2 chars)
def test_create_student_invalid_first_name(client):
    new_student = {
        "firstName": "J",
        "lastName": "Doe",
        "email": "j.doe@example.com",
        "grade": 14.5,
        "field": "informatique",
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 400


# 8. POST /students (lastName < 2 chars)
def test_create_student_invalid_last_name(client):
    new_student = {
        "firstName": "John",
        "lastName": "D",
        "email": "jd@example.com",
        "grade": 14.5,
        "field": "informatique",
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 400


# 9. POST /students (Invalid email)
def test_create_student_invalid_email(client):
    new_student = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "not-an-email",
        "grade": 14.5,
        "field": "informatique",
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 400


# 10. POST /students (Duplicate email)
def test_create_student_duplicate_email(client):
    new_student = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "alice@example.com",  # already exists
        "grade": 14.5,
        "field": "informatique",
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 409


# 11. POST /students (Invalid grade)
def test_create_student_invalid_grade(client):
    new_student = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john2@example.com",
        "grade": 25,  # out of bounds
        "field": "informatique",
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 400


# 12. POST /students (Invalid field)
def test_create_student_invalid_field(client):
    new_student = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john3@example.com",
        "grade": 15,
        "field": "biologie",  # invalid value
    }
    res = client.post("/students", json=new_student)
    assert res.status_code == 400


# 13. PUT /students/:id (Success)
def test_update_student_success(client):
    update_data = {
        "firstName": "AliceUpdated",
        "lastName": "Martin",
        "email": "alice@example.com",
        "grade": 16,
        "field": "informatique",
    }
    res = client.put("/students/1", json=update_data)
    assert res.status_code == 200
    assert res.get_json()["firstName"] == "AliceUpdated"


# 14. PUT /students/:id (Not Found)
def test_update_student_not_found(client):
    res = client.put(
        "/students/999",
        json={
            "firstName": "AliceUpdated",
            "lastName": "Martin",
            "email": "alice999@example.com",
            "grade": 16,
            "field": "informatique",
        },
    )
    assert res.status_code == 404


# 15. PUT /students/:id (Duplicate Email)
def test_update_student_duplicate_email(client):
    update_data = {
        "firstName": "AliceUpdated",
        "lastName": "Martin",
        "email": "bob@example.com",  # belongs to id 2
        "grade": 16,
        "field": "informatique",
    }
    res = client.put("/students/1", json=update_data)
    assert res.status_code == 409


# 16. DELETE /students/:id (Success)
def test_delete_student_success(client):
    res = client.delete("/students/1")
    assert res.status_code == 200
    # verify deletion
    res_get = client.get("/students/1")
    assert res_get.status_code == 404


# 17. DELETE /students/:id (Not Found)
def test_delete_student_not_found(client):
    res = client.delete("/students/999")
    assert res.status_code == 404


# 18. GET /students/stats (Success)
def test_get_stats(client):
    res = client.get("/students/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["totalStudents"] == 5
    assert data["averageGrade"] == 15.0  # (15+12.5+18+9.5+20) / 5 = 15.0


# 19. GET /students/search (Success)
def test_search_students(client):
    res = client.get("/students/search?q=alice")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["firstName"] == "Alice"


# 20. GET /students/search (Missing Query)
def test_search_students_missing_query(client):
    res = client.get("/students/search")
    assert res.status_code == 400


# 21. GET /students (Pagination)
def test_get_students_pagination(client):
    # Add enough students to paginate
    # We already have 5, so page 1 limit 2 should return 2 students
    res = client.get("/students?page=1&limit=2")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2

    res2 = client.get("/students?page=3&limit=2")
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert len(data2) == 1
    assert data2[0]["id"] == 5


# 22. GET /students (Sorting)
def test_get_students_sorting(client):
    res = client.get("/students?sort=grade&order=desc")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 5
    assert data[0]["grade"] == 20.0
    assert data[4]["grade"] == 9.5
