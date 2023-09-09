
# base image  
FROM python:3.9-alpine
RUN apk update && apk add haproxy
RUN apk update && apk add supervisor

# setup environment variable  
ENV DockerHOME=/home/app/musalla

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Haproxy app runs  
EXPOSE 8001  

COPY haproxy.cfg /etc/haproxy/haproxy.cfg
# Add supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Migration
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["/usr/bin/supervisord"]

