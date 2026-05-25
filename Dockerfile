# Step 1: Use an official, lightweight Python base image
FROM python:3.11-slim-bookworm

# Step 2: Set environment variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (critical for clean logs in CI/CD)
ENV PYTHONUNBUFFERED=1

# Step 3: Establish the working directory inside the container
WORKDIR /app

# Step 4: Install dependencies
# We copy only the requirements first to leverage Docker's caching layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application source code
COPY app.py .

# Step 6: REMEDIATION FOR "missing-user"
# Create a non-privileged system user and group to run the application
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
# Change ownership of the application directory to the new user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user context
USER appuser

# Step 7: Expose the network port the Flask app binds to
EXPOSE 5000

# Step 8: Define the execution command
# We use host 0.0.0.0 to allow the container to accept external traffic
CMD ["python", "app.py"]
