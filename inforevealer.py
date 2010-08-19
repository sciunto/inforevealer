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


import getinfo #Get info from commands and files
import io #outputs...
import readconf #read categories
import action # main part...


import os, sys, time, urllib, re, gettext, string, stat,configobj, locale, string
#from subprocess import PIPE,Popen

from validate import Validator
from configobj import ConfigObj
from pastebin import sendFileContent


gettext.textdomain('inforevealer')
_ = gettext.gettext


#####################
#Main part
#####################
def main(argv):
	try:
		import getopt
		import sys

		version=0.4

		#set default
		dumpfile='/tmp/inforevealer'
		tmp_configfile="/tmp/inforevealer_tmp.conf" #tmp configuration file (substitute)
		verbosity=False
		category=""
		runfile=None #option only for internal use, see above
		gui=False #run the GUI

		defaultPB = "http://pastebin.com" #Default pastebin
		website = defaultPB
		pastebin_choice=False

		#what locale is used?
		lang = locale.getdefaultlocale()[0]
		lang = re.sub('_.*','',lang)
		loc_path='inforevealer.d/'+str(lang)+'/categories.conf'
		filename=None
		#look for categories.conf in differents directories for the current locale
		if os.access('/etc/'+loc_path,os.R_OK):
			filename='/etc/'+loc_path
		elif os.access(os.path.join(os.path.dirname(__file__), loc_path),os.R_OK):
			filename=loc_path
		if filename==None:
			#use the default file (english)
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
			sys.stderr.write(_("Error: the configuration file %(file1)s is not valid.\nSee %(file2)s for a template.\n") % {'file1':filename,'file2':spec_filename})  
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
									   'runfile=',
									   'gui'
									 ])
									 
		except getopt.GetoptError:
			sys.stderr.write(_("Invalid arguments."))
			io.usage()
			sys.exit(1)

		for opt, arg in options:
			if opt in ('-h', '--help'):
				io.usage()
				sys.exit()
			elif opt in ('-l', '--list'):
				io.list(list_category)
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
			elif opt in ('--gui'):
				gui=True

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
		elif gui==True:
			import gui
			gui.main(configfile,list_category)
		#check if category is ok
		elif category in list_category:
			action.action(category,dumpfile,configfile,tmp_configfile,verbosity)
			sendFileContent(dumpfile,title=category,website=website,version=None)
		else:
			sys.stderr.write(_('Error: Wrong category'))
			io.usage()
			sys.exit(1)
	
	except KeyboardInterrupt:
		sys.exit(_("KeyboardInterrupt caught."))



#####################
# run main
#####################
if __name__ == "__main__":
	    main(sys.argv[1:])
        

