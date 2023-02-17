FROM ubuntu:latest

COPY ./scripts/nginx.sh /scripts/nginx.sh
COPY ./scripts/python.sh /scripts/python.sh
COPY ./scripts/run.sh /scripts/run.sh

RUN chmod +x /scripts/run.sh
RUN chmod +x /scripts/nginx.sh
RUN chmod +x /scripts/python.sh

CMD ["./run.sh"]

# HOST : CONTAINER

# -- API
EXPOSE 8000:80

# -- NGINX RTMP
EXPOSE 1935:1935 