
# 🔹 Basic Capture (Verbose + Save to File)

```bash
tcpdump -i eth0 -nn -vv -w capture.pcap
```

* `-nn` → don’t resolve DNS/ports (faster)
* `-vv` → verbose
* `-w file` → write to pcap

---

# 🔥 TCP Filters

### Capture All TCP

```bash
tcpdump -i eth0 tcp -nn -vv
```

### Specific TCP Port (e.g., 80)

```bash
tcpdump -i eth0 tcp port 80 -nn -vv
```

### Source Port

```bash
tcpdump -i eth0 tcp src port 443 -nn
```

### Destination Port

```bash
tcpdump -i eth0 tcp dst port 22 -nn
```

### TCP SYN Packets (detect scans/flood)

```bash
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0' -nn
```

### TCP RST Packets

```bash
tcpdump -i eth0 'tcp[tcpflags] & tcp-rst != 0' -nn
```

---

# 🔥 UDP Filters

### All UDP

```bash
tcpdump -i eth0 udp -nn -vv
```

### Specific UDP Port

```bash
tcpdump -i eth0 udp port 53 -nn
```

### Possible UDP Flood (high packet rate)

```bash
tcpdump -i eth0 udp -nn -tttt -vv -w udp_flood.pcap
```

(Add `-c 1000` to limit packets)

---

# 🌐 DNS Filters

### DNS (UDP 53)

```bash
tcpdump -i eth0 udp port 53 -nn -vv
```

### DNS Over TCP

```bash
tcpdump -i eth0 tcp port 53 -nn -vv
```

### Show DNS Queries Only

```bash
tcpdump -i eth0 udp port 53 and 'udp[10] & 0x80 = 0' -nn
```

---

# 🌍 HTTP Filters

### HTTP (Port 80)

```bash
tcpdump -i eth0 tcp port 80 -nn -A
```

* `-A` → print ASCII payload

### HTTP Methods Only (GET/POST)

```bash
tcpdump -i eth0 -nn -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

(Simpler version:)

```bash
tcpdump -i eth0 -nn -A tcp port 80 | grep -E "GET|POST"
```

---

# 🔐 HTTPS (TLS)

```bash
tcpdump -i eth0 tcp port 443 -nn
```

Show TLS handshake:

```bash
tcpdump -i eth0 'tcp port 443 and (tcp[tcpflags] & tcp-syn != 0)' -nn
```

---

# 🖥 Capture by Host

### Specific IP

```bash
tcpdump -i eth0 host 192.168.1.10
```

### Source IP

```bash
tcpdump -i eth0 src 192.168.1.10
```

### Destination IP

```bash
tcpdump -i eth0 dst 8.8.8.8
```

---

# 🔁 Combine Filters

### TCP + UDP

```bash
tcpdump -i eth0 '(tcp or udp)' -nn
```

### HTTP or HTTPS

```bash
tcpdump -i eth0 'tcp port 80 or tcp port 443' -nn
```

### DNS from Specific Host

```bash
tcpdump -i eth0 'host 192.168.1.5 and port 53' -nn
```

---

# 📦 Capture and Save with Filter

Example: Capture DNS traffic to file:

```bash
tcpdump -i eth0 udp port 53 -nn -vv -w dns_capture.pcap
```

---

# 🚨 DDoS / Flood Detection Examples

### SYN Flood Detection

```bash
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0 and not tcp[tcpflags] & tcp-ack != 0'
```

### ICMP Flood

```bash
tcpdump -i eth0 icmp -nn
```

### Large Packet Detection

```bash
tcpdump -i eth0 'greater 1000'
```

---

# 🛠 Useful Options

* `-c 100` → capture only 100 packets
* `-s 0` → capture full packet
* `-tttt` → readable timestamp
* `-A` → ASCII payload
* `-X` → hex + ASCII
* `-e` → show MAC addresses
