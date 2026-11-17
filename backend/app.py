import os
from flask import Flask, request, jsonify
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "taskmanager")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        row_factory=dict_row
    )


@app.route("/api/health", methods=["GET"])
def health():
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1")

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:
        app.logger.exception("Health check failed")
        return jsonify({
            "status": "unhealthy"
        }), 503


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    with get_db_connection() as conn:
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    return jsonify(tasks), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title or len(title) > 200:
        return jsonify({
            "error": "Title is required and must be under 200 characters"
        }), 400

    with get_db_connection() as conn:
        task = conn.execute(
            """
            INSERT INTO tasks (title, description)
            VALUES (%s, %s)
            RETURNING *
            """,
            (title, description)
        ).fetchone()

    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    allowed_statuses = [
        "Pending", "In Progress", "Completed"
    ]

    if status not in allowed_statuses:
        return jsonify({"error": "Invalid status"}), 400

    with get_db_connection() as conn:
        task = conn.execute(
            """
            UPDATE tasks
            SET status = %s
            WHERE id = %s
            RETURNING *
            """,
            (status, task_id)
        ).fetchone()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db_connection() as conn:
        task = conn.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id
            """,
            (task_id,)
        ).fetchone()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
