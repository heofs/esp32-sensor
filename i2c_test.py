from machine import I2C, Pin
import time

scl = Pin(22)
sda = Pin(21)
address = 68

i2c = I2C(scl=scl, sda=sda, freq=400000) 

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

print("Temperature: %.2f C" % cTemp)
print("Relative Humidity: %.2f %%RH" % humidity)