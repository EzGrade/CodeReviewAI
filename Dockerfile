FROM python:3.10-alpine as base

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

RUN chmod +x entrypoint.sh

# Run the application
CMD ["/app/entrypoint.sh"]