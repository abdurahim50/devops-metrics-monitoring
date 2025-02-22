# devops-metrics-monitoring

# 🚀 DevOps-Powered Python Monitoring System

## 📌 Project Overview
This project is a **real-time system monitoring application** that collects, processes, and visualizes system metrics such as CPU and memory usage. The backend is built with **FastAPI**, metrics are stored in **PostgreSQL**, real-time streaming is handled by **Kafka**, and the application is deployed using **Docker, Kubernetes (EKS), and AWS** with a **CI/CD pipeline** for automation.

## 🎯 Key Features
✅ **FastAPI Backend** to expose system metrics via REST API  
✅ **Kafka Streaming** for real-time metric ingestion  
✅ **PostgreSQL Database** for storing historical data  
✅ **Docker & Kubernetes** for containerization and orchestration  
✅ **GitLab CI/CD** for automated deployment  
✅ **Terraform & AWS EKS** for cloud infrastructure  
✅ **Grafana & VictoriaMetrics** for real-time monitoring & alerting  

---

## 📂 Project Structure
```
📦 devops-monitoring
├── 📂 app                 # FastAPI app for collecting system metrics
│   ├── __init__.py       # Initializes the app module
│   ├── __pycache__       # Compiled Python files
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── database.cpython-310.pyc
│   │   ├── main.cpython-310.pyc
│   │   └── main.cpython-39.pyc
│   ├── consumer.py       # Kafka consumer to process messages
│   ├── database.py       # PostgreSQL database connection
│   ├── main.py           # API endpoints for metrics
│   ├── producer.py       # Kafka producer for real-time streaming
│   └── schemas.py        # Pydantic models for data validation
├── 📂 docker              # Docker related files
│   ├── Dockerfile        # Dockerfile for containerizing the app
│   └── start.sh          # Startup script for the container
├── docker-compose.yaml   # Docker Compose configuration for multi-container setup
├── 📂 helm               # Helm charts for Kubernetes deployment
│   └── metrics-app       # Helm chart for deploying the metrics app
├── 📂 kubernetes         # Kubernetes deployment files
│   ├── alerting_rules.yaml   # Alerting rules configuration
│   ├── deployment.yaml   # Kubernetes deployment spec
│   ├── hpa.yaml          # Horizontal Pod Autoscaler configuration
│   ├── monitoring.yaml   # Grafana and VictoriaMetrics setup
│   ├── network-policy.yaml   # Network policy configuration
│   ├── pdb.yaml          # Pod Disruption Budget configuration
│   └── service.yaml      # Kubernetes service for the app
├── requirements.txt      # Dependencies for the Python app
├── 📂 terraform          # Terraform scripts to deploy EKS cluster
│   ├── eks_cluster.tf    # EKS cluster configuration
│   └── main.tf           # Infrastructure setup
└── 📂 tests              # Automated tests for the application
    └── test_main.py      # Tests for API endpoints

```

---
## 🚀 Phase 1: Project Setup
## 🛠️ Setup & Installation

