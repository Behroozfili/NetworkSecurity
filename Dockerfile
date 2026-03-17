# Use an official and lightweight base image
FROM python:3.10-slim-bullseye

# Set appropriate environment variables for an ML runtime
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
# PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal (useful for logging)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required for typical ML and networking packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency files first to maximize Docker layer caching
COPY requirements.txt setup.py ./


# Remove '-e .' from requirements.txt to avoid needing the full source code for dependency installation,
# then install the dependencies
RUN sed -i 's/-e .//g' requirements.txt && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application
COPY . .

# Install the application package itself
RUN pip install --no-cache-dir .

# Expose the port (FastAPI default)
EXPOSE 8000

# Specify the entrypoint to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
