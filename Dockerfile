FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY src/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code including start.sh
COPY src /code

# Make start.sh executable
RUN chmod +x /code/start.sh

# Expose app port
EXPOSE 5000

# Run your custom start script
ENTRYPOINT ["/code/start.sh"]
