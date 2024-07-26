from datetime import datetime, timedelta

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
            "call_for_proposal_id": str(uuid.uuid4()),
            "manager_id": "",
            "manager_description": "",
            "tasks": tasks,
            "task_description": "Execute system tasks",
            "contractor_selection_criterion": "lowest_bid",
            "bid_selection_criterion": "fastest_completion",
            "task_deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "cfp_deadline": (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "cfp_state": "open"
        }
        self.client.post("/create_cfp", json=cfp_data)

