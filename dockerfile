FROM python:3.11-slim

WORKDIR /app

# This now matches your renamed requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# This copies the app folder you just created
COPY app/ ./app/

# This copies the artifacts folder you just created
COPY artifacts/ ./artifacts/

EXPOSE 8000

# Note: Make sure the path to your FastAPI app matches where app.py is located
# If your FastAPI instance is named "app" inside app.py, use app.app:app
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]