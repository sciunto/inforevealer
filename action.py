# -*- coding: utf-8 -*-

import io, readconf, getinfo, which, pastebin
import os, sys, gettext,string

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



def RunAs(category_info):
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
			substitute=askYesNo(_("""To generate a complete report, root access is needed.
Do you want to substitute user?"""))
			if substitute:
				run_as="substitute"
			else:
				run_as="user"
		else:
			run_as='user'
	return run_as

def CompleteReportRoot(run_as,tmp_configfile):
	"""Run a new instance of inforevealer with root priviledge to complete tmp_configfile"""
	if run_as == "substitute":
		#find the substitute user command and run the script	
		if which.which('sudo') != None: #TODO checkme
			print(_("Please, enter your user password."))
			root_instance = str(which.which('sudo')) + os.path.abspath(" "+sys.argv[0])+" --runfile "+ tmp_configfile
			os.system(root_instance)
		elif which.which('su') != None:
			print(_("Please, enter the root password."))
			root_instance = str(which.which('su')) + " - -c \'"+ os.path.abspath(sys.argv[0])+" --runfile "+ tmp_configfile+"\'" 
			os.system(root_instance)
		else:
			sys.stderr.write(_("Error: No substitute user command available.\n"))
		



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
