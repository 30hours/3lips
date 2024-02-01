FROM python:3.9-slim

WORKDIR /app
COPY src /app

# install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# make port 5000 available to the world outside this container
EXPOSE 5000

# define environment variable
ENV FLASK_APP=main.py

# run Gunicorn instead of the default Flask development server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
