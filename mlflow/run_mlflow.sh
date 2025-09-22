#!/bin/bash
set -e

containers=(
    "ml-postgres"
    "ml-minio"
)

echo "-- Start mlflow... --"

for container in "${containers[@]}"; do
    echo "Wait for $container..."
    until [ "$(docker inspect -f '{{.State.Health.Status}}' "$container" 2>/dev/null)" == "healthy" ]; do
	status=$(docker inspect -f '{{.State.Health.Status}}' "$container" 2>/dev/null || echo "not found")
	echo "$container in $status status"
	sleep 3
    done

    echo "  -- $container healthy!"
done

echo "All waited containers healthy"

docker compose -f ./mlflow/docker-compose.yml --env-file ./.env up -d
