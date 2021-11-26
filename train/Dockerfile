FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime

ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /code
COPY . .

CMD ["python", "train.py"]