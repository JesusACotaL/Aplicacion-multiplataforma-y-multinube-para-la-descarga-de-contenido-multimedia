# Debian with python pre installed 
# https://hub.docker.com/_/python
FROM python:3.8-slim
# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True
ENV PORT 5000
# Copy local code to the container image.
WORKDIR /app
COPY . ./
# Update sources.list
RUN apt update -y
# Install python dependencies for pip
RUN apt install -y build-essential python3-dev libffi-dev
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
# Run the web service on container startup. Here we use the gunicorn WSGI webserver
# For environments with multiple CPU cores, increase the number of workers to be equal to the cores available. 
# example: --workers 1 --threads 8
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
RUN pip install --no-cache-dir gunicorn
CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 main:app
EXPOSE ${PORT}