# Используем готовый образ Spark с Hadoop и OpenJDK 17
FROM bitnami/spark:3.5.0

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем sbt (если нужен для сборки внутри контейнера)
USER root
RUN apt-get update && \
    apt-get install -y curl gnupg2 && \
    curl -L https://github.com/sbt/sbt/releases/download/v1.9.4/sbt-1.9.4.tgz | tar xz -C /usr/local && \
    ln -s /usr/local/sbt/bin/sbt /usr/bin/sbt

