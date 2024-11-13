import esp32 # type: ignore
import machine # type: ignore
import time # type: ignore
import dht # type: ignore

PIN_PIR_SENSOR = 35

PIN_BUZZER = 32

PIN_LED_GREEN = 33
PIN_LED_ORANGE = 25
PIN_LED_RED = 26

PIN_TEMP_SENSOR = 27
PIN_BUTTON = 14

use_offboard = True
double_press = False

pir_sensor = machine.Pin(PIN_PIR_SENSOR, machine.Pin.IN)

buzzer = machine.PWM(machine.Pin(PIN_BUZZER))
buzzer.deinit()

led_green = machine.Pin(PIN_LED_GREEN, machine.Pin.OUT)
led_orange = machine.Pin(PIN_LED_ORANGE, machine.Pin.OUT)
led_red = machine.Pin(PIN_LED_RED, machine.Pin.OUT)

button = machine.Pin(PIN_BUTTON)

# DHT 11 - Temp / Humidity Sensor
temp_sensor = dht.DHT11(machine.Pin(PIN_TEMP_SENSOR, machine.Pin.IN))

last_temp = 0
last_offboard_temp = 0

def to_celcius(input: int):
    return (input - 32.0) / 1.8

def get_onboard_temp():
    """
    Gets the temperature from the ESP32's internal sensor.

    :return: The temperature in fahrenheit.
    """
    return esp32.raw_temperature()

def get_offboard_temp():
    """
    Gets the temperature from the DHT11 sensor.

    :return: The temperature in celcius.
    """
    temp_sensor.measure() 
    return temp_sensor.temperature()

def get_temp():
    global last_temp, last_offboard_temp, use_offboard

    onboard_temp = to_celcius(get_onboard_temp())
    offboard_temp = get_offboard_temp()

    if not is_close(last_temp, onboard_temp):
        print(f"Onboard temperature changed from {last_temp} to {onboard_temp}.")
        last_temp = onboard_temp

    if not is_close(last_offboard_temp, offboard_temp):
        print(f"Offboard temperature changed from {last_offboard_temp} to {offboard_temp}.")
        last_offboard_temp = offboard_temp

    return offboard_temp if use_offboard else onboard_temp

def is_close(a, b):
    """
    Used to calculate if floating point numbers are the same using an epsilon.
    """
    epsilon = 0.01
    return abs(a - b) < epsilon

def button_pressed(pin):
    global use_offboard, double_press

    # this handler gets triggered once per button press and release,
    # so we store a flag to skip every second trigger
    if double_press:
        double_press = False
        return
    
    double_press = True

    use_offboard = not use_offboard
    print(f"Button on {pin} pressed, changing sensor to {"offboard" if use_offboard else "onboard"}")


def buzz(frequency: int, duration_ms: int, break_ms: int):
    buzzer.init(freq=frequency)
    time.sleep_ms(duration_ms)
    buzzer.deinit()
    time.sleep_ms(break_ms)

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)

def pir_sensed(pin):
    print("Received PIR SENSATION.")
    #buzz(1000, 250, 1)

pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_sensed)

while True:
    temp = get_temp()

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