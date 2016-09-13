import time
from ubinascii import hexlify
from machine import unique_id
from robust import MQTTClient

SERVER = "192.168.123.195"
CLIENT_ID = "esp8266-" + str(hexlify(unique_id()), "utf-8")
OneWirePin = 0

time.sleep_ms(10000)

def sub_cb(topic, msg):
    print((topic, msg))

def readDS18x20():
    from machine import Pin
    import onewire, ds18x20

    # the device is on GPIO12
    dat = Pin(OneWirePin)
    # create the onewire object
    ds = ds18x20.DS18X20(onewire.OneWire(dat))
    # scan for devices on the bus
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    values = []

    for rom in roms:
        values.append(ds.read_temp(rom))

    print(values)
    return values

c = MQTTClient("umqtt_client_" + CLIENT_ID, SERVER)
c.DEBUG = False
c.set_callback(sub_cb)
if not c.connect(clean_session=False):
    #print("New session being set up")
    #c.subscribe(b"foo_topic")
    c.publish(b"heartbeat", b"New session being set up", qos=1)

def main():
    while True:
        try:
            c.publish(b"heartbeat", CLIENT_ID, qos=1)
            print("publish msg")

            # read ds18x20 sensors
            values = readDS18x20()
            for value in values:
                c.publish(CLIENT_ID + "/" + "temperature" + "/" + str(values.index(value)), str(value), qos=1)
        except TypeError as te:
            pass
        time.sleep(5)

if __name__ == '__main__':
    main()
