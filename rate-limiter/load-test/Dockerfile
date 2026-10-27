
FROM locustio/locust:latest

WORKDIR /mnt/locust

COPY locustfile.py /mnt/locust/locustfile.py

EXPOSE 8089

CMD ["-f", "/mnt/locust/locustfile.py", "--web-host", "0.0.0.0", "--web-base-path", "/locust"]
