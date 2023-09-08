FROM python:latest

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils default-jdk gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY submission_evaluation.py .

CMD ["python3", "submission_evaluation.py"]
