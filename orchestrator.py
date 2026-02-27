#!/usr/bin/env python3
import subprocess
import sys
import shlex
import signal
import os
from concurrent.futures import ThreadPoolExecutor

COMPOSE_CMD = ["docker", "compose"]
ACTIVE_PROCESSES = []


# Signal Handling

def shutdown_handler(signum, frame):
    print("\n[!] Interrupt received. Stopping all running commands...")

    for p in ACTIVE_PROCESSES:
        try:
            if p.poll() is None:
                print(f"[+] Terminating PID {p.pid}")
                p.send_signal(signal.SIGINT)
        except Exception:
            pass

    for p in ACTIVE_PROCESSES:
        try:
            p.wait(timeout=5)
        except:
            p.kill()

    print("[+] Cleanup complete")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# Utility

def run(cmd, check=True):
    result = subprocess.run(cmd, text=True)
    if check and result.returncode != 0:
        print(f"[!] Command failed: {' '.join(cmd)}")
        sys.exit(1)
    return result


def get_container_ids(service):
    result = subprocess.run(
        COMPOSE_CMD + ["ps", "-q", service],
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        print(f"[!] Failed to get containers for {service}")
        sys.exit(1)

    return result.stdout.strip().splitlines()


# Docker Exec with Signal Control

def exec_on_container(container_id, cmd_args):
    full_cmd = ["docker", "exec", container_id] + cmd_args

    process = subprocess.Popen(full_cmd)
    ACTIVE_PROCESSES.append(process)

    return process


def docker_exec_on_attackers(cmd_string):
    container_ids = get_container_ids("attacker")

    if not container_ids:
        print("[!] No attacker containers found")
        return

    cmd_args = shlex.split(cmd_string)

    print(f"[+] Executing on {len(container_ids)} attacker(s)")

    processes = []

    for cid in container_ids:
        print(f"[+] {cid} -> {cmd_string}")
        p = exec_on_container(cid, cmd_args)
        processes.append(p)

    # Wait for all processes
    for p in processes:
        p.wait()


def docker_exec_on_victim(cmd_string):
    container_ids = get_container_ids("victim")

    if not container_ids:
        print("[!] No victim container found")
        return

    cmd_args = shlex.split(cmd_string)

    cid = container_ids[0]
    print(f"[+] Executing on victim {cid}: {cmd_string}")

    p = exec_on_container(cid, cmd_args)
    p.wait()


# Compose Controls

def up(scale=None):
    if scale:
        print(f"[+] Starting lab with {scale} attacker(s)")
        run(COMPOSE_CMD + ["up", "-d", "--scale", f"attacker={scale}"])
    else:
        print("[+] Starting lab")
        run(COMPOSE_CMD + ["up", "-d"])


def down():
    print("[+] Stopping lab")
    run(COMPOSE_CMD + ["down"])


def scale_attackers(count):
    print(f"[+] Scaling attackers to {count}")
    run(COMPOSE_CMD + ["up", "-d", "--scale", f"attacker={count}"])


def restart():
    print("[+] Restarting lab")
    run(COMPOSE_CMD + ["restart"])


def status():
    print("[+] Container status:")
    run(COMPOSE_CMD + ["ps"])


def logs(service=None):
    if service:
        run(COMPOSE_CMD + ["logs", "-f", service])
    else:
        run(COMPOSE_CMD + ["logs", "-f"])


# CLI

def usage():
    print("""
Usage:
  orchestrator.py up [num_attackers]
  orchestrator.py down
  orchestrator.py scale <num_attackers>
  orchestrator.py restart
  orchestrator.py status
  orchestrator.py logs [service]
  orchestrator.py exec-attacker <command>
  orchestrator.py exec-victim <command>
""")


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "up":
        scale = int(sys.argv[2]) if len(sys.argv) > 2 else None
        up(scale)

    elif cmd == "down":
        down()

    elif cmd == "scale":
        if len(sys.argv) != 3:
            usage()
            sys.exit(1)
        scale_attackers(int(sys.argv[2]))

    elif cmd == "restart":
        restart()

    elif cmd == "status":
        status()

    elif cmd == "logs":
        service = sys.argv[2] if len(sys.argv) > 2 else None
        logs(service)

    elif cmd == "exec-attacker":
        if len(sys.argv) < 3:
            usage()
            sys.exit(1)
        docker_exec_on_attackers(" ".join(sys.argv[2:]))

    elif cmd == "exec-victim":
        if len(sys.argv) < 3:
            usage()
            sys.exit(1)
        docker_exec_on_victim(" ".join(sys.argv[2:]))

    else:
        usage()


if __name__ == "__main__":
    main()