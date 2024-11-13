import esp32
import dht
import machine

class TSense:
    on_temp_changed: function
    temp_old: float

    def __init__(self, sensor_pin = 0):
        if sensor_pin:
            self.sensor_external = dht.DHT11(machine.Pin(sensor_pin, machine.Pin.IN))
        self.temp_old = 0.0

    def __to_celcius(self, input: int):
        return (input - 32.0) / 1.8
    
    def __to_fahrenheit(self, input: int):
        return (input * 1.8) + 32.0
    
    def __is_close(self, temp_old, temp_new):
        """
        Compares the temperature floating point values and returns true or false depending on how close to the epsilon it is.
        """
        epsilon = 0.01
        return abs(temp_old - temp_new) < epsilon
    
    def get_temp(self, use_external: bool = False, use_fahrenheit: bool = False) -> float:
        """
        Gets the temperature from the ESP32's internal or external sensor.

        :return: The temperature in celcius. (Set use_fahrenheit parameter for fahrenheit)
        """

        temp_new: float

        if use_external:
            self.sensor_external.measure() 
            temp_new = self.__to_fahrenheit(self.sensor_external.temperature()) if use_fahrenheit else self.sensor_external.temperature()
        else:
            temp_new = esp32.raw_temperature() if use_fahrenheit else self.__to_celcius(esp32.raw_temperature())

        if not self.__is_close(self.temp_old, temp_new):
            self.on_temp_changed(self.temp_old, temp_new)
            self.temp_old = temp_new

        return temp_new