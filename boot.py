import network # type: ignore
import time # type: ignore
import urequests # type: ignore

import sys

from lib.dotenv import DotEnv
from lib import mfrc522

allowed_uids = [ "AC030AE1" ]

def zfill(input, width):
    return '0' * (width - len(input)) + input

def uidToString(uid):
    s = ""
    for i in uid:
        s = s + zfill(hex(i)[2:], 2).upper()
    return s.upper()

try:

    card_reader = mfrc522.MFRC522(sck=18,mosi=23,miso=19,rst=22,cs=21)

    print("Waiting for access card..")

    # Loop until a valid card is scanned
    while True:
        # Wait for card to be scanned
        (stat, _) = card_reader.request(card_reader.REQIDL)

        # Check if the card scanned correctly
        if stat == card_reader.OK:
            # Read the UID from the card
            (_, uid) = card_reader.SelectTagSN()
        
            # Convert it to a readable hex format
            uid_s = uidToString(uid)

            print(uid_s)

            # Check if the hex uid exists in the whitelist
            if uid_s in allowed_uids:
                print("Access granted.")
                break

            print("Access denied.")

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

    response = urequests.get(url="http://http.thetruthhurts.me/")

    if not response.status_code == 200:
        raise Exception(f"Network connection test failed, got response: {response.text}")
    
except Exception as ex:
    print(f"An exception occured: {ex}")
    sys.exit()
