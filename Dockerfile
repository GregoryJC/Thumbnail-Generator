FROM python:3.8

WORKDIR /thumbnail_generator
ADD . /thumbnail_generator
CMD /bin/sh -x run.sh
EXPOSE 630