up:
	docker compose -f ./store/docker-compose.yml --env-file ./.env up -d && \
		./init/run_init.sh  
	#	./mlflow/run_mlflow.sh && \
	#	./airflow/run_airflow.sh

down:
	docker compose -f ./airflow/docker-compose.yml --env-file ./.env down && \
	docker compose -f ./mlflow/docker-compose.yml --env-file ./.env down && \
	docker compose -f ./store/docker-compose.yml --env-file ./.env down && \
	docker rm ml-init

