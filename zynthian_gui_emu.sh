#!/bin/bash

export DISPLAY_WIDTH="320"
export DISPLAY_HEIGHT="240"
export ZYNTHIAN_AUBIONOTES=1
export ZYNTHIAN_TOUCHOSC=1
export ZYNTHIAN_WIRING_LAYOUT="EMULATOR"
export ZYNTHIAN_LOG_LEVEL=10

cd ../zynthian-ui
exec ./zynthian_gui.py $1
