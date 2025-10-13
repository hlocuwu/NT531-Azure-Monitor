from locust import HttpUser, task, between

class StartupTestUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def view_homepage(self):
        self.client.get("/")

