FROM centos/python-36-centos7

ARG DB_CRYPT_KEY

LABEL source="githuburl" \
      maintainer="k-batista"

EXPOSE 5005

COPY . /raven/

WORKDIR /raven/

#local install without index-url and trusted host
RUN pip3 install --no-index --find-links pkg/ -r requirements.txt
# RUN pip3 install -r requirements.txt 

ENV DYNACONF_DB_CRYPT__KEY=$DB_CRYPT_KEY

ENV BOOT_PARAMS="--preload --bind 0.0.0.0:5000 --worker-class=gevent --worker-connections=1000 app.application:app"

ENTRYPOINT ["sh", "-c", "gunicorn $BOOT_PARAMS"]