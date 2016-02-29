#!/usr/bin/python3
# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: Zynthian Emulator
# 
# This program emulates a Zynthian Box.
# It embed the Zynthian GUI and uses rotary QT widgets to emulate
# the phisical rotary encoders throw the zyncoder library's emulation
# layer.
# 
# Copyright (C) 2015-2016 Fernando Moyano <jofemodo@zynthian.org>
#
#********************************************************************
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the doc/GPL.txt file.
# 
#********************************************************************

import sys
import signal
import os
from re import findall
from time import sleep
from PyQt4 import QtGui
from PyQt4.QtCore import * 
import zynthian_emubox


class ZynthianQProcess(QProcess):     
	client_window_xid=None

	def __init__(self,zcontainer):
		#Call base class method 
		QProcess.__init__(self)
		#Launch Zynthian GUI
		self.zcontainer=zcontainer
		self.zcontainer_xid=zcontainer.winId()
		self.setProcessChannelMode(QProcess.SeparateChannels); #ForwardedChannels,MergedChannels
		print("Zynthian Container XID: "+str(self.zcontainer_xid))
		QObject.connect(self,SIGNAL("readyReadStandardOutput()"),self,SLOT("readStdOutput()"))
		self.start("./zynthian_gui_emu.sh "+str(self.zcontainer_xid))
	
	#Define Slot Here 
	@pyqtSlot()
	def readStdOutput(self):
		zoutput=str(self.readAllStandardOutput(),encoding='utf-8')
		zoutput=zoutput.replace("FLUSH\n","")
		zoutput=zoutput.replace("FLUSH","")
		zoutput=zoutput.strip()
		if zoutput:
			print(zoutput)
			xids = findall("Zynthian GUI XID: ([\d]+)", zoutput)
			try:
				self.client_window_xid=int(xids[0])
				self.zcontainer.embedClient(self.client_window_xid)
			except:
				pass


class MainWindow(QtGui.QMainWindow):
	zynthian_pid=None
	
	# Pin Configuration (PROTOTYPE-EMU)
	rencoder_pin_a=[4,5,6,7]
	rencoder_pin_b=[8,9,10,11]
	gpio_switch_pin=[0,1,2,3]

	# Rencoder status & last values
	rencoder_status=[0,0,0,0]
	rencoder_lastval=[0,0,0,0]

	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = zynthian_emubox.Ui_ZynthianEmubox()
		self.ui.setupUi(self)
		# Connect Switches
		self.ui.switch_1.pressed.connect(self.cb_switch_1_pressed)
		self.ui.switch_1.released.connect(self.cb_switch_1_released)
		self.ui.switch_2.pressed.connect(self.cb_switch_2_pressed)
		self.ui.switch_2.released.connect(self.cb_switch_2_released)
		self.ui.switch_3.pressed.connect(self.cb_switch_3_pressed)
		self.ui.switch_3.released.connect(self.cb_switch_3_released)
		self.ui.switch_4.pressed.connect(self.cb_switch_4_pressed)
		self.ui.switch_4.released.connect(self.cb_switch_4_released)
		# Connect Rotary Encoders
		self.ui.rencoder_1.valueChanged.connect(self.cb_rencoder_1_change)
		self.ui.rencoder_2.valueChanged.connect(self.cb_rencoder_2_change)
		self.ui.rencoder_3.valueChanged.connect(self.cb_rencoder_3_change)
		self.ui.rencoder_4.valueChanged.connect(self.cb_rencoder_4_change)
		# Embed Zynthian GUI
		self.zynthian_container = QtGui.QX11EmbedContainer(self.ui.frame_screen)
		self.zynthian_container.setGeometry(QRect(1, 3, 320, 240))
		if len(sys.argv)>1:
			self.zynthian_pid=int(sys.argv[1])
		else:
			self.start_zynthian()

	def closeEvent(self, event):
		print("EXIT!")
		self.zynthian_process.terminate()
		self.zynthian_process.waitForFinished(5000)
		event.accept()

	def start_zynthian(self):
		self.zynthian_process=ZynthianQProcess(self.zynthian_container)
		self.zynthian_pid=self.zynthian_process.pid()
		print("Zynthian GUI PID: "+str(self.zynthian_pid))

	def cb_switch_pressed(self,i):
		os.kill(self.zynthian_pid, signal.SIGRTMIN+2*self.gpio_switch_pin[i])

	def cb_switch_released(self,i):
		os.kill(self.zynthian_pid, signal.SIGRTMIN+2*self.gpio_switch_pin[i]+1)

	def cb_switch_1_pressed(self):
		self.cb_switch_pressed(0)

	def cb_switch_1_released(self):
		self.cb_switch_released(0)

	def cb_switch_2_pressed(self):
		self.cb_switch_pressed(1)

	def cb_switch_2_released(self):
		self.cb_switch_released(1)

	def cb_switch_3_pressed(self):
		self.cb_switch_pressed(2)

	def cb_switch_3_released(self):
		self.cb_switch_released(2)

	def cb_switch_4_pressed(self):
		self.cb_switch_pressed(3)

	def cb_switch_4_released(self):
		self.cb_switch_released(3)

	def cb_rencoder_change(self,i,v):
		if v>self.rencoder_lastval[i]:
			if self.rencoder_status[i]>=3:
				self.rencoder_status[i]=0
			else:
				self.rencoder_status[i]+=1
		elif v<self.rencoder_lastval[i]:
			if self.rencoder_status[i]<=0:
				self.rencoder_status[i]=3
			else:
				self.rencoder_status[i]-=1
		self.rencoder_lastval[i]=v
		#print("RENCODER CHANGE "+str(i)+" => "+str(v)+" ("+str(self.rencoder_status[i])+")")
		if self.rencoder_status[i]==0:
			os.kill(self.zynthian_pid, signal.SIGRTMIN+2*self.rencoder_pin_a[i])
		elif self.rencoder_status[i]==1:
			os.kill(self.zynthian_pid, signal.SIGRTMIN+2*self.rencoder_pin_b[i])
		if self.rencoder_status[i]==2:
			os.kill(self.zynthian_pid, signal.SIGRTMIN+2*self.rencoder_pin_a[i]+1)
		elif self.rencoder_status[i]==3:
			os.kill(self.zynthian_pid, signal.SIGRTMIN+2*self.rencoder_pin_b[i]+1)

	def cb_rencoder_1_change(self,v):
		self.cb_rencoder_change(0,v)

	def cb_rencoder_2_change(self,v):
		self.cb_rencoder_change(1,v)

	def cb_rencoder_3_change(self,v):
		self.cb_rencoder_change(2,v)

	def cb_rencoder_4_change(self,v):
		self.cb_rencoder_change(3,v)


app = QtGui.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
