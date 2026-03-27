import re
from flask import Blueprint, request, jsonify
import src.data as data_store

routes = Blueprint("routes", __name__)

ALLOWED_FIELDS = {"informatique", "mathématiques", "physique", "chimie"}


def validate_student_data(data, student_id=None):
    if not data:
        return "Missing data", 400

    required_keys = ["firstName", "lastName", "email", "grade", "field"]
    if not all(k in data for k in required_keys):
        return "Missing required fields", 400

    if not isinstance(data["firstName"], str) or len(data["firstName"]) < 2:
        return "firstName must be at least 2 characters", 400

    if not isinstance(data["lastName"], str) or len(data["lastName"]) < 2:
        return "lastName must be at least 2 characters", 400

    if not isinstance(data["email"], str) or not re.match(
        r"[^@]+@[^@]+\.[^@]+", data["email"]
    ):
        return "Invalid email format", 400

    # Check email uniqueness
    for s in data_store.students:
        if s["email"] == data["email"] and s["id"] != student_id:
            return "Email already taken", 409

    if not isinstance(data["grade"], (int, float)) or not (0 <= data["grade"] <= 20):
        return "grade must be a number between 0 and 20", 400

    if data["field"] not in ALLOWED_FIELDS:
        return "Invalid field", 400

    return None, None


@routes.route("/students/stats", methods=["GET"])
def get_stats():
    students = data_store.students
    total = len(students)
    if total == 0:
        return (
            jsonify(
                {
                    "totalStudents": 0,
                    "averageGrade": 0,
                    "studentsByField": {},
                    "bestStudent": None,
                }
            ),
            200,
        )

    avg_grade = round(sum(s["grade"] for s in students) / total, 2)
    students_by_field = {
        field: sum(1 for s in students if s["field"] == field)
        for field in ALLOWED_FIELDS
    }
    best_student = max(students, key=lambda s: s["grade"])

    return (
        jsonify(
            {
                "totalStudents": total,
                "averageGrade": avg_grade,
                "studentsByField": students_by_field,
                "bestStudent": best_student,
            }
        ),
        200,
    )


@routes.route("/students/search", methods=["GET"])
def search_students():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify({"error": "Search query parameter 'q' is missing or empty"}), 400

    results = [
        s
        for s in data_store.students
        if query in s["firstName"].lower() or query in s["lastName"].lower()
    ]
    return jsonify(results), 200


@routes.route("/students", methods=["GET"])
def get_students():
    result = data_store.students.copy()

    # Sorting
    sort_by = request.args.get("sort")
    order = request.args.get("order", "asc").lower()

    if sort_by and len(result) > 0 and sort_by in result[0]:
        reverse = order == "desc"
        result.sort(key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)

    if page is not None and limit is not None:
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10
        start = (page - 1) * limit
        end = start + limit
        result = result[start:end]

    return jsonify(result), 200


@routes.route("/students/<id>", methods=["GET"])
def get_student(id):
    if not id.isdigit():
        return jsonify({"error": "Invalid ID format"}), 400
    student_id = int(id)
    student = next((s for s in data_store.students if s["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@routes.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    error, status = validate_student_data(data)
    if error:
        return jsonify({"error": error}), status

    new_student = {
        "id": data_store.student_id_counter,
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "email": data["email"],
        "grade": data["grade"],
        "field": data["field"],
    }
    data_store.students.append(new_student)
    data_store.student_id_counter += 1
    return jsonify(new_student), 201


@routes.route("/students/<id>", methods=["PUT"])
def update_student(id):
    if not id.isdigit():
        return jsonify({"error": "Invalid ID format"}), 400
    student_id = int(id)
    student = next((s for s in data_store.students if s["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    error, status = validate_student_data(data, student_id)
    if error:
        return jsonify({"error": error}), status

    student["firstName"] = data["firstName"]
    student["lastName"] = data["lastName"]
    student["email"] = data["email"]
    student["grade"] = data["grade"]
    student["field"] = data["field"]

    return jsonify(student), 200


@routes.route("/students/<id>", methods=["DELETE"])
def delete_student(id):
    if not id.isdigit():
        return jsonify({"error": "Invalid ID format"}), 400
    student_id = int(id)
    student = next((s for s in data_store.students if s["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data_store.students = [s for s in data_store.students if s["id"] != student_id]
    return jsonify({"message": "Student deleted successfully"}), 200
