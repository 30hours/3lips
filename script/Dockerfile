# use an official Python runtime as a parent image
FROM python:3.9-slim

# set the working directory to /app
WORKDIR /app

# install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

