FROM python:3.9

ENV LANG=en_US.UTF-8
ENV TZ='Asia/Tokyo'

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /root/app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv sync --system
