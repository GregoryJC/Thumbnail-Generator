FROM python:3.8

ADD logs/  /
ADD examples/  /
ADD finished/  /
ADD config.py /
ADD server.py /
COPY requirements.txt /
COPY run.sh /

CMD /bin/sh -x run.sh

EXPOSE 630