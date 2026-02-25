
# CICFlowMeter 

---

# 🎯 Objective

Build a stable pipeline:

```
PCAP capture → CICFlowMeter → Flow CSV
```

---

# 🖥️ Environment

* Ubuntu 20.04 / 22.04
* Java 8 (required)
* Network interface example: `enp2s0`
* Working directory example:

  ```
  ~/playground/threatwatch/ddos-dataset-gen/
  ```

---

# 1️⃣ Install System Dependencies

## Install Java 8 (Critical)

Gradle 4.2 does NOT support Java 21.

```bash
sudo apt update
sudo apt install openjdk-8-jdk git maven tcpdump
```

Verify:

```bash
java -version
```

If multiple Java versions exist:

```bash
sudo update-alternatives --config java
```

Select Java 8.

---

# 2️⃣ Clone Official CICFlowMeter

Repository:

Canadian Institute for Cybersecurity
Project:

CICFlowMeter

```bash
cd ~/playground/threatwatch/ddos-dataset-gen/
git clone https://github.com/ahlashkari/CICFlowMeter.git
cd CICFlowMeter
```

---

# 3️⃣ Install jNetPcap (Native Dependency)

CICFlowMeter depends on jNetPcap 1.4.1.

```bash
cd jnetpcap/linux/jnetpcap-1.4.r1425

sudo mvn install:install-file \
  -Dfile=jnetpcap.jar \
  -DgroupId=org.jnetpcap \
  -DartifactId=jnetpcap \
  -Dversion=1.4.1 \
  -Dpackaging=jar
```

Return:

```bash
cd ../../../..
```

---

# 4️⃣ Build Project

```bash
chmod +x gradlew
./gradlew clean build
```

If successful → Gradle + Java config is correct.

---

# 5️⃣ Modify CLI Execution (Required Fix for Gradle 4.2)

Open `build.gradle` and update the `exeCMD` task:

```gradle
task exeCMD(type: JavaExec){
    main = "cic.cs.unb.ca.ifm.Cmd"
    classpath = sourceSets.main.runtimeClasspath

    if (project.hasProperty("input") && project.hasProperty("output")) {
        args project.property("input"), project.property("output")
    }

    String osName = System.getProperty('os.name').toLowerCase()
    if(osName.contains('windows')){
        jvmArgs '-Djava.library.path=jnetpcap/win/jnetpcap-1.4.r1425'
    }else{
        jvmArgs '-Djava.library.path=jnetpcap/linux/jnetpcap-1.4.r1425'
    }
}
```

Save.

---

# 6️⃣ Create Application Distribution

```bash
./gradlew installDist
```

This generates:

```
build/install/CICFlowMeter/bin/cfm
```

This is the stable executable entry point.

---

# 7️⃣ Capture Network Traffic (PCAP)

Start capture:

```bash
sudo tcpdump -i enp2s0 -s 0 -w capture.pcap
```

Generate traffic in another terminal:

```bash
curl http://example.com
wget http://speedtest.tele2.net/1MB.zip
ping 8.8.8.8
```

Stop tcpdump (Ctrl+C).

---

# 8️⃣ Convert PCAP → Flow CSV (Final Working Command)

This is the **confirmed working command**:

```bash
sudo JAVA_OPTS="-Djava.library.path=jnetpcap/linux/jnetpcap-1.4.r1425" \
build/install/CICFlowMeter/bin/cfm capture.pcap output
```

(Replace with your filename properly.)

---

# ⚠️ Known Limitations (Important)

* jNetPcap is outdated
* Native library is fragile
* Not ideal for production
* Strict flow termination logic
* Does not scale to large PCAPs easily

For research baseline → fine
For production IDS → not ideal

---

# 🔁 Minimal Recreation Commands (Condensed)

```bash
sudo apt update
sudo apt install openjdk-8-jdk git maven tcpdump

git clone https://github.com/ahlashkari/CICFlowMeter.git
cd CICFlowMeter

cd jnetpcap/linux/jnetpcap-1.4.r1425
sudo mvn install:install-file -Dfile=jnetpcap.jar \
-DgroupId=org.jnetpcap -DartifactId=jnetpcap \
-Dversion=1.4.1 -Dpackaging=jar
cd ../../../..

chmod +x gradlew
./gradlew clean build
./gradlew installDist

sudo tcpdump -i enp2s0 -s 0 -w capture.pcap

sudo JAVA_OPTS="-Djava.library.path=jnetpcap/linux/jnetpcap-1.4.r1425" \
build/install/CICFlowMeter/bin/cfm capture.pcap output.csv
```

