FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    tcpdump \
    iputils-ping \
    net-tools \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

CMD ["tail", "-f", "/dev/null"]