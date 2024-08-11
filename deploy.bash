#!/bin/bash

# Exit on any error and print all commands
set -e
set -x

# Step 0: Ensure Minikube is running
echo "Starting Minikube..."
minikube start -p lpdl --driver=docker || { echo "Failed to start Minikube"; exit 1; }

# Ensure Minikube's Docker daemon is used
echo "Configuring Docker to use Minikube's Docker daemon..."
eval $(minikube -p lpdl docker-env) || { echo "Failed to switch to Minikube's Docker daemon"; exit 1; }

# Step 1: Build Docker Images
echo "Building Docker images for Django app..."
docker build -t django-app ./eshop || { echo "Failed to build Django Docker image"; exit 1; }
echo "Building Docker images for Apache server..."
docker build -t apache-server ./apache || { echo "Failed to build Apache Docker image"; exit 1; }

# Step 3: Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -f ./k8s/django-deployment.yaml || { echo "Failed to apply Django deployment"; exit 1; }
kubectl apply -f ./k8s/django-service.yaml || { echo "Failed to apply Django service"; exit 1; }
kubectl apply -f ./k8s/apache-deployment.yaml || { echo "Failed to apply Apache deployment"; exit 1; }
kubectl apply -f ./k8s/apache-service.yaml || { echo "Failed to apply Apache service"; exit 1; }

# Step 4: Verify deployment
#echo "Checking deployment status for Django deployment..."
#kubectl rollout status deployment/django-deployment || { echo "Django deployment rollout failed"; exit 1; }
#echo "Checking deployment status for Apache server..."
#kubectl rollout status deployment/apache-server || { echo "Apache server deployment rollout failed"; exit 1; }

# Optional: Display all resources
echo "Deployment complete! Check the status with 'kubectl get all'"
kubectl get all
# Step 5: Open the application in the browser (if service type is NodePort and using Minikube)
# Uncomment and modify the following line according to your service name and type if necessary
# minikube service django-service
