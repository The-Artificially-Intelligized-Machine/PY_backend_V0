# Use the official Python image from the Docker Hub
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Ensure vectorDB is declared as a volume
VOLUME /app/vectorDB

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["fastapi", "run", "app.py"]
