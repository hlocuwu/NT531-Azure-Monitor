# Sử dụng base image Python 3.10 loại slim 
FROM python:3.10-slim

# Đặt thư mục làm việc bên trong container là /app
WORKDIR /app

# 1. Sao chép file requirements

COPY requirements.txt .

# 2. Cài đặt các thư viện Từ file requirements
RUN pip install -r requirements.txt

# 3. Sao chép file kịch bản của bạn vào
COPY locust_file.py .

# Cổng mặc định của giao diện web Locust
EXPOSE 8089

# Lệnh mặc định để chạy khi container khởi động
ENTRYPOINT ["locust"]
CMD ["-f", "locust_file.py"]