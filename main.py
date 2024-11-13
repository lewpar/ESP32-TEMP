import machine # type: ignore
import time # type: ignore
import urequests # type: ignore
import ujson # type: ignore
import gc # type: ignore

from lib.tsense import TSense
from lib.dotenv import DotEnv

PIN_PIR_SENSOR = 35

PIN_BUZZER = 32

PIN_LED_GREEN = 33
PIN_LED_ORANGE = 25
PIN_LED_RED = 26

PIN_TEMP_SENSOR = 27
PIN_BUTTON = 14

use_offboard = True
double_press = False

last_temp = 0
last_offboard_temp = 0

pir_sensor = machine.Pin(PIN_PIR_SENSOR, machine.Pin.IN)

buzzer = machine.PWM(machine.Pin(PIN_BUZZER))
buzzer.deinit()

led_green = machine.Pin(PIN_LED_GREEN, machine.Pin.OUT)
led_orange = machine.Pin(PIN_LED_ORANGE, machine.Pin.OUT)
led_red = machine.Pin(PIN_LED_RED, machine.Pin.OUT)

button = machine.Pin(PIN_BUTTON)

SUPA_API_URL = DotEnv.get('SUPABASE_API_URL')
SUPA_API_KEY = DotEnv.get('SUPABASE_API_KEY')

def temp_changed(temp_old: float, temp_new: float):
    print(f"Temperature changed from {temp_old} to {temp_new}")

def button_pressed(pin):
    global use_offboard, double_press

    # this handler gets triggered once per button press and release,
    # so we store a flag to skip every second trigger
    if double_press:
        double_press = False
        return
    
    double_press = True

    use_offboard = not use_offboard
    print(f"Button on {pin} pressed, changing sensor to {'offboard' if use_offboard else 'onboard'}")


def buzz(frequency: int, duration_ms: int, break_ms: int):
    buzzer.init(freq=frequency)
    time.sleep_ms(duration_ms)
    buzzer.deinit()
    time.sleep_ms(break_ms)

def send_temp_reading(temp, type):
    reading = {
        "type": type,
        "reading": temp,
        "unit": "celcius"
    }

    headers = {
        "Content-Type": "application/json",
        "apiKey": SUPA_API_KEY
    }

    print("Sending temp reading to database..")
    json = ujson.dumps(reading)
    print(json)
    response = urequests.post(url=SUPA_API_URL, headers=headers, data=json)
    print(f"Done {response.status_code}")

def pir_sensed(pin):
    print("Received PIR SENSATION.")
    #buzz(1000, 250, 1)

def main():
    button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)
    pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_sensed)

    tsense = TSense(PIN_TEMP_SENSOR)
    tsense.on_temp_changed = temp_changed

    while True:
        temp = tsense.get_temp(use_external=use_offboard, use_fahrenheit=False)

        if temp <= 24:
            led_green.on()
            led_orange.off()
            led_red.off()
        elif temp > 24 and temp <= 25:
            led_green.off()
            led_orange.on()
            led_red.off()
            #buzz(1000, 100, 250)
        elif temp > 25:
            led_green.off()
            led_orange.off()
            led_red.on()
            #buzz(1000, 100, 50)
            
        gc.collect()

try:
    main()
except Exception as ex:
    print(ex)
finally:
    print("Disabling sensors..")
    # Disable all of the sensors
    button.irq(handler=None)
    pir_sensor.irq(handler=None)
    buzzer.deinit()
    led_green.off()
    led_orange.off()
    led_red.off()
    print("Done")
    gc.collect()