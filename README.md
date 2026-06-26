# Raspberry_pi proj1
# ⏰ Raspberry Pi Smart Alarm with RGB LED & Music Sync

## 📌 Overview
This project is a Raspberry Pi-based smart alarm system that:
- Triggers on a button press
- Uses a DS1307 RTC to log trigger time
- Plays a Jingle Bells melody on a buzzer
- Syncs RGB LED colors with music beats

---

## ✅ Important Note
This project uses a **KY-009 RGB LED module**, which includes built-in current-limiting resistors.

✔ No external resistors are required  
✔ Safe to connect directly to GPIO pins  

---

## 🔧 Hardware Components

- Raspberry Pi (GPIO-enabled, Pi 3/4 recommended)
- Push Button (momentary)
- KY-006 Passive Buzzer
- KY-009 RGB LED Module (Common Cathode)
- DS1307 RTC Module (I2C)
- Jumper wires

---
## 🔌 Hardware Connections (BCM Mode)

| Component | Pin Connection |
|----------|----------------|
| Button | GPIO 27 ↔ GND |
| Buzzer (KY-006) | GPIO 17 (Signal) |
| RGB LED (KY-009) R | GPIO 18 |
| RGB LED (KY-009) G | GPIO 23 |
| RGB LED (KY-009) B | GPIO 24 |
| RGB LED (KY-009 GND) | GND |
| RTC SDA | GPIO 2 |
| RTC SCL | GPIO 3 |
| RTC VCC | 3.3V / 5V |
| RTC GND | GND |
---

## ⚙️ Software Requirements

Install dependencies:

```bash
pip install adafruit-circuitpython-ds1307
```
Enable I2C:
```bash
sudo raspi-config
```

run:
```
source myenv/bin/activate
python alarm_project.py
```

Amrutha M
