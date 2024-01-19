FROM apache/airflow:2.2.4-python3.8


USER root


RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends vim && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow


RUN pip install pandas

ENV PYTHONPATH "${PYTHONPATH}:/src"

