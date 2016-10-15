from machine import Pin, I2C
import time
from ubinascii import hexlify
from machine import unique_id
from simple import MQTTClient
from esp8266_i2c_lcd import I2cLcd

time.sleep_ms(3000)

i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)

# https://forum.micropython.org/viewtopic.php?f=14&t=1422&start=10
lcd = I2cLcd(i2c, 39, 4, 20)
lcd.blink_cursor_off()

SERVER = "192.168.123.195"
CLIENT_ID = "esp8266-" + str(hexlify(unique_id()), "utf-8")
c = MQTTClient("umqtt_client_" + CLIENT_ID, SERVER)



def sub_cb(topic, msg):
    if lcd.cursor_y * lcd.num_columns + lcd.cursor_x + len(str(msg)) > (lcd.num_lines * lcd.num_columns):
        lcd.clear()
        lcd.move_to(0,0)
    lcd.putstr("Puffer[" + str(topic, "utf-8").split("/")[-1] + "]:" + str(msg, "utf-8") + "\n")
    time.sleep_ms(3000)

def main():
    c.set_callback(sub_cb)
    c.connect()
    #c.subscribe(CLIENT_ID + "/display")
    c.subscribe("esp8266-35cacf00/temperature/0")
    c.subscribe("esp8266-35cacf00/temperature/1")
    c.subscribe("esp8266-35cacf00/temperature/2")

    while True:
        c.check_msg()
        time.sleep_ms(500)
    c.disconnect()
        
if __name__ == '__main__':
    main()
