FROM python:3.11.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

CMD ["sleep", "infinity"]
# CMD ["flask", "run", "--host=0.0.0.0"]
