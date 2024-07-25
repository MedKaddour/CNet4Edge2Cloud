# locustfile.py

from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)  # wait between 1 and 2 seconds between each task execution

    @task
    def test_traffic_light_service(self):
        self.client.get("/")

    @task
    def test_noise_service(self):
        self.client.get("/noise")

    @task
    def test_air_quality_service(self):
        self.client.get("/air-quality")

    @task
    def test_video_detect_service(self):
        self.client.get("/video-detect")

