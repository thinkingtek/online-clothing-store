FROM python:3.12.6-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /code

COPY reqs.txt /code/

# Install dependencies

RUN apt-get update && apt-get install -y cron
RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install -r reqs.txt

COPY . /code/

# Add crontab file to the cron directory

COPY crontab /etc/cron.d/unverified_users_cron

# Set up cron job log file

RUN touch /var/log/cron.log

# Give execution rights on the cron job

RUN chmod 0644 /etc/cron.d/unverified_users_cron

# Create the log file to be able to run tail

RUN touch /var/log/cron.log

# CMD cron && tail -f /var/log/cron.log

# RUN crontab /etc/cron.d/unverified_users_cron

# Set the command to run the management command

# CMD [ "cron", "-f" ]

CMD cron && tail -f /var/log/cron/log/cron.log

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
