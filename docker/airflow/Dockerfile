FROM apache/airflow:3.0.6

USER root
RUN apt-get update \
   && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      git \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

USER airflow

COPY ./docker/airflow/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /opt/airflow
