FROM python:3.10-alpine AS base

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Ensure the entrypoint script has execute permissions
RUN chmod +x entrypoint.sh

# Run the application
ENTRYPOINT ["./entrypoint.sh"]
