FROM python:3.9


ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]