FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y nano sudo apt-utils python-dev-is-python3 \
    openssh-server dos2unix telnet inetutils-ping pylint postgresql-client

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile --system

EXPOSE 8000
