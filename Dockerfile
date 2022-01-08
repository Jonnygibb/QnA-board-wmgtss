FROM python:3.10.1-alpine3.15
LABEL org.opencontainers.image.authors = "Jonnygibb"

# Sets python to unbuffered mode, removes complications when running python in docker
ENV PYTHONUNBUFFERED 1

# Copy and run install of required python libraries in docker container
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Make empty folder and copy into it the code for the django application
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create a user for running apps only and switch to it
# Security consideration: Prevents running of Django application as root
RUN adduser -D wmgtss
USER wmgtss