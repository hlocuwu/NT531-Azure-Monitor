from locust import HttpUser, task, between

class SteadyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def view_homepage(self):
        self.client.get("/")
