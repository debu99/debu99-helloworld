FROM python:3-alpine
RUN apk --no-cache upgrade && pip3 install --no-cache flask
COPY helloworld.py /app/
CMD ["/usr/local/bin/python3", "/app/helloworld.py"]
