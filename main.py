import esp32
import machine
import time
import dht

PIN_LED_GREEN = 33
PIN_LED_ORANGE = 25
PIN_LED_RED = 26

PIN_TEMP_SENSOR = 27
PIN_BUTTON = 14

use_offboard = True
double_press = False

pin_green = machine.Pin(PIN_LED_GREEN, machine.Pin.OUT)
pin_orange = machine.Pin(PIN_LED_ORANGE, machine.Pin.OUT)
pin_red = machine.Pin(PIN_LED_RED, machine.Pin.OUT)

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

def is_close(a, b):
    """
    Used to calculate if floating point numbers are the same using an epsilon.
    """
    epsilon = 0.01
    return abs(a - b) < epsilon

def button_pressed(pin):
    global use_offboard, double_press

    if double_press:
        double_press = False
        return
    
    double_press = True

    use_offboard = not use_offboard
    print(f"Button on {pin} pressed, changing sensor to {"offboard" if use_offboard else "onboard"}")

# Creates an Interrupt Request (IRQ) when a Falling Edge is detected on the button Pin.
# A falling edge is a drop in voltage from HIGH to LOW.
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)

while True:
    onboard_temp = to_celcius(get_onboard_temp())
    offboard_temp = get_offboard_temp()

    if not is_close(last_temp, onboard_temp):
        print(f"Onboard temperature changed from {last_temp} to {onboard_temp}.")
        last_temp = onboard_temp

    if not is_close(last_offboard_temp, offboard_temp):
        print(f"Offboard temperature changed from {last_offboard_temp} to {offboard_temp}.")
        last_offboard_temp = offboard_temp

    temp =  offboard_temp if use_offboard else onboard_temp

    if temp <= 27:
        pin_green.on()
        pin_orange.off()
        pin_red.off()
    elif temp > 27 and temp <= 28:
        pin_green.off()
        pin_orange.on()
        pin_red.off()
    elif temp > 28:
        pin_green.off()
        pin_orange.off()
        pin_red.on()

    time.sleep_ms(250)