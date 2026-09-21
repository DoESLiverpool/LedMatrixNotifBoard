# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc

# This allows remote programming and modifying files over the network
import webrepl
webrepl.start()

gc.collect()
