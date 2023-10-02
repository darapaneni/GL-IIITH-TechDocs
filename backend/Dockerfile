FROM python:3.9-slim
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /app
CMD gunicorn --bind 0.0.0.0:5000 --chdir /app app:app
