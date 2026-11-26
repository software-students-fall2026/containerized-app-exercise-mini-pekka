FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# Set the working directory within the image to /app
WORKDIR /app

# in Python, a requirements.txt file is a way of indicating dependencies in a way that the package manager, pip, can understand
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser
USER appuser
# Make port 5000 available to the world outside this container
EXPOSE 5000
# Run app.py when the container launches
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
