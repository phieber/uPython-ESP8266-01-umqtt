import time

time.sleep_ms(10000)

def readDS18x20():
    from machine import Pin
    import onewire, ds18x20

    OneWirePin = 0

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

def getClientID():
    from ubinascii import hexlify
    from machine import unique_id
    return "esp8266-" + str(hexlify(unique_id()), "utf-8")

def initMQTT():
    from simple import MQTTClient
    SERVER = "192.168.123.195"

    return MQTTClient("umqtt_client_" + getClientID(), SERVER)

def pubMQTT(client, sensorID, sensorValue):
    client.publish(getClientID() + "/" + "temperature" + "/" + sensorID, sensorValue)

def main():
    c = initMQTT()

    while True:
        try:
            c.connect()
            c.publish(b"heartbeat", getClientID())
            print("publish msg")
            #c.disconnect()

            # read ds18x20 sensors
            values = readDS18x20()
            for value in values:
                #c.connect()
                pubMQTT(c, str(values.index(value)), str(value))
                #c.disconnect()

        except Exception as e:
            print(str(e))
            time.sleep(10)
            import machine
            machine.reset()
        finally:
            c.disconnect()
        time.sleep(5)

if __name__ == '__main__':
    main()
