# docker/Dockerfile
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt  # <-- Add --no-cache-dir

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /usr/local
COPY . .

RUN chmod +x docker/start.sh
CMD ["./docker/start.sh"]