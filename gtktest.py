#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import gtk

import action,pastebin

import gettext
gettext.textdomain('inforevealer')
_ = gettext.gettext


icon_path='icon.svg'

ui_info ='''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>
</ui>'''


class Application(gtk.Window):
	def __init__(self, configfile, list_category, parent=None):
		self.configfile=configfile
		self.check_list=list_category
		self.category=None

		# Create the toplevel window
		gtk.Window.__init__(self)
			
		pixbuf = gtk.gdk.pixbuf_new_from_file(icon_path)
		self.set_icon(pixbuf)
			
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy', lambda *w: gtk.main_quit())

		self.set_title("Inforevealer") #FIXME
		self.set_default_size(200, 200)
		#self.set_resizable(False)



		merge = gtk.UIManager()
		#self.set_data("ui-manager", merge)
		merge.insert_action_group(self.__create_action_group(), 0)
		#should be added to the top level window so that the Action accelerators can be used by your users
		self.add_accel_group(merge.get_accel_group())



		# Create Menu
		try:
			mergeid = merge.add_ui_from_string(ui_info)
		except gobject.GError, msg:
			print("building menus failed: %s" % msg)
			
		bar = merge.get_widget("/MenuBar")



		# Create TABLE
		box1 = gtk.VBox(True, 0)
		self.add(box1)

		#Add Menu into TABLE        
		box1.pack_start(bar, False, False, 0)
		bar.show()

		#Add info
		label = gtk.Label();
		label.set_markup(_("Select one of the following category:"))
		box1.pack_start(label, False, False, 0)

		self.__create_radio_buttons(box1)


		#buttons (bottom)
		# Create TABLE
		box2 = gtk.HBox(True, 0)
		box1.pack_start(box2, False, False, 0)

		#quit
		bouton = gtk.Button(stock=gtk.STOCK_CLOSE)
		bouton.connect("clicked", self.quit_prog,self, None)
		box2.pack_start(bouton, True, True, 0)
		bouton.set_flags(gtk.CAN_DEFAULT)
		bouton.grab_default()
		bouton.show()
		#apply
		bouton = gtk.Button(stock=gtk.STOCK_APPLY)
		bouton.connect("clicked", self.generate,self, None) #FIXME
		box2.pack_start(bouton, True, True, 0)
		bouton.show()

		box2.show()
		box1.show()    
		self.show_all()

        
        
	def __create_radio_buttons(self,box):
		""" Create the category list """
		first=True
		for item in self.check_list:
		button_label = str(item)+": "+ str(self.check_list[item])
		if first:
			button = gtk.RadioButton(group=None, label=button_label)
			self.category=item
		else:
			button = gtk.RadioButton(group=button, label=button_label)
		button.connect("toggled", self.callback_radio_buttons, item)
		box.pack_start(button, True, True, 0)
		button.show()
		first=False
		
	def callback_radio_buttons(self,widget,data=None):
		""" Get the selected radio button """
		if widget.get_active():
			self.category=data
   

	def __create_action_group(self):
		""" Create the top menu entry  """
		# GtkActionEntry
		entries = ( #FIXME
		( "FileMenu", None, "_File" ),               # name, stock id, label
		( "HelpMenu", None, "_Help" ),               # name, stock id, label
		( "New", gtk.STOCK_NEW,                      # name, stock id
		"_New", "<control>N",                      # label, accelerator
		"Create a new file",                       # tooltip
		self.activate_action ),
		( "Open", gtk.STOCK_OPEN,                    # name, stock id
		"_Open","<control>O",                      # label, accelerator
		"Open a file",                             # tooltip
		self.activate_action ),
		( "Save", gtk.STOCK_SAVE,                    # name, stock id
		"_Save","<control>S",                      # label, accelerator
		"Save current file",                       # tooltip
		self.activate_action ),
		( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
		"Save _As...", None,                       # label, accelerator
		"Save to a file",                          # tooltip
		self.activate_action ),
		( "Quit", gtk.STOCK_QUIT,                    # name, stock id
		"_Quit", "<control>Q",                     # label, accelerator
		"Quit",                                    # tooltip
		self.activate_action ),
		( "About", None,                             # name, stock id
		"_About", "<control>A",                    # label, accelerator
		"About",                                   # tooltip
		self.activate_about ),
		);


		# Create the menubar and toolbar
		action_group = gtk.ActionGroup("AppWindowActions")
		action_group.add_actions(entries)
		
		return action_group

	def activate_about(self, action):
		""" About dialog """
		dialog = gtk.AboutDialog()
		dialog.set_name("Inforevealer") #FIXME
		dialog.set_copyright("\302\251 Copyright 2010 Francois Boulogne")
		dialog.set_website("http://github.com/sciunto/inforevealer")
		## Close dialog on user response
		dialog.connect ("response", lambda d, r: d.destroy())
		dialog.show()
		
	def activate_action(self, action):
		dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
		gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
		'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
		# Close dialog on user response
		dialog.connect ("response", lambda d, r: d.destroy())
		dialog.show()

	def generate(self,widget,evnmt,data=None):
		""" Do the work """
		dumpfile='/tmp/inforevealer' #FIXME
		verbosity=False
		
		website = "http://pastebin.com"
		pastebin_choice=False
		tmp_configfile="/tmp/inforevealer_tmp.conf" #tmp configuration file (substitute)
		print self.category
		action.action(self.category,dumpfile,self.configfile,tmp_configfile,verbosity,pastebin_choice,website,gui=True)
		TextViewer(dumpfile)

	def quit_prog(self,widget,evnmt,data=None):
		""" Quit the software """
		gtk.main_quit()


