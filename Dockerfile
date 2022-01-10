FROM python:3.10.1-alpine3.15
LABEL maintainer = "Jonathan Gibbons"

# Sets python to unbuffered mode, removes complications when running python in docker
ENV PYTHONUNBUFFERED 1

# Make empty folder and copy into it the code for the django application
COPY ./app /app
# Copy and run install of required python libraries in docker container
COPY ./requirements.txt /app/requirements.txt

# Set working directory to directory with Django app
WORKDIR /app

# Expose the port in the container that will listen for the Django application
EXPOSE 8000

# Create python virtual environment to house all dependencies of web app
# Upgrade the package manager and install all requirements from requirements file
# Add a user for the app to run on in the container
# Security consideration: Prevents running of Django application as root
# Installs the postgres drivers and removes the unecessary postgres dependencies to keep the image lightweight
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home wmgtss

# Add the python virtual environment to the path
ENV PATH="/py/bin:$PATH"

# Switch to unpriviledged user
USER wmgtss