# Base image Python
FROM python:3.11-slim

# Cài đặt thư viện cần thiết
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY Scenarios ./Scenarios 


# Cổng mặc định của Locust UI
EXPOSE 8089

# Mặc định chạy chế độ web
CMD ["locust", "-f", "Scenarios/Scenario_1_Startup.py"]

