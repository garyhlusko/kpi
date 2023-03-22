FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/kpi
WORKDIR /code
RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN python -m pip install -r /code/requirements.txt
COPY ./sunflower /code/kp

EXPOSE 8000