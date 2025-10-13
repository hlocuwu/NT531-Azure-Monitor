FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Cho phép chạy file bash
RUN chmod +x run_all.sh

# Khi container chạy → tự động thực thi script
CMD ["bash", "run_all.sh"]
