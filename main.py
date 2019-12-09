import network
from machine import I2C, Pin
import time
import urequests
import json
import ubinascii

print("\nRUNNING MAIN!\n")


def get_mac_address():
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


def post_data(data):
    data = json.dumps(data).encode('utf-8')
    urequests.post('http://192.168.1.23:5000/api', data=data)
    print("Posted new sensor data")


print("Starting..")

# SHT3X Sensor
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

address = 68

if (address not in i2c.scan()):
    raise Exception("SENSOR NOT FOUND!")

time.sleep(1)

while True:

    data = get_sensor_data()

    device_id = get_mac_address()
    data["device_id"] = device_id

    post_data(data=data)

    print("Uploaded data.")
    time.sleep(10)
