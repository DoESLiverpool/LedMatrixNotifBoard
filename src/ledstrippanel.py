import framebuf
from machine import Pin, SPI

cs, spi = None, None
brightnesschars = None
buffer = None
fbuff = None
numledchars = 0
# ESP32-HSPI: sck=14, mosi=13

def setbrightness(brightness, i0=0, i1=9999):
    # 0<=brightness<=15
    for i in range(max(i0, 0), min(i1, numledchars)):
        brightnesschars[(numledchars - i)*2 - 1] = brightness
        
def showbrightness():
    cs.value(0)  
    spi.write(brightnesschars)
    cs.value(1)
    
def scrollbrightness(brightness=0):
    for i in range(numledchars - 1):
        brightnesschars[(numledchars - i)*2 - 1] = brightnesschars[(numledchars - (i+1))*2 - 1]
    brightnesschars[1] = brightness
    
s = bytearray(8)
def show():
    for y in range(8):
        s[6] = s[4] = s[2] = s[0] = y+1
        yp = y*(numledchars) + numledchars
        cs.value(0)  # cannot put in loop as resets the shifting
        for m in range(0, numledchars-1, 4):
            s[1] = buffer[yp - m - 1]
            s[3] = buffer[yp - m - 2]
            s[5] = buffer[yp - m - 3]
            s[7] = buffer[yp - m - 4]
            spi.write(s)
        cs.value(1)

def init():
    for i in range(0, 10, 2):
        cs.value(0)
        x = b"\x0c\x00\x0f\x00\x0b\x07\x09\x00\x0c\x01"[i:i+2]
        spi.write(x*numledchars)
        cs.value(1)
    showbrightness()
        
def setup(lnumledchars, lcs, lspi):
    global numledchars, cs, spi, brightnesschars, buffer, fbuff
    cs, spi = lcs, lspi
    numledchars = lnumledchars # can be 4n+1 for scroll buffer

    brightnesschars = bytearray(bytes([0x0a, 0])*numledchars)
    buffer = bytearray(8*(numledchars))  # make one extra character to scroll from
    fbuffwidth = 8*(numledchars)
    fbuffheight = 8
    fbuff = framebuf.FrameBuffer(buffer, fbuffwidth, fbuffheight, framebuf.MONO_HLSB)

    init()
    
    for i in range(0, numledchars*8, 4):
        fbuff.fill_rect(i, (i%8), 4, 4, 1)
    show()
    return fbuff
