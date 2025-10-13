from locust import HttpUser, task, between, events

class SpikeUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def simulate_spike(self):
        self.client.get("/")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Spike Test bắt đầu – tăng tải đột ngột!")
