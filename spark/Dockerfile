# Use a base image with Java 11
FROM openjdk:11-jdk-slim

# Set environment variables for Spark
ENV SPARK_VERSION=3.5.7
ENV HADOOP_VERSION=3
ENV SCALA_VERSION=2.13

RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Download and extract Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}-scala${SCALA_VERSION}.tgz -O /tmp/spark.tgz \
    && tar -xzf /tmp/spark.tgz -C /opt \
    && rm /tmp/spark.tgz \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}-scala${SCALA_VERSION} /opt/spark

# Set Spark Home
ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

# Expose Spark UI port (optional, adjust as needed)
EXPOSE 8080 7077

# Set working directory
WORKDIR /opt/spark

# You can add further configurations or applications here
# For example, to run a Spark application:
# CMD ["spark-submit", "--class", "com.example.MyApp", "my_app.jar"]

# Or to run a Spark shell:
# CMD ["spark-shell"]
