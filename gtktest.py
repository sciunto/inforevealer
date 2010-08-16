#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import gtk

import action

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
            print "building menus failed: %s" % msg
            
        bar = merge.get_widget("/MenuBar")
        
        
        
        # Create TABLE
        box1 = gtk.VBox(True, 0)
        self.add(box1)
        
        #Add Menu into TABLE        
        box1.pack_start(bar, False)
        bar.show()

        #Add info
        label = gtk.Label();
        label.set_markup("Select on of the following category:")
        box1.pack_start(label, False, False, 0)

        self.__create_radio_buttons(box1)


        #buttons (bottom)
        # Create TABLE
        box2 = gtk.HBox(True, 0)
        box1.pack_start(box2, False, False, 0)

        #quit
        bouton = gtk.Button(stock=gtk.STOCK_CLOSE)
        bouton.connect_object("clicked", self.quit_prog,self, None)
        box2.pack_start(bouton, True, True, 0)
        bouton.set_flags(gtk.CAN_DEFAULT)
        bouton.grab_default()
        bouton.show()
        #apply
        bouton = gtk.Button(stock=gtk.STOCK_APPLY)
        bouton.connect_object("clicked", self.generate,self, None) #FIXME
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
        print( str(data) + "  " + str(widget.get_active()))
        if widget.get_active():
	     self.category=data
        #TODO

    def __create_action_group(self):
        """ Create the top menu entry  """
        # GtkActionEntry
        entries = (
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
	dumpfile='/tmp/inforevealer'
	verbosity=False
	
	website = "http://pastebin.com"
	pastebin_choice=False
	tmp_configfile="/tmp/inforevealer_tmp.conf" #tmp configuration file (substitute)
	print self.category
	#action.action(self.category,dumpfile,self.configfile,tmp_configfile,verbosity,pastebin_choice,website)
	

    def quit_prog(self,widget,evnmt,data=None):
        """ Quit the software """
        gtk.main_quit()


def main(configfile,list):
    Application(configfile,list)
    gtk.main()

if __name__ == '__main__':
    main()
