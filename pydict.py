#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#English malayalam Dictionary
#Copyright (C) 2008  Kerala State IT Mission
#Author : Vimal Joseph
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
  	import pickle
  	import pango
  	
except:
	sys.exit(1)

class pyDict:
	"""This is an English Malayalam Dictionary application"""

	def __init__(self):
			
		#Set the Glade file
		self.gladefile = "data/pydict.glade"  
		self.wTree = gtk.glade.XML(self.gladefile, "main_window") 
		self.dictionary={}
		self.dictFile="data/dict.dat"
		f=open(self.dictFile,'r')
		self.dictionary=pickle.load(f)
			
		#Create our dictionay and connect it
		dic = {"on_main_window_destroy" : gtk.main_quit
				, "on_btn_search_clicked" : self.OnSearch
				,"on_quit1_activate":gtk.main_quit
				,"on_about1_activate":self.OnAbout}
		self.wTree.signal_autoconnect(dic)
		
		#Here are some variables that can be reused later
				
		
					
		self.entry_key = self.wTree.get_widget("entry_key")		
		#Get the treeView from the widget Tree
		self.meaningView = self.wTree.get_widget("txt_meaning")
		self.meaningbuffer = self.meaningView.get_buffer()
		self.meaningView.modify_font(pango.FontDescription("Meera 12"))
		completion = gtk.EntryCompletion()
		self.entry_key.set_completion(completion)
		completion_model = self.__create_completion_model()
		completion.set_model(completion_model)
		completion.set_text_column(0)
		completion.connect("match-selected",self.match_cb)

	def match_cb(self, completion, model, iter):
		self.findMeaning(model[iter][0].lower())
        	return
	
	def findMeaning(self,key):
		str=""
		self.meaningbuffer.set_text("")
		if self.dictionary.has_key(key):
			meaningList=self.dictionary[key]
			for i in meaningList:
				str=str+i.strip()	+"\n"
			self.meaningbuffer.set_text(str)
		else :
			self.meaningbuffer.set_text("താങ്കള്‍ അന്വേഷിച്ച വാക്ക് ഈ നിഘണ്ടുവിലില്ല")
	
	def OnSearch(self, widget):
		"""Called when the use wants to search for a word"""
		key=self.entry_key.get_text().lower()
		self.findMeaning(key)
	
	def OnAbout(self,widget):
		dlgAbout = AboutDlg();		
		dlgAbout.run()

	def __create_completion_model(self):
		try:
		        store = gtk.ListStore(str)
			for key_word in self.dictionary.keys():
				iter = store.append()
				store.set(iter,0,key_word)
		        return store
		except:
			store = []
			return store

			
class AboutDlg:
	def __init__(self):
		#setup the glade file
		self.gladefile = "data/pydict.glade"
		
	def run(self):
		self.wTree = gtk.glade.XML(self.gladefile, "dlgAbout") 
		#Get the actual dialog widget
		img = self.wTree.get_widget("image1")
		img.set_from_file("data/ml_logo.png")
		self.dlg = self.wTree.get_widget("dlgAbout")
		self.dlg.run()
		self.dlg.destroy()
		return
		
if __name__ == "__main__":
	d = pyDict()
	gtk.main()
