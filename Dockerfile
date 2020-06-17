FROM centos/python-36-centos7

LABEL maintainer="k-batista"

COPY . /raven/

WORKDIR /raven/

RUN pip3 install -r requirements.txt 

# ENV BOOT_PARAMS="--bind 0.0.0.0:5000 --worker-class=gevent --worker-connections=1000 app.application:app"

# ENTRYPOINT ["sh", "-c", "gunicorn $BOOT_PARAMS"]

CMD gunicorn --bind 0.0.0.0:$PORT --worker-class=gevent --worker-connections=1000 app.application:app