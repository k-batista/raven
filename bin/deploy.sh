#!/bin/sh

docker build -t raven . 
heroku container:push web --app ravensp
heroku container:release web --app ravensp