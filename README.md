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
├── 📂 backend           # FastAPI app for collecting system metrics
│   ├── main.py         # API endpoints for metrics
│   ├── database.py     # PostgreSQL database connection
│   ├── producer.py     # Kafka producer for real-time streaming
│   ├── consumer.py     # Kafka consumer to process messages
│   ├── Dockerfile      # Dockerfile for containerizing the app
│   ├── requirements.txt # Dependencies
├── 📂 kubernetes        # Kubernetes deployment files
│   ├── deployment.yaml # Kubernetes deployment spec
│   ├── service.yaml    # Kubernetes service for app
│   ├── monitoring.yaml # Grafana and VictoriaMetrics setup
├── 📂 terraform         # Terraform scripts to deploy EKS cluster
│   ├── main.tf         # Infrastructure setup
├── .gitlab-ci.yml      # CI/CD pipeline configuration
└── README.md           # Documentation
```

---

## 🛠️ Setup & Installation

### **1️⃣ Prerequisites**
Ensure you have the following installed:
- [Python 3.9+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Apache Kafka](https://kafka.apache.org/)
- [Docker](https://www.docker.com/)
- [Kubernetes (kubectl, minikube)](https://kubernetes.io/)
- [Terraform](https://www.terraform.io/)

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/devops-monitoring.git
cd devops-monitoring
```

### **3️⃣ Set Up FastAPI Backend**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### **4️⃣ Start PostgreSQL & Create Metrics Table**
```bash
sudo -u postgres psql -c "CREATE DATABASE metrics_db;"
python database.py
```

### **5️⃣ Run Kafka Producer & Consumer**
```bash
python producer.py & python consumer.py
```

### **6️⃣ Dockerize the Application**
```bash
docker build -t metrics_app .
docker run -p 8000:8000 metrics_app
```

### **7️⃣ Deploy to Kubernetes**
```bash
kubectl apply -f kubernetes/deployment.yaml
```

### **8️⃣ Deploy to AWS using Terraform**
```bash
cd terraform
terraform init
terraform apply
```

---

## 🚀 CI/CD Pipeline (GitLab)

This project uses **GitLab CI/CD** for automated builds and deployments. The `.gitlab-ci.yml` file contains:
```yaml
stages:
  - build
  - deploy

deploy:
  script:
    - docker build -t registry.gitlab.com/your-repo/metrics_app .
    - docker push registry.gitlab.com/your-repo/metrics_app
    - kubectl apply -f kubernetes/deployment.yaml
```

Trigger the pipeline by pushing code to GitLab:
```bash
git add .
git commit -m "Deploying new version"
git push origin main
```

---

## 📊 Monitoring & Alerting
This project integrates **Grafana & VictoriaMetrics** for real-time monitoring.

### **1️⃣ Install Grafana & VictoriaMetrics**
```bash
helm install vm victoria-metrics/victoria-metrics-single
helm install grafana grafana/grafana
```

### **2️⃣ Access Grafana Dashboard**
```bash
kubectl port-forward svc/grafana 3000:80
```
- Default username/password: `admin/admin`
- Configure PromQL queries like:
  ```promql
  sum(rate(cpu_usage[5m])) by (instance)
  ```

### **3️⃣ Set Up Alerting Rules**
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
```bash
kubectl apply -f monitoring.yaml
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
