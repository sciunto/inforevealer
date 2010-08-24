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

import io #outputs...
import readconf #read categories
import action # main part...

import sys, time, gettext, string

from pastebin import sendFileContent


gettext.textdomain('inforevealer')
_ = gettext.gettext

__version__="0.5.1"

#####################
#Main part
#####################
def main(argv):
	try:
		import getopt
		import sys

		

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
				#find categories.conf
				filename=readconf.find_categories_conf()
				#find validator.conf
				spec_filename=readconf.find_validator_conf()
				#open categories.conf with validator.conf
				configfile=readconf.open_config_file(filename,spec_filename)
				# load the list of categories
				list_category=readconf.LoadCategoryList(configfile)
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
			readconf.ReadAndMakeInternalDesire(tmp_configfile)
			sys.exit()
		else:
			#find categories.conf
			filename=readconf.find_categories_conf()
			#find validator.conf
			spec_filename=readconf.find_validator_conf()
			#open categories.conf with validator.conf
			configfile=readconf.open_config_file(filename,spec_filename)
			# load the list of categories
			list_category=readconf.LoadCategoryList(configfile)
			
			if gui==True:
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
		sys.exit("KeyboardInterrupt caught.")



#####################
# run main
#####################
if __name__ == "__main__":
	    main(sys.argv[1:])
        

