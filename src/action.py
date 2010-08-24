# -*- coding: utf-8 -*-

# Inforevealer
# Copyright (C) 2010  Francois Boulogne <fboulogne at april dot org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import io, readconf, getinfo, pastebin
import os, sys, gettext,string, pexpect,getpass


gettext.textdomain('inforevealer')
_ = gettext.gettext

__version__="0.5.1"

def askYesNo(question,default='y'):
	""" Yes/no question throught a  console """
	if string.lower(default) == 'y':
		question = question + " [Y/n]"
	else:
		question = question + " [y/N]"

	ret = string.lower(raw_input(question))
	if ret == 'y' or ret == "":
		answer=True
	else:
		answer=False
	return answer



def RunAs(category_info,gui=False):
	""" Check if root is needed, if user want to be root... """
	if gui: from gui import  yesNoDialog
	run_as='user'
	if os.getuid() == 0:
		#we are root
		run_as='root'
	else:
		#check if root is needed
		root_needed=False
		for i in category_info:
			if i.root:
				root_needed=True
				break
		if root_needed:
			#ask if the user want to substitute
			question=_("""To generate a complete report, root access is needed.
Do you want to substitute user?""")
			if gui:
				#substitute=yesNoDialog(question=question)
				substitute=True #It seems more confortable to remove the question
			else:
				#substitute=askYesNo(question)
				substitute=True #It seems more confortable to remove the question
			if substitute:
				run_as="substitute"
			else:
				run_as="user"
		else:
			run_as='user'
	return run_as

def CompleteReportAsRoot(run_as,tmp_configfile,gui=False):
	"""Run a new instance of inforevealer with root priviledge to complete tmp_configfile"""
    
	if gui: from gui import askPassword

	if run_as == "substitute":
		#find the substitute user command and run the script	

		if pexpect.which('su') != None:
			message=_("Please, enter the root password.")
			root_instance = str(pexpect.which('su')) + " - -c \'"+ os.path.abspath(sys.argv[0])+" --runfile "+ tmp_configfile+"\'" 
			
		elif pexpect.which('sudo') != None: #TODO checkme
			message=_("Please, enter your user password.")
			root_instance = str(pexpect.which('sudo')) + ' ' + os.path.abspath(sys.argv[0])+' --runfile '+ tmp_configfile
		else:
			sys.stderr.write(_("Error: No substitute user command available.\n"))
			return 1
		ret=""
		count=0
		while ret!=[' \r\n'] and count <3:
			#Get password
			count+=1
			if gui:
				password=askPassword(question=message)
			else:
				print(message)
				password=getpass.getpass()
			if password != False: #askPassword could return False
				#Run the command #TODO exceptions ?
				child = pexpect.spawn(root_instance)
				ret=child.expect([".*:",pexpect.EOF]) #Could we do more ?
				child.sendline(password)
				ret = child.readlines() 
				if ret ==[' \r\n']: return 0
		message=_("Wrong password.\nThe log will be generated without root priviledge.")
		if gui:
			import gtk
			md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, message)
			md.set_title(_("Error"))
			md.run()
			md.destroy()
		else:
			print(message)
			


def action(category,dumpfile,configfile,tmp_configfile,verbosity,gui=False):
	if gui: from gui import  yesNoDialog
	#####################
	# Write in dumpfile
	#####################
	dumpfile_handler= open(dumpfile,'w')

	io.print_write_header(dumpfile_handler)

	dumpfile_handler.write('Category: '+ category+'\n')	

	category_info = readconf.LoadCategoryInfo(configfile,category)
	
	#need/want to run commands as...
	run_as = RunAs(category_info,gui)

	#detect which distribution the user uses
	linux_distrib=getinfo.General_info(dumpfile_handler)

	# In the case of run_as='substitute'
	# a configuration file is generated
	# su/sudo is used to run a new instance of inforevealer in append mode
	# to complete the report

	tmp_configfile_handler= open(tmp_configfile,'w')
	for i in category_info:
		i.write(linux_distrib,verbosity,dumpfile_handler,dumpfile,run_as,tmp_configfile_handler)
	tmp_configfile_handler.close()
		
	#Use su or sudo to complete the report
	dumpfile_handler.close() #the next function will modify the report, close the dumpfile
	CompleteReportAsRoot(run_as,tmp_configfile,gui)


	# Message to close the report
	dumpfile_handler= open(dumpfile,'a')
	io.write_title("You didn\'t find what you expected?",dumpfile_handler)
	dumpfile_handler.write( 'Please, open a bug report on\nhttp://github.com/sciunto/inforevealer\n')
	dumpfile_handler.close()

	print( _("The output has been dumped in %s") %dumpfile)

	
