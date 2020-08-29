# !/usr/bin/python3
# -*- coding: utf-8 -*-
from confapp import conf
from AnyQt.QtGui import QIcon


from pybpod_rotaryencoder_module.module_gui import RotaryEncoderModuleGUI

class ProjectsRotaryEncoder(object):

	def register_on_main_menu(self, mainmenu):
		super(ProjectsRotaryEncoder, self).register_on_main_menu(mainmenu)

		if len([m for m in mainmenu if 'Tools' in m.keys()]) == 0:
			 mainmenu.append({'Tools': []})

		menu_index = 0
		for i, m in enumerate(mainmenu):
			if 'Tools' in m.keys(): menu_index=i; break

		mainmenu[menu_index]['Tools'].append( '-' )	
		mainmenu[menu_index]['Tools'].append( {'Rotary encoder': self.open_rotaryencoder_plugin, 'icon': QIcon(conf.ROTARYENCODER_PLUGIN_ICON)} )
	
	def open_rotaryencoder_plugin(self):
		if not hasattr(self, 'rotaryencoder_plugin'):
			self.rotaryencoder_plugin = RotaryEncoderModuleGUI(self)
			self.rotaryencoder_plugin.show()
			self.rotaryencoder_plugin.resize(*conf.ROTARYENCODER_PLUGIN_WINDOW_SIZE)			
		else:
			self.rotaryencoder_plugin.show()

		return self.rotaryencoder_plugin