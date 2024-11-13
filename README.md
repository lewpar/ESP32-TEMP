# ESP32 - Temperature Sensor
An ESP32 temp sensor IoT device that detects changes in temperature and POSTs them to a Supabase database.
It also has support for switching between internal and external sensor through a button.

There is also a PIR sensor that activates a buzzer to scare the ants away from the sensor.

## Tools
There are some tools in the `./tools` folder for cleaning / flashing firmware to the ESP32 flash memory.
There is also stub files for the ESP32 in the `./typings` folder to allow Pylance intellisense to work (credits to [micropython stubs](https://github.com/Josverl/micropython-stubs)).

## Dependencies
- MicroPython
- ESPTool