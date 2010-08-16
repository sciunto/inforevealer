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
			if gui:
				pass #TODO
			else:
				substitute=askYesNo(_("""To generate a complete report, root access is needed.
Do you want to substitute user?"""))
			if substitute:
				run_as="substitute"
			else:
				run_as="user"
		else:
			run_as='user'
	return run_as

def CompleteReportRoot(run_as,tmp_configfile,gui=False):
	"""Run a new instance of inforevealer with root priviledge to complete tmp_configfile"""
	if run_as == "substitute":
		#find the substitute user command and run the script	
		if pexpect.which('sudo') != None: #TODO checkme
			print(_("Please, enter your user password."))
			root_instance = str(pexpect.which('sudo')) + os.path.abspath(" "+sys.argv[0])+" --runfile "+ tmp_configfile

		elif pexpect.which('su') != None:
			print(_("Please, enter the root password."))
			root_instance = str(pexpect.which('su')) + " - -c \'"+ os.path.abspath(sys.argv[0])+" --runfile "+ tmp_configfile+"\'" 
			
		else:
			sys.stderr.write(_("Error: No substitute user command available.\n"))
			return 1
		if gui:
			pass
		else:
			password=getpass.getpass()
		
		child = pexpect.spawn(root_instance)
		child.expect([".*:",pexpect.EOF]) #Could we do more ?
		child.sendline(password)



def action(category,dumpfile,configfile,tmp_configfile,verbosity, pastebin_choice,website):
	#####################
	# Write in dumpfile
	#####################
	dumpfile_handler= open(dumpfile,'w')

	io.print_write_header(dumpfile_handler)

	dumpfile_handler.write('Category: '+ category+'\n')	

	category_info = readconf.LoadCategoryInfo(configfile,category)
	
	#need/want to run commands as...
	run_as = RunAs(category_info)

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
	CompleteReportRoot(run_as,tmp_configfile)


	# Message to close the report
	dumpfile_handler= open(dumpfile,'a')
	io.write_title(_("You didn\'t find what you expected?"),dumpfile_handler)
	dumpfile_handler.write( _('Please, fill in a bug report on\nhttp://github.com/sciunto/inforevealer\n'))
	dumpfile_handler.close()

	print( _("The output has been dumped in ")+dumpfile)

	
	#if desired, send the report on pastebin
	if pastebin_choice:
		pastebin.sendFileContent(dumpfile,title=category,website=website,version=None)
