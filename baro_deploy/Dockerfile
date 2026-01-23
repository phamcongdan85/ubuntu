# Dockerfile
# ----------------------------------------
# Base image: Python 3.10 slim (official)
# ----------------------------------------
FROM python:3.10-slim

# Làm việc trong thư mục /app
WORKDIR /app

# Copy file requirements và cài đặt dependencies
COPY app/requirements.txt /app/requirements.txt

# Cài đặt gcc và libpq-dev tạm thời để build các gói cần thiết (ví dụ numpy, pandas)
# Sau khi cài xong thì remove để image nhẹ hơn
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get purge -y --auto-remove gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy toàn bộ mã nguồn ứng dụng vào container
COPY app /app

# Expose port FastAPI (uvicorn)
EXPOSE 8000

# Lệnh khởi chạy container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
