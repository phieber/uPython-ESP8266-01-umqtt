import time
from ubinascii import hexlify
import machine
from umqtt import simple
import bme280

SERVER = "192.168.123.195"
CLIENT_ID = "esp8266-" + str(hexlify(machine.unique_id()), "utf-8")

time.sleep_ms(10000)

c = simple.MQTTClient("umqtt_client_" + CLIENT_ID, SERVER)
c.DEBUG = False

def main():
    while True:
        try:
            c.connect()
            c.publish(b"heartbeat", CLIENT_ID)
            print("publish msg")

            i2c = machine.I2C(scl=machine.Pin(0), sda=machine.Pin(2))
            bme = bme280.BME280(i2c=i2c, address=119)

            c.publish(CLIENT_ID + "/temperature", bme.values[0])
            c.publish(CLIENT_ID + "/pressure", bme.values[1])
            c.publish(CLIENT_ID + "/humidity", bme.values[2])
            
        except (TypeError, OSError):
            machine.reset()
        time.sleep(5)

if __name__ == '__main__':
    main()