class TextViewer:
	def change_editable(self, case, textview):
		textview.set_editable(case.get_active())

	def change_curseur_visible(self, case, textview):
		textview.set_cursor_visible(case.get_active())

	
	def quit_prog(self, widget):
		gtk.main_quit()

	def __init__(self,output_file):
		self.output=output_file
	

      
		fenetre = gtk.Window(gtk.WINDOW_TOPLEVEL)
		pixbuf = gtk.gdk.pixbuf_new_from_file(icon_path)
		fenetre.set_icon(pixbuf)
		fenetre.set_resizable(True)
		fenetre.set_default_size(600, 400)
		fenetre.connect("destroy", self.quit_prog)
		fenetre.set_title("Inforevealer") #FIXME
		fenetre.set_border_width(0)

		boite1 = gtk.VBox(False, 0)
		fenetre.add(boite1)
		boite1.show()


		boite2 = gtk.VBox(False, 10)
		boite2.set_border_width(10)
		boite1.pack_start(boite2, True, True, 0)
		boite2.show()

		#Add info
		label = gtk.Label();
		output_string=_("The following report is availlable in ")+str(self.output)
		label.set_markup(output_string)
		label.show()
		boite2.pack_start(label,False,False,0)

		fd = gtk.ScrolledWindow()
		fd.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_editable(False)

		buffertexte = textview.get_buffer()
		fd.add(textview)
		fd.show()
		textview.show()
		textview.set_cursor_visible(False)

		boite2.pack_start(fd)
		#load file
		try:
			fichier = open(self.output, "r")#FIXME
			self.text = fichier.read()
			fichier.close()
			buffertexte.set_text(self.text)
		except IOError:
			sys.stderr.write("Error: Cannot open %s" %self.output)

		#Add Pastebin
		boiteH = gtk.HBox(True,0)
		boite2.pack_start(boiteH, False, False, 0)
		boiteH.show()


		label = gtk.Label();
		label.set_markup(_("Send the report on pastebin "))
		label.show()
		boiteH.pack_start(label,True,False,0)
		
		#TODO
		
		self.pastebin_list = pastebin.preloadPastebins()
		self.combobox = gtk.combo_box_new_text()
		self.website=list()
		boiteH.pack_start(self.combobox, True, False, 0)
		for k in self.pastebin_list:
			self.combobox.append_text(k)
			self.website.append(k)
		self.combobox.set_active(0)
		self.combobox.show()
		
		bouton = gtk.Button(_("Send"))
		bouton.connect("clicked", self.send_pastebin)
		bouton.show()
		boiteH.pack_start(bouton, True, False, 0)
		
		#END pastebin
	
		#Buttons
		boiteH = gtk.HBox(True,0)
		boite2.pack_start(boiteH, False, False, 0)
		boiteH.show()	
		
		bouton = gtk.Button(_("Copy to clipboard"))
		bouton.connect("clicked", self.copy_clipboard)
		boiteH.pack_start(bouton, False, False, 0)
		bouton.show()

		bouton = gtk.Button(stock=gtk.STOCK_CLOSE)
		bouton.connect("clicked", self.quit_prog)
		boiteH.pack_start(bouton, False, False, 0)
		bouton.set_flags(gtk.CAN_DEFAULT)
		#bouton.grab_default()
		bouton.show()
		fenetre.show()
        
	def copy_clipboard(self,widget):
		""" Copy self.text in clipboard """
		clipb = gtk.Clipboard()
		clipb.set_text(self.text, len=-1)

	def send_pastebin(self, widget): #IMPROVEME
		link = "http://" + self.website[self.combobox.get_active()]+"/"
		link=pastebin.sendFileContent(self.output,title=None,website=link,version=None)
		message = "File sent on\n"+link
		md = gtk.MessageDialog(None, 
			gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
			gtk.BUTTONS_CLOSE, message)
		md.set_title(_("Pastebin link"))
		md.run()
		md.destroy()


