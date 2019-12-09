# Uploading SHT3x sensor data

## Setup

Erease flash
`esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART erase_flash`

Flash new firmware
`esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 esp32-file.bin`

## Running

Run script

`pipenv run ampy --port /dev/tty.SLAB_USBtoUART run boot.py`

Upload file

`pipenv run ampy --port /dev/tty.SLAB_USBtoUART put boot.py`

Enter REPL

`screen /dev/tty.SLAB_USBtoUART 115200`
