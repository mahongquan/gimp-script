#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
class HelloWorldGTK:
	"""This is an Hello World GTK application"""
	def __init__(self):
		# Set the glade file
		self.gladefile = "helloworld.glade" 
		self.wtree = gtk.glade.XML(self.gladefile)
		self.window = self.wtree.get_widget("window1")
		dic = {"on_button1_clicked" : self.button1_clicked,
		       "on_window1_destroy" : gtk.main_quit } 
		self.wtree.signal_autoconnect(dic)
		if (self.window):
#			self.window.connect("destroy", gtk.main_quit)
			self.window.show()
	def button1_clicked(self, widget):
		print "Hello World!"	
		
if __name__ == "__main__":
	print("run")
	hwg = HelloWorldGTK()
	hwg.window.show_all()
