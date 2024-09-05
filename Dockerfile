###########
# BUILDER #
###########

# pull official base image
FROM python:3.12-bookworm as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y libsnmp-dev libzmq3-dev libczmq-dev


RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip wheel --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip wheel --no-deps --wheel-dir /usr/src/app/wheels gunicorn mysqlclient

#########
# FINAL #
#########

FROM python:3.12-bookworm

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web

# install system dependencies
RUN apt-get update && apt-get install -y libsnmp-dev libzmq3-dev libczmq-dev

RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

EXPOSE 8000

# Start gunicorn
ENTRYPOINT ["gunicorn"]