### **1️⃣ Prerequisites**
Ensure you have the following installed:
- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- [Kubernetes (kubectl, minikube)](https://kubernetes.io/)
- [Terraform](https://www.terraform.io/)

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/devops-metrics-monitoring.git
cd devops-metrics-monitoring

python3.10 -m venv venv
source venv/bin/activate

```
### 3️⃣ Create .env File
```
# Database
POSTGRE_HOST=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=StrongPass123!
POSTGRES_DB=metrics_db
# Kafka
KAFKA_BROKER=kafka:9092
# security
SECRET_KEY=$(openssl rand -hex 32)  # Generate a secure key
ALGORITHM=HS256
```

---
## 🚀 Phase 2: Backend Development (FastAPI)
### 4️⃣ Install Dependencies
```
pip install -r requirements.txt

# output
annotated-types==0.7.0
anyio==4.8.0
click==8.1.8
fastapi==0.115.8
greenlet==3.1.1
h11==0.14.0
idna==3.10
#kafka-python==2.0.3
prometheus_client==0.21.1
psycopg2-binary==2.9.10
pydantic==2.10.6
pydantic_core==2.27.2
sniffio==1.3.1
SQLAlchemy==2.0.38
starlette==0.45.3
typing_extensions==4.12.2
uvicorn==0.34.0
python-jose[cryptography]==3.3.0
passlib==1.7.4
python-multipart==0.0.6
cryptography==42.0.8  # Required for JWT
psutil==5.9.8
confluent-kafka==2.3.0
```
## Running Locally
Build the Docker image to ensure all dependencies are installed
```
docker-compose build --no--cache
docker-compose up -d
```
### verify containers
```
docker ps # Should show 4 running containers
```
### Test API Endpoints
```
# Get JWT token
curl -X POST http://localhost:8000/token -d "username=admin&password=adminpass"

# Access metrics (replace <TOKEN>)
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/metrics
```
### Kafka Integration
```
# Start producer
docker-compose exec app python app/producer.py

# Start consumer in another terminal
docker-compose exec app python app/consumer.py
```
### Database Verification
```
docker-compose exec db psql -U postgres -d metrics_db -c "SELECT * FROM metrics;"
```

---
## 🚀 Phase 3: Production Deployment (AWS EKS)
1. **Configure AWS CLI**
```
aws configure
```

2.  **Provision Infrastructure**
```
cd terraform
terraform init
terraform apply
```

3. **Deploy to Kubernetes** 
```
kubectl apply -f k8s/
kubectl create secret generic app-secrets \
  --from-literal=POSTGRES_PASSWORD=StrongPass123! \
  --from-literal=SECRET_KEY=$(openssl rand -hex 32)
```

---
 
## 📊 Monitoring & Alerting
This project integrates **Grafana & VictoriaMetrics** for real-time monitoring
### Install VictoriaMetrics & Grafana
```
helm repo add victoria-metrics https://victoriametrics.github.io/helm-charts
helm install victoria-metrics victoria-metrics/victoria-metrics-single -n monitoring

helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana -n monitoring
```
### Access Grafana dashboard
```
kubectl port-forward svc/grafana -n monitoring 3000:3000
```
Visit http://localhost:3000 and configure VictoriaMetrics as a data source.

- Default username/password: `admin/admin`
- Configure PromQL queries like:
  ```promql
  sum(rate(cpu_usage[5m])) by (instance)
  ```
  
###  **Set Up Alerting Rules**
```yaml
groups:
- name: alerts
  rules:
  - alert: HighCPUUsage
    expr: avg(rate(cpu_usage[5m])) > 75
    for: 2m
    labels:
      severity: critical
```


## 🚀 CI/CD Pipeline (GitLab)

This project uses **GitLab CI/CD** for automated builds and deployments. The `.gitlab-ci.yml` file contains:
```
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest -v

build:
  stage: build
  script:
    - docker build -t registry.gitlab.com/your-repo/metrics-app .
    - docker push registry.gitlab.com/your-repo/metrics-app

deploy:
  stage: deploy
  script:
    - aws eks update-kubeconfig --name metrics-cluster
    - kubectl apply -f kubernetes/deployment.yaml
```

Trigger the pipeline by pushing code to GitLab:
```bash
git add .
git commit -m "Deploying new version"
git push origin main
```

---

## 📌 Next Steps
📌 Add authentication & security best practices  
📌 Optimize Kafka consumer performance  
📌 Extend monitoring to include disk/network metrics  
📌 Deploy using ArgoCD for GitOps  

---

## 🤝 Contributing
We welcome contributions! Feel free to fork the repo and submit PRs. 

---

## 📜 License
This project is licensed under the MIT License.

---

## 📞 Contact
For questions, reach out at **yonghoabdurahim@gmail.com** or open an issue on GitHub. 🚀
