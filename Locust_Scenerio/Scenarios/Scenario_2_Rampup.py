from locust import HttpUser, task, between

class RampUpUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_products(self):
        self.client.get("/")
