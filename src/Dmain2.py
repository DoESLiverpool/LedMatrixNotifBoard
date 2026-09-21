from stdmqttas import fconfig
import time
from machine import Pin, SPI
from ledstrippanel import setup, show
import math

numledchars = int(fconfig["numledchars"])
fbuff = setup(numledchars, Pin(int(fconfig["pincs"]), Pin.OUT), SPI(1, 1000000))

for i in range(400):
    s = math.sin(math.radians(i/60*360))
    x = int((s+1)*50)
    fbuff.fill(0)
    fbuff.rect(x,1,40,5,1)
    fbuff.hline(100-x,7,30,1)
    fbuff.text(str(i),i+50,0,1)
    show()
    time.sleep_ms(10)
    