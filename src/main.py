from mqtt_as import MQTTClient
from stdmqttas import fconfig, config, mqttconnecttask, callbackcmdtask, flashledconnectedtask
import uasyncio as asyncio
from stdmqttas import pinled, flashpinled, shortmac, topicstem, topicstatus
from machine import Pin, PWM, SPI
import time, itertools
from ledstrippanel import setup, show
from uasyncio.queues import Queue

numledchars = int(fconfig["numledchars"])
fbuff = setup(numledchars, Pin(int(fconfig["pincs"]), Pin.OUT), SPI(1, 1000000))
flashpinled(5, 300, 300)

topicmessage = topicstem+"/message"
topiccmd = (topicstem+"/cmd").encode()
topicreply = topicstem+"/reply"

qmessages = Queue()
async def messagetask():
    message = " "
    while True:
        prevmessage, message = message, await(qmessages.get())
        for xchar, (c1, c2) in enumerate(zip(prevmessage, message)):
            if c1 != c2:
                break
        fbuff.fill(0)
        fbuff.text(message, 0, 0, 1)
        for ys in range(7, -1, -1):
            fbuff.fill_rect(xchar*8, 0, (numledchars - xchar)*8, 8, 0)
            fbuff.text(prevmessage[xchar:], xchar*8, ys - 8, 1)
            fbuff.text(message[xchar:], xchar*8, ys, 1)
            show()
            await asyncio.sleep_ms(50)
        await asyncio.sleep_ms(450)

async def cursorflash(client):    
    for i in itertools.count():
        await asyncio.sleep_ms(1000)
        if client.connectioncount and not client.isconnected() and qmessages.qsize() < 2:
            await qmessages.put("wifi fail: %d"%i)
            await asyncio.sleep_ms(5000)
            ipnumber = client._sta_if.ifconfig()[0]
            await qmessages.put(ipnumber)
            await asyncio.sleep_ms(4000)
        elif qmessages.empty():
            fbuff.fill_rect((numledchars-1)*8, 7, 8, 1, i%2)
            show()
        if client.isconnected():
            await client.publish(topicstatus, "beat-%d"%i)
        
def callbackcmd(topic, msg, retained):
    print("callbackcmd", topic, msg)
    if topic == topiccmd:
        aloop.create_task(callbackcmdtask(client, topicreply, msg))
    elif qmessages.qsize() < 5:
        if 1 <= len(msg) <= 50:
            aloop.create_task(qmessages.put(msg.decode()))

async def onconnecttask(client):
    ipnumber = client._sta_if.ifconfig()[0]
    await client.publish(topicstatus, ipnumber, retain=True)
    await qmessages.put("subscribing")
    await client.subscribe(topiccmd)
    await client.subscribe(topicmessage)
    await qmessages.put("ip: "+ipnumber)
    await client.publish(topicmessage, "reconnections #%d"%client.connectioncount)
    client.connectioncount += 1
    print("subscribed")
            
config['subs_cb'] = callbackcmd
config['connect_coro'] = onconnecttask
client = MQTTClient(config)
client.DEBUG = True
client.connectioncount = 0

aloop = asyncio.get_event_loop()
aloop.create_task(messagetask())
aloop.create_task(cursorflash(client))
aloop.create_task(mqttconnecttask(client))
aloop.create_task(flashledconnectedtask(client))
aloop.run_forever()
