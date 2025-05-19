from locust import HttpUser, task, between
import json

class URLClassifierUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    @task
    def classify_url(self):
        # Test with a valid URL
        self.client.post(
            "/api/classify",
            json={"url": "https://www.google.com"},
            headers={"Content-Type": "application/json"}
        )
    
    @task
    def classify_invalid_url(self):
        # Test with an invalid URL
        self.client.post(
            "/api/classify",
            json={"url": "not-a-valid-url"},
            headers={"Content-Type": "application/json"}
        )
    
    @task
    def classify_empty_url(self):
        # Test with empty URL
        self.client.post(
            "/api/classify",
            json={"url": ""},
            headers={"Content-Type": "application/json"}
        ) 