import RPi.GPIO as GPIO
import time
import board
import adafruit_ds1307

# ── Pin definitions (BCM) ──
BUTTON = 27
BUZZER = 17   # KY-006: PWM
LED_R  = 18   # common cathode → HIGH = ON
LED_G  = 23
LED_B  = 24

DELAY = 3  # seconds after button press

# ── GPIO setup ──
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # LOW when pressed
GPIO.setup(BUZZER,GPIO.OUT)
# COMMON CATHODE → start OFF (LOW)
GPIO.setup(LED_R, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_B, GPIO.OUT, initial=GPIO.LOW)

# Buzzer PWM
buzzer_pwm = GPIO.PWM(BUZZER, 1000)

# ── RTC setup ──
i2c = board.I2C()
rtc = adafruit_ds1307.DS1307(i2c)

NOTE_C5 = 523
NOTE_E5 = 659
NOTE_G5 = 784
NOTE_C6 = 1047
# Create PWM objects (100 Hz is fine)
pwm_r = GPIO.PWM(LED_R, 100)
pwm_g = GPIO.PWM(LED_G, 100)
pwm_b = GPIO.PWM(LED_B, 100)

# Start them OFF
pwm_r.start(0)
pwm_g.start(0)
pwm_b.start(0)

def led_on(color="red"):
    """Common cathode: HIGH = ON"""
    GPIO.output(LED_R, GPIO.HIGH if color in ("red", "white") else GPIO.LOW)
    GPIO.output(LED_G, GPIO.HIGH if color in ("green", "white") else GPIO.LOW)
    GPIO.output(LED_B, GPIO.HIGH if color in ("blue", "white") else GPIO.LOW)

def led_off():
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)

def jingle_tune(buzzer_pwm, pwm_r, pwm_g, pwm_b):
    # Note frequencies (Hz)
    NOTE_E5 = 659
    NOTE_G5 = 784
    NOTE_C5 = 523
    NOTE_D5 = 587
    NOTE_F5 = 698

    melody = [
        NOTE_E5, NOTE_E5, NOTE_E5,
        NOTE_E5, NOTE_E5, NOTE_E5,
        NOTE_E5, NOTE_G5, NOTE_C5, NOTE_D5, NOTE_E5,

        NOTE_F5, NOTE_F5, NOTE_F5, NOTE_F5,
        NOTE_F5, NOTE_E5, NOTE_E5, NOTE_E5, NOTE_E5,
        NOTE_E5, NOTE_D5, NOTE_D5, NOTE_E5, NOTE_D5, NOTE_G5
    ]

    durations = [
        0.3, 0.3, 0.6,
        0.3, 0.3, 0.6,
        0.3, 0.3, 0.3, 0.3, 0.8,

        0.3, 0.3, 0.3, 0.3,
        0.3, 0.3, 0.3, 0.3, 0.6,
        0.3, 0.3, 0.3, 0.3, 0.8,
        0.5
    ]

    # Simple color palette (cycle through)
    colors = [
        (100, 0, 0),     # red
        (100, 50, 0),    # orange
        (100, 100, 0),   # yellow
        (0, 100, 0),     # green
        (0, 100, 100),   # cyan
        (0, 0, 100),     # blue
        (100, 0, 100),   # purple
    ]

    def set_color(r, g, b):
        pwm_r.ChangeDutyCycle(r)
        pwm_g.ChangeDutyCycle(g)
        pwm_b.ChangeDutyCycle(b)

    for i, (note, duration) in enumerate(zip(melody, durations)):
        # 🎵 play note
        buzzer_pwm.ChangeFrequency(note)
        buzzer_pwm.start(50)

        # 🌈 change color based on beat
        color = colors[i % len(colors)]
        set_color(*color)

        time.sleep(duration)

        buzzer_pwm.stop()
        time.sleep(0.05)

    # turn off LED at end
    set_color(0, 0, 0)

def mario_tune():
    melody = [
        NOTE_E5, NOTE_E5, 0, NOTE_E5,
        0, NOTE_C5, NOTE_E5, 0,
        NOTE_G5, 0, 0, 0,
        NOTE_C6
    ]

    melody = melody[:80]
    duration = 0.15

    for note in melody:
        if note == 0:
            buzzer_pwm.stop()
            time.sleep(duration)
        else:
            buzzer_pwm.ChangeFrequency(note)
            buzzer_pwm.start(50)
            time.sleep(duration)
def trigger_alarm():
    t = rtc.datetime
    print(f"Triggered at {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}")

    led_on("red")

    jingle_tune(buzzer_pwm, pwm_r, pwm_g, pwm_b)
    led_off()
print("Waiting for button press...")

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.LOW:
            print(f"Button pressed! Alarm in {DELAY}s...")
            time.sleep(0.3)  # debounce
            time.sleep(DELAY)

            trigger_alarm()

            time.sleep(1)  # prevent retrigger
        time.sleep(0.05)

except KeyboardInterrupt:
    buzzer_pwm.stop()
    led_off()
    GPIO.cleanup()
    print("Cleaned up.")
