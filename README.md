# Overview

Code for the LED matrix display which includes coffee timer, and other
features currently in development.

## Installation

TBD. I suspect that mpflash will be needed or other flashing tool.
However, I have not yet tried to flash anything on the device. Moreover,
I have not checked if mpremote could also be used for this.

## Utilities 

mpremote was used to retrieve the micropython code inside the
esp8266MOD. Therefore, it would be a tool that would be nice to have
while dealing with the system. Instructions for the installation
of mpremote is shown below:

Installation via pip
> pip install -- user mpremote

Installation via pipx
> pipx install mpremote

Installation via uv
> uv tool install mpremote

To view the micropython code inside the device simply type in
> mpremote ls

To copy the files into your own file system. Note that the src
should be prefixed by ":" (eg. ":main.py")
> mpremote cp \<src\> \<dest\>

## Notes
Sensitive details from the config.txt and webrepl_cfg.py file has been removed.
Before putting the file in the esp8266MOD, fill in the appropriate details.
Further information about the device is found in: https://github.com/DoESLiverpool/somebody-should/wiki/ESP-devices
