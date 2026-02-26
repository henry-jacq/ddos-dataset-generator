FROM python:3.9-slim

# System deps for networking + scapy stability
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    net-tools \
    libpcap-dev \
    tcpdump \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install scapy
RUN pip install --no-cache-dir scapy

WORKDIR /scripts

# Keep container alive
CMD ["tail", "-f", "/dev/null"]