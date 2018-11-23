# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /bot
WORKDIR /tasks

# Copy the current directory contents into the container at /bot
COPY . /tasks

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD celery worker -l info -A main
