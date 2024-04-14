# Use the official Python image as base
FROM python:3.11

# Set environment variables
ENV FLASK_APP=connection.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that Flask is running on
EXPOSE 5000

# Command to run on container start
CMD ["flask", "run"]
