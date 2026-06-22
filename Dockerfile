# Step 1 — Start from official Python image
FROM python:3.12-slim

# Create non-root user — security best practice
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Step 2 — Set working directory inside container
WORKDIR /app

# Step 3 — Copy requirements first (for caching)
COPY requirements.txt .

# Step 4 — Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5 — Copy your application code
COPY . .

# Give ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Step 6 — Tell Docker which port the app uses
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Step 7 — Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]