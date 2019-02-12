FROM python:3.7
MAINTAINER logileifs <logileifs@gmail.com>

ADD . /app

EXPOSE 8000

WORKDIR /app
RUN pip3 install pipenv
RUN pipenv install --system

CMD ["python", "-m", "lemo"]