FROM python:3.10-slim-bookworm
RUN apt-get update && apt-get -y install cron vim libpq-dev gcc 

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt



COPY crontab /etc/cron.d/crontab
COPY core_etl.py /app/core_etl.py
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab



CMD ["/bin/bash", "-c", "printenv > /etc/environment && cron -f"]