def yesNoDialog(title=" ",question="?"):
	'''
	returns True if yes 
	        False if no
	#inspired from http://www.daa.com.au/pipermail/pygtk/2002-June/002962.html
		   '''
	#create window+ Vbox + question
	window=gtk.Window()
	pixbuf = gtk.gdk.pixbuf_new_from_file(icon_path)
	window.set_icon(pixbuf)
	window.set_title(title)
	vbox = gtk.VBox(True, 0)
	window.add(vbox)
	label = gtk.Label();
        label.set_markup(question)
        vbox.pack_start(label, False, False, 0)
	
	
	hbox = gtk.HButtonBox()
	def delete_event(widget, event, window):
		window.callback_return=-1
		return False
	window.connect("delete_event", delete_event, window)
	vbox.pack_start(hbox, False, False, 0)
	
	
	def callback(widget, data):
		window=data[0]
		data=data[1]
		window.hide()
		window.callback_return=data

	yes = gtk.Button(stock=gtk.STOCK_YES)
	yes.set_flags(gtk.CAN_DEFAULT)
	window.set_default(yes)
	yes.connect("clicked", callback, (window, True))
	hbox.pack_start(yes)

	no = gtk.Button(stock=gtk.STOCK_NO)
	no.connect("clicked", callback, (window, False))
	hbox.pack_start(no)

	window.set_modal(True)
	window.show_all()
	window.callback_return=None
	while window.callback_return==None:
		gtk.main_iteration(True) # block until event occurs
	return window.callback_return



def askPassword(title=" ",question="?"):
	""" Dialog box for a password.
	Return the password 
	return false if the dialog is closed"""
	#create window+ Vbox + question
	window=gtk.Window()
	pixbuf = gtk.gdk.pixbuf_new_from_file(icon_path)
	window.set_icon(pixbuf)
	window.set_title(title)
	vbox = gtk.VBox(True, 0)
	window.add(vbox)
	label = gtk.Label();
        label.set_markup(question)
        vbox.pack_start(label, False, False, 0)


	def delete_event(widget, event, window):
		window.callback_return=False
		return False
	window.connect("delete_event", delete_event, window)	
	
	def callback(widget,data):
		window=data[0]
		window.hide()
		window.callback_return=pword.get_text()

	# Message for the window 
	pword = gtk.Entry()
	pword.set_visibility(False)
	vbox.pack_start(pword, False, False, 0)
	
	
	hbox = gtk.HButtonBox()
	vbox.pack_start(hbox, False, False, 0)

	# OK button
	but = gtk.Button(stock=gtk.STOCK_OK)
	but.set_flags(gtk.CAN_DEFAULT)
	window.set_default(but)
	hbox.add(but)
	but.connect("clicked", callback, (window,True))


	window.set_modal(True)
	window.show_all()
	window.callback_return=None
	while window.callback_return==None:
		gtk.main_iteration(True) # block until event occurs
	return window.callback_return



def main(configfile,list):
	Application(configfile,list)
	gtk.main()

if __name__ == '__main__':
    main()
