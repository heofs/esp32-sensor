import ubinascii
import json
import urequests
import time
from machine import I2C, Pin
import network

# import esp
# esp.osdebug(None)


class WiFi(object):
    """Connects to WiFi."""

    def __init__(self):
        with open('wifi.json') as json_file:
            self.config = json.load(json_file)
        print(self.config)
        self.wlan = network.WLAN(network.STA_IF)
        print("Initialized wlan object")

    def connect(self):
        if not self.wlan.isconnected():
            print("Connecting to network...")
            self.wlan.active(True)
            self.wlan.connect(self.config["ssid"], self.config["pw"])
            while not self.wlan.isconnected():
                pass
            print("Successfully connected to network.")

    def is_connected(self):
        return self.wlan.isconnected()

    def get_mac_address(self):
        mac = ubinascii.hexlify(network.WLAN().config('mac')).decode()
        return mac


def get_sensor_data():
    """Return sensor temperature and humidity."""
    # Send measurement command
    payload = bytes([0x06])
    i2c.writeto_mem(address, 0x2C, payload)

    time.sleep(0.5)

    # Read data back
    data = i2c.readfrom_mem(address, 0x00, 6)

    # Convert data
    temp = data[0] * 256 + data[1]
    cTemp = -45 + (175 * temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    return {
        "temperature": cTemp,
        "humidity": humidity
    }


post_headers = {
    'Content-Type': 'application/json'
}


def post_data(data):
    if(not wlan.is_connected()):
        wlan.connect()
        time.sleep(1)

    try:
        data = json.dumps(data).encode('utf-8')
        res = urequests.post('http://192.168.1.23:5000/api',
                             data=data, headers=post_headers)
        res.close()

    except Exception as e:
        print("Failed to insert new data.")
        print(e)


# WiFi connection
wlan = WiFi()
wlan.connect()

while (not wlan.is_connected()):
    print("Not connected... waiting 1 second.")
    time.sleep(1)


# SHT3X Sensor
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
address = 68

if (address not in i2c.scan()):
    raise Exception("SENSOR NOT FOUND!")

time.sleep(1)

while True:
    data = get_sensor_data()

    device_id = wlan.get_mac_address()
    data["device_id"] = device_id

    post_data(data=data)

    time.sleep(5)
