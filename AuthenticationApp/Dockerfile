# Use official Python image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for efficient caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose the correct port
EXPOSE 5001

# Start the Flask server
CMD ["python", "flask_auth_server.py"]
