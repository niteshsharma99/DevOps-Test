#!/bin/bash
set -e

REGISTRY_NAME="kind-registry"
REGISTRY_PORT="5000"

# Start registry container if not running
if [ "$(docker ps -q -f name=$REGISTRY_NAME)" ]; then
  echo "Registry already running."
else
  docker run -d --restart=always -p ${REGISTRY_PORT}:5000 --name ${REGISTRY_NAME} registry:2
  echo "Local Docker registry started on localhost:${REGISTRY_PORT}"
fi

# Connect registry to Kind cluster
kubectl get configmap local-registry-hosting -n kube-public >/dev/null 2>&1 || \
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:${REGISTRY_PORT}"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF
