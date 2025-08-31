#!/bin/bash
set -e

CLUSTER_NAME="devops-test-cluster"

echo "Creating Kind cluster: $CLUSTER_NAME ..."

# Delete existing cluster if exists
kind delete cluster --name $CLUSTER_NAME || true

# Create new cluster
kind create cluster --name $CLUSTER_NAME --config=cluster-config.yaml

echo "Kind cluster '$CLUSTER_NAME' created successfully!"
kubectl cluster-info --context kind-$CLUSTER_NAME
