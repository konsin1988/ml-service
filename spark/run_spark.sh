docker exec -it ml-spark spark-submit --class Main target/scala-2.13/test_2.13-0.0.1.jar

/home/konsin1988/spark-3.5.6-bin-hadoop3-scala2.13/bin/spark-submit       --class Main       --jars ./test_spark/click-jar/clickhouse-jdbc-0.8.5.jar       test_spark/target/scala-2.13/hello-world_2.13-1.0.jar
