# Use official Python image
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .
COPY config/ ./config/

EXPOSE 3000

CMD ["python", "app.py"]
