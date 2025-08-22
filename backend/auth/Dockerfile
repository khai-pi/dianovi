# Use official Python slim image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements (if any) first — helps with caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
