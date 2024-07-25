from locust import HttpUser, task, between
import random
import uuid

class LoadTestUser(HttpUser):
    wait_time = between(1, 5)

    system_tasks = ["ps", "echo", "ifconfig", "ls", "pwd", "uptime", "df -h", "free -m", "uname -a", "whoami"]

    @task
    def create_cfp(self):
        tasks = [{"id": str(uuid.uuid4()), "command": random.choice(self.system_tasks)} for _ in range(5)]
        cfp_data = {
            "id": str(uuid.uuid4()),
            "tasks": tasks
        }
        self.client.post("/create_cfp", json=cfp_data)

