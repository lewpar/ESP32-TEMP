import network # type: ignore
import time # type: ignore
import urequests # type: ignore

import sys

from lib.dotenv import DotEnv

try:
    # Load all the environment variables from the .env file in current directory.
    DotEnv.load(".")

    # Ensure the required environment variables exist in the .env (throws exception if they do not exist)
    DotEnv.ensure("WIFI_SSID")
    DotEnv.ensure("WIFI_PASS")

    DotEnv.ensure('SUPABASE_API_URL')
    DotEnv.ensure('SUPABASE_API_KEY')

    WIFI_SSID = DotEnv.get("WIFI_SSID")
    WIFI_PASS = DotEnv.get("WIFI_PASS")

    # Connect to the Wi-Fi network in Station (STA) mode
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASS)

    print(f"Connecting to {WIFI_SSID}..")

    # Seconds before timing out connection attempt
    wifi_timeout = 5
    wifi_tracker = 0

    while not wifi.isconnected():
        time.sleep_ms(1000)
        wifi_tracker = wifi_tracker + 1

        if wifi_tracker >= wifi_timeout:
            raise Exception(f"Failed to connect to {WIFI_SSID}: Timed out")

    print(f"Connected to network, testing internet connection..")

    response = urequests.get(url="https://cyberbilby.com/")
    if not response == 200:
        raise Exception("Network connection test failed.")
    
except Exception as ex:
    print(f"An exception occured: {ex}")
    sys.exit()
