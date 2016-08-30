import time
from ubinascii import hexlify
from machine import unique_id
#import socket
from robust import MQTTClient

SERVER = "213.136.92.188"
CLIENT_ID = hexlify(unique_id())

time.sleep_ms(10000)

def sub_cb(topic, msg):
    print((topic, msg))

c = MQTTClient("umqtt_client_" + str(CLIENT_ID), SERVER)
c.DEBUG = True
c.set_callback(sub_cb)
if not c.connect(clean_session=False):
    print("New session being set up")
    c.subscribe(b"foo_topic")

while True:
    c.wait_msg()
    #c.connect()
    #c.ping()
    c.publish(b"foo_topic", b"hello", qos=1)
    #c.disconnect()
    time.sleep_ms(1000)

c.disconnect()
