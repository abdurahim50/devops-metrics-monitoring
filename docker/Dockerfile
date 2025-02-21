# docker/Dockerfile
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /usr/local
COPY . .

RUN chmod +x docker/start.sh
CMD ["./docker/start.sh"]