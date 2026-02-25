#!/usr/bin/env python3
import subprocess
import sys
import time

COMPOSE_CMD = ["docker", "compose"]   # works for Docker v2


def run(cmd):
    """Run shell command and print output."""
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        sys.exit(1)


def up(scale=None):
    """Start lab containers. Optionally scale attackers."""
    if scale:
        print(f"[+] Starting lab with {scale} attacker(s)")
        run(COMPOSE_CMD + ["up", "-d", "--scale", f"attacker={scale}"])
    else:
        print("[+] Starting lab with default scale")
        run(COMPOSE_CMD + ["up", "-d"])


def down():
    """Stop and remove all containers."""
    print("[+] Stopping lab")
    run(COMPOSE_CMD + ["down"])


def scale_attackers(count):
    """Scale attacker containers dynamically."""
    print(f"[+] Scaling attackers to {count}")
    run(COMPOSE_CMD + ["up", "-d", "--scale", f"attacker={count}"])


def restart():
    """Restart all services."""
    print("[+] Restarting lab")
    run(COMPOSE_CMD + ["restart"])


def status():
    """Show container status."""
    print("[+] Container status:")
    run(COMPOSE_CMD + ["ps"])


def logs(service=None):
    """View logs of specific service or all."""
    if service:
        run(COMPOSE_CMD + ["logs", "-f", service])
    else:
        run(COMPOSE_CMD + ["logs", "-f"])


def usage():
    print("""
Usage:
  orchestrator.py up [num_attackers]
  orchestrator.py down
  orchestrator.py scale <num_attackers>
  orchestrator.py restart
  orchestrator.py status
  orchestrator.py logs [service]

Examples:
  python orchestrator.py up 3
  python orchestrator.py scale 5
  python orchestrator.py down
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

    else:
        usage()


if __name__ == "__main__":
    main()