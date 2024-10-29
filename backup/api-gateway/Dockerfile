# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the local ./app directory into the /app directory in the container
COPY ./app /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_WARN_SCRIPT_LOCATION=0 \
    PIP_PROGRESS_BAR=off

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# Expose the port 8000 to the outside world
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
