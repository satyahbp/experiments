import random, uuid, logging
from locust import HttpUser, task, between

logger = logging.getLogger(__name__)


class APIUser(HttpUser):
    # Nginx service name on the Docker Compose network
    host = "http://nginx:80"

    # Wait between requests to simulate user behavior
    wait_time = between(0.1, 0.5)

    @task
    def test_home(self):
        self.client.get("/api/", name="GET /api/")


    @task
    def get_existing_user(self):
        # Pick a random user ID from a sample range
        user_id = random.randint(1, 1000)
        with self.client.get(
            f"/api/users/{user_id}",
            name="GET /api/users/[user_id]",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
                return
            body = response.json()
            if body.get("user_id") != user_id:
                response.failure(f"Mismatched user_id in response: {body}")


    @task(1)
    def create_student(self):
        # Unique email per request so a unique constraint on email won't cause failures
        payload = {
            "name": f"Student {uuid.uuid4().hex[:8]}",
            "email": f"student-{uuid.uuid4().hex}@example.com",
            "class_": random.choice(["8", "9", "10", "11", "12"]),
            "section": random.choice(["A", "B", "C"]),
        }
        with self.client.post(
            "/api/students",
            json=payload,
            name="POST /api/students [create]",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}: {response.text}")
                return
            body = response.json()
            if body.get("email") != payload["email"] or "id" not in body:
                response.failure(f"Response did not match created student: {body}")


    @task(3)
    def list_students(self):
        limit = random.randint(10, 100)
        section = random.choice(["A", "B", "C"])

        with self.client.get(
            "/api/students",
            params={
                "limit": limit,
                "offset": 0,
                "sort_by": "id",
                "section": section,
            },
            name="GET /api/students [list]",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
                logger.error(
                    "HTTP failure: status=%s, url=%s, body=%s",
                    response.status_code,
                    response.url,
                    response.text[:500],
                )
                return

            try:
                body = response.json()
            except ValueError:
                response.failure("Response is not valid JSON")
                logger.exception("Invalid JSON response: %s", response.text[:500])
                return

            error = None
            if not isinstance(body, list):
                error = f"Expected a list, got {type(body).__name__}"
            elif len(body) > limit:
                error = f"Expected at most {limit} students, got {len(body)}"
            elif any(student.get("section") != section for student in body):
                error = f"Expected section {section}; received sections: " + str(
                    sorted({
                        student.get("section")
                        for student in body
                    })
                )
            elif body and "email" not in body[0]:
                error = f"Student entries are missing fields: {body[0]}"

            if error:
                response.failure(error)
                logger.error(
                    "Validation failure: %s | requested_section=%s | "
                    "limit=%s | url=%s",
                    error,
                    section,
                    limit,
                    response.url,
                )