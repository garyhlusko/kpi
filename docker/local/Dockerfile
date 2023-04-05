FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/kpi
WORKDIR /code
RUN pip install --upgrade pip
COPY ./kpi/requirements.txt /code/
RUN python -m pip install -r /code/requirements.txt
COPY ./kpi /code/kpi/
RUN file="$(ls -1 /code/kpi)" && echo $file
WORKDIR /code/kpi
EXPOSE 8000
