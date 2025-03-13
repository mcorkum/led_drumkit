# led_drumkit

###### By Stephen Colfer

## Description

Turn your drumkit into a light show! By mounting an led strip to your drums you can use this code to control the strip through MIDI. With the correct setup the LEDs will react to the midi drum pads. This repo also includes the code for an optional web app to control the LED colours. Follow the steps here in the README for materials and setup. For more info on the project check out the video: https://youtu.be/ctKZRcTf2wk

## Materials

- Raspberry Pi
- [WS2812 RGB LED Strip](https://www.amazon.co.uk/CHINLY-WS2812B-Individually-Addressable-Waterproof/dp/B01LSF4Q0A?pd_rd_w=Y8qio&pf_rd_p=907ba819-1a37-4335-8b84-d82a78945ade&pf_rd_r=XJJKR5NCNPWB7S3EAEC3&pd_rd_r=6c6d6a0f-9829-4747-8fee-2d0778cb1b8d&pd_rd_wg=QvtLt&pd_rd_i=B01LSF4Q0A&psc=1&ref_=pd_bap_d_rp_2_t) (or similar strip with individually addresable LEDs)
- [Power supply suitedable](https://www.amazon.co.uk/gp/product/B07C4SNYCH/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) for the LED strip. 10A per 300 5v leds in this case.
- Drum kit capable of MIDI note output (electric drumkit or acoustic with triggers)
- (Optional) [Aluminium LED channel](https://www.amazon.co.uk/Chesbung-Aluminum-Channels-Diffusers-Mounting/dp/B07RJVV9MY?pd_rd_w=TNSWg&pf_rd_p=508c5101-ccd9-46e7-b139-f5fa5b359865&pf_rd_r=BYKFHRAD8NJNQ7T5TBR3&pd_rd_r=4dde0c46-0170-4a38-af65-c321c9e4feb1&pd_rd_wg=nqF4R&psc=1&ref_=pd_bap_d_csi_vtp_0_t) for mounting to stands.
- (Optional) [Useful power connectors](https://www.amazon.co.uk/gp/product/B01JZ3O36O/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
- (Optional) [No solder strip connectors](https://www.amazon.co.uk/gp/product/B08FHXW4G5/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1)

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

## 🎉 Conclusion

Following these steps, you should have a fully working **LED Drumkit** setup on your Raspberry Pi using `sudo` and `--break-system-packages`. Happy drumming! 🥁✨
