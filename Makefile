

all: zynthian_emubox

zynthian_emubox:
	pyuic4 zynthian_emubox.ui -o zynthian_emubox.py
	pyrcc4 -py3 zynthian_emuface.qrc -o zynthian_emuface_rc.py
