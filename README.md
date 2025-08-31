This project implements a self-service database anti-corruption layer REST API on Kubernetes with a GitOps workflow. 

1. Developers define REST endpoints → SQL queries → field mappings in mappings.yaml.
2. A Python Flask API reads the config and dynamically serves data from PostgreSQL.
3. All infrastructure is deployed to a Kind cluster with a local Docker registry.
4. GitHub Actions automates build + push + deployment (GitOps style).

**Setup Instructions**

**Prerequisites**

Docker
Kind (Kubernetes in Docker)
kubectl
GitHub Actions enabled (for CI/CD)

**Create Kind Cluster:**

cd infra/k8s-cluster
./create-kind-cluster.sh

**Start Local Docker Registry**

cd infra/docker-registry
./start-registry.sh

**Deploy PostgreSQL**

kubectl apply -f infra/database/deployment.yaml

**Deploy API**

kubectl apply -f infra/api/deployment.yaml

**Test API**

kubectl port-forward svc/anti-corruption-api-service 3000:3000
curl http://localhost:3000/users

**GitOps Workflow**

The workflow is defined in .github/workflows/main.yaml.

**Triggers**

Config changes (mappings.yaml) → ConfigMap updated → API reloads automatically.
API code/Dockerfile changes → New Docker image built + pushed → Deployment refreshed.
Database manifest changes → PostgreSQL redeployed.

**Flow**

1. Developer commits to main.
2. GitHub Actions workflow runs:
   1. Build & push Docker image to localhost:5000.
   2. Apply manifests for PostgreSQL + API.
3. Cluster updates automatically.

**Deliverables**

1. Infra: Local K8s cluster + Docker registry + PostgreSQL + API deployments.
2. API: Flask app with dynamic YAML-based query mapping.
3. GitOps CI/CD: GitHub Actions workflow automating build & deploy.
