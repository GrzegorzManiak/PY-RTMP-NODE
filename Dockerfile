FROM ubuntu:latest


# -- Nginx and the RTMP module
COPY ./scripts/nginx.sh /scripts/nginx.sh
RUN chmod +x /scripts/nginx.sh

# -- Python and its dependencies
COPY ./scripts/python.sh /scripts/python.sh
RUN chmod +x /scripts/python.sh

# -- Run the server
COPY ./scripts/run.sh /scripts/run.sh
RUN chmod +x /scripts/run.sh

# -- Once the Setup is done, we can start the server
COPY ./nginx.conf /scripts/nginx.conf

# CMD ["./run.sh"]
