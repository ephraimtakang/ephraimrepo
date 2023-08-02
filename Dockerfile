# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port on which Flask will run
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
