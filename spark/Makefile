# include .env
# export $(shell sed 's/=.*//' .env)

re:
	rm -rf ml_service/target/ && \
	cd ml_service && sbt assembly && \
	cd .. &&  /home/konsin1988/spark-3.5.6-bin-hadoop3-scala2.13/bin/spark-submit  --class com.konsin1988.Main \
		ml_service/target/scala-2.13/ml_service-assembly-1.0.0.jar

up:
	docker compose -f docker-compose-spark.yml up

down: 
	docker compose -f docker-compose-spark.yml down
