import json
import unittest
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8081"


def request_api(path, method="GET", data=None):
    url = BASE_URL + path

    headers = {}
    body = None

    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.read()

    except urllib.error.HTTPError as error:
        return error.code, error.read()


def create_test_task():
    status, body = request_api(
        "/api/tasks",
        method="POST",
        data={
            "title": "Automated Test Task",
            "description": "Created by automated testing"
        }
    )

    if status != 201:
        raise RuntimeError(
            f"Could not create test task. Status: {status}"
        )

    task = json.loads(body)

    return task["id"]


class TaskManagerAPITests(unittest.TestCase):

    def test_health_endpoint(self):
        status, body = request_api("/api/health")

        self.assertEqual(status, 200)

        response = json.loads(body)

        self.assertEqual(response["status"], "healthy")
        self.assertEqual(response["database"], "connected")

    def test_get_tasks(self):
        status, body = request_api("/api/tasks")

        self.assertEqual(status, 200)

        tasks = json.loads(body)

        self.assertIsInstance(tasks, list)

    def test_create_task(self):
        status, body = request_api(
            "/api/tasks",
            method="POST",
            data={
                "title": "Jenkins Automated Test",
                "description": "Created by CI pipeline"
            }
        )

        self.assertEqual(status, 201)

        task = json.loads(body)

        self.assertEqual(
            task["title"],
            "Jenkins Automated Test"
        )

        self.assertEqual(task["status"], "Pending")

    def test_invalid_task_title(self):
        status, body = request_api(
            "/api/tasks",
            method="POST",
            data={
                "title": "",
                "description": "Invalid task"
            }
        )

        self.assertEqual(status, 400)

    def test_invalid_task_status(self):
        task_id = create_test_task()

        status, body = request_api(
            f"/api/tasks/{task_id}",
            method="PATCH",
            data={
                "status": "Invalid Status"
            }
        )

        self.assertEqual(status, 400)

    def test_update_task_status(self):
        task_id = create_test_task()

        status, body = request_api(
            f"/api/tasks/{task_id}",
            method="PATCH",
            data={
                "status": "Completed"
            }
        )

        self.assertEqual(status, 200)

        task = json.loads(body)

        self.assertEqual(task["status"], "Completed")

    def test_delete_task(self):
        task_id = create_test_task()

        status, body = request_api(
            f"/api/tasks/{task_id}",
            method="DELETE"
        )

        self.assertEqual(status, 200)

        response = json.loads(body)

        self.assertEqual(
            response["message"],
            "Task deleted"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
