#!/usr/bin/python
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


import getinfo
import io
import pastebin
import which
import readconf


import os, sys, time, urllib, re, gettext, string, stat,configobj
from subprocess import PIPE,Popen

from validate import Validator
from configobj import ConfigObj

import string
gettext.textdomain('inforevealer')
_ = gettext.gettext

def usage():
	print _("""
usage:		%s [options]

options:
		-h or --help: print this help
		-l or --list: print a trouble category list
		-c or --category [arg]: choose a category
		-f or --file [arg]: dump file
		-p or --pastebin: send the report on pastebin
		-w or --website [arg]: specify pastebin website
		--verbose: increase verbosity
		""") %sys.argv[0] 
		
		
def list(categories):
	print _("""
List of categories:""")

	for i in categories:
		print ("\t* "+i+" -> "+categories[i])
	print _("\nReminder: %s -c internet") %sys.argv[0] 





def askYesNo(question,default='y'):
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
		


#####################
#Main part
#####################
def main(argv):
	try:
		import getopt
		import sys

		version=0.1

		#set default
		dumpfile='/tmp/inforevealer'
		verbosity=False
		category=""
		runfile=None #option only for internal use, see above

		defaultPB = "http://pastebin.com" #Default pastebin
		website = defaultPB
		pastebin_choice=False

		#look for categories.conf in differents directories
		if os.access('/etc/inforevealer.d/categories.conf',os.R_OK):
			filename="/etc/inforevealer.d/categories.conf"
		elif os.access(os.path.join(os.path.dirname(__file__), 'inforevealer.d/categories.conf'),os.R_OK):
			filename="inforevealer.d/categories.conf"
		else:
			sys.stderr.write(_("Error: No categories.conf available.\n"))
			sys.exit(1)

		#look for validator.conf in differents directories
		if os.access('/etc/inforevealer.d/validator.conf',os.R_OK):
			spec_filename="/etc/inforevealer.d/validator.conf"
		elif os.access(os.path.join(os.path.dirname(__file__), 'inforevealer.d/validator.conf'),os.R_OK):
			spec_filename="inforevealer.d/validator.conf"
		else:
			sys.stderr.write(_("Error: No validator.conf available.\n"))
			sys.exit(1)

		tmp_configfile="/tmp/inforevealer_tmp.conf" #tmp configuration file (substitute)

		###########
		# Open config files
		###########





		try:
			configspec = ConfigObj(spec_filename, interpolation=False, list_values=False,_inspec=True)
		except configobj.ConfigObjError, e:
			sys.stderr.write('%s: %s' % (filename, e))
			sys.exit(1)

		try:
			configfile = ConfigObj(filename, configspec=configspec)
		except configobj.ConfigObjError, e:
			sys.stderr.write('%s: %s' % (filename, e))
			sys.exit(1)
		#check if configfile respects specs
		if configfile.validate(Validator()) == True:
			list_category=readconf.LoadCategoryList(configfile)
		else:
			sys.stderr.write(_("Error: the configuration file %s is not valid.\nSee %s for a template.\n") % (filename,spec_filename))  
			sys.exit(1)





		#####################
		# GETOPT
		#####################
		try:	
			options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hlc:vf:pw:', ['help',
									   'list',
									   'category=',
									   'verbose',
									   'file=',
									   'pastebin',
									   'website',
									   'runfile='
									 ])
									 
		except getopt.GetoptError:
			sys.stderr.write(_("Invalid arguments."))
			usage()
			sys.exit(1)

		for opt, arg in options:
			if opt in ('-h', '--help'):
				usage()
				sys.exit()
			elif opt in ('-l', '--list'):
				list(list_category)
				sys.exit()
			elif opt in ('-c', '--category'):	
				category=arg
			elif opt in ('-v','--verbose'):
				verbosity=True
			elif opt in ('-f','--file'):
				dumpfile=arg
			elif opt in ('-p','--pastebin'):
				pastebin_choice=True
			elif opt in ('-w','--website'):
				website=arg
				if not website.endswith("/"):
					website += "/"
			elif opt in ('--runfile'):
				runfile=arg

		#First to do: runfile (internal use)
		if runfile != None:
			#TODO > in readconf.py
			try:
				config = ConfigObj(tmp_configfile)
			except configobj.ConfigObjError, e:
				sys.stderr.write('%s: %s' % (filename, e))
				sys.exit(1)
			for section in config.sections:
				descr=config[section]['descr']
				e_type=config[section]['type']
				execu=config[section]['exec']
				root=config[section]['root']
				verb=config[section]['verb']
				linux=config[section]['linux_distribution']
				dumpfile=config[section]['dumpfile']
				if e_type == 'command':
				       com=getinfo.Command(section,execu.split(" "),root,verb,linux)
				elif e_type == 'file':
				       com=getinfo.File(section,execu,root,verb,linux)
				dumpfile_handler= open(dumpfile,'a')
				com.write(linux,verb,dumpfile_handler,dumpfile,"root",None)
				dumpfile_handler.close()
			sys.exit()
		#check if category is ok
		elif category in list_category:
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
				pastebin.sendFileContent(dumpfile,title=category,website=website,version=version)
		
		else:
			sys.stderr.write(_('Error: Wrong category'))
			usage()
			sys.exit(1)
	
	except KeyboardInterrupt:
		sys.exit(_("KeyboardInterrupt caught."))



#####################
# run main
#####################
if __name__ == "__main__":
	    main(sys.argv[1:])


