# led_drumkit

###### By

## Description

Credit to Stephen Colfer whom this is forked from. I have made significant changes. For more info on the project check out the video: https://youtu.be/ctKZRcTf2wk

## 📌 Materials

- Raspberry Pi 3 (what I used)
- WS2812 RGB LED Strip (or similar strip with individually addressable LEDs)
- Power supply suitable for the LED strip (10A per 300 5V LEDs)
- Drum kit capable of MIDI note output (Mine is a TD17)

# LED Drumkit - Raspberry Pi Setup Guide

This guide provides step-by-step instructions to set up the `led_drumkit` project on a **fresh Raspberry Pi installation**.

## 📌 Prerequisites

- A Raspberry Pi (any model with GPIO support)
- Raspbian (Raspberry Pi OS) installed
- Internet connection

---

## 🛠️ 1. Update & Upgrade the Raspberry Pi

Ensure your system is up-to-date:

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

---

## 📦 2. Install Required System Packages

Install dependencies for **Python, MIDI, GPIO, and Audio**:

```bash
sudo apt-get install -y python3 python3-pip python3-rpi.gpio libasound2-dev libjack-dev portaudio19-dev
```

---

## 📥 3. Clone the Repository

Download the `led_drumkit` project:

```bash
git clone https://github.com/mcorkum/led_drumkit.git
cd led_drumkit
```

---

## 🚀 4. Install Python Dependencies System-Wide

Since we are running with `sudo`, install all Python dependencies globally:

```bash
sudo pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel
sudo pip3 install --no-cache-dir --break-system-packages -r requirements.txt
```

If `rpi_ws281x` is not in `requirements.txt`, install it explicitly:

```bash
sudo pip3 install --no-cache-dir --break-system-packages rpi-ws281x
```

---

## 🔇 5. Disable Onboard Audio (Required for LED Control)

The `rpi_ws281x` library **uses PWM**, which conflicts with onboard audio. Disable it:

```bash
echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/snd-blacklist.conf
```

_(This prevents interference between PWM and the Raspberry Pi’s default sound system.)_

**Optional: Force HDMI Audio (For Headless Systems)**

```bash
sudo sed -i '$a hdmi_force_hotplug=1\nhdmi_force_edid_audio=1' /boot/config.txt
```

This ensures HDMI audio works even if no monitor is plugged in.

---

## 🔄 6. Reboot the System

After installing all dependencies, reboot the Raspberry Pi:

```bash
sudo reboot
```

---

## 🥁 7. Run the Drumkit Code (Always Use `sudo`)

Since `rpi_ws281x` requires root access, always run the script with `sudo`:

```bash
cd led_drumkit
sudo python3 main.py
```

---

## 🔄 8. Start the Drumkit Script on Boot

To automatically start the LED Drumkit script when the Raspberry Pi boots, use `systemd`.

### **✅ 1. Create a Systemd Service File**

Run:

```bash
sudo nano /etc/systemd/system/led_drumkit.service
```

Paste the following content:

```ini
[Unit]
Description=LED Drumkit Service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/led_drumkit/main.py
WorkingDirectory=/home/pi/led_drumkit
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

> **Ensure** the `ExecStart` path matches your Python installation and script location.

Save and exit (**CTRL + X → Y → ENTER**).

### **✅ 2. Enable & Start the Service**

Run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable led_drumkit.service
sudo systemctl start led_drumkit.service
```

To check if it's running:

```bash
sudo systemctl status led_drumkit.service
```

### **✅ 3. (Optional) Auto Restart on Crash**

If you want the script to restart automatically if it crashes, ensure this line is in the `[Service]` section:

```
Restart=always
```

Then reload systemd:

```bash
sudo systemctl daemon-reload
sudo systemctl restart led_drumkit.service
```

### **✅ 4. (Optional) Disable Autostart**

To stop it from running on boot, disable it with:

```bash
sudo systemctl disable led_drumkit.service
sudo systemctl stop led_drumkit.service
```
