#!/bin/bash
set -ex
poetry export --only main -f requirements.txt --output requirements.txt

TAG=$(git rev-parse --short HEAD || echo "unknown")
echo "Building Docker image with tag: ${TAG}"
docker build . -t scalasmhmh/my-hello-mcp-server:${TAG} -t scalasmhmh/my-hello-mcp-server:latest
docker push scalasmhmh/my-hello-mcp-server:${TAG}
