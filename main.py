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

import os
import time
import sys
from subprocess import PIPE,Popen


def usage():
	print("""
usage:		"""+sys.argv[0]+""" [options]

options:
		-h or --help: print this help
		-l or --list: print a trouble category list
		-c or --category [arg]: choose a category
		-f or --file [arg]: dump file
		--verbose: increase verbosity
		"""
		)
		
		
def list(categories):
	print("""
List of categories:""")

	for i in categories:
		print("\t* "+i+" -> "+categories[i])
	print("""Reminder: 
	"""+sys.argv[0]+""" -c internet
	""")






#####################
#Main part
#####################
def main(argv):
	import getopt
	import sys

	dumpfile='/tmp/inforevealer'
	verbosity=False
	category=None

	###########
	# FILES & COMMANDS
	###########
	#wiki.mandriva.com/en/Docs/Hardware

	list_category={ 'disk':"Volumes, sizes, UUID...",
			'cpu':"All CPU info",
			'hardware':"General hardware information which are not included in other items",
			'display':"Xorg, monitor info...",
			'sound':"",
			'bootloader':'Everything on grub and partitions (include "disk")',
			'internet':'Wifi, ethernet...',
			'package':"List of reprositories..."
			}

# dmesg
# /var/log/messages

	disk = (getinfo.Command(["df","-h"]),
		getinfo.Command(["fdisk", "-l"],root=True),
		getinfo.File("/etc/fstab"),
		getinfo.Command(["blkid"],root=True)
		)

	cpu = (getinfo.Command(["lscpu"],root=True),
		getinfo.File("/proc/cpuinfo",root=True),
		getinfo.Command(["cpufred-info"],root=True)
		)

	#temperature=(getinfo.Command(["sensors"]))

	hardware = (
		    getinfo.Command(["lsmod"],root=True), #hummm
		    getinfo.Command(["lsusb"],root=True),
		    getinfo.Command(["lspci","-v"],root=True),
		    getinfo.Command(["lshal"],root=True,verb=True),
		    getinfo.Command(["lshw"],root=True,verb=True)
		    )

	#lspci -vvv  Display  VGA
	display = (getinfo.File("/etc/X11/xorg.conf"),
			getinfo.File('/var/log/Xorg.0.log',root=True),
			getinfo.Command("monitor-edid",root=True)
			)


	#lspci -vvv Audio
	sound = (
		 getinfo.Command(['aumix', '-q']), # Volume ?
		 getinfo.Command(['/sbin/fuser', '-v', '/dev/dsp'],root=True) # what is in use ?
		 )
	
	bootloader= (getinfo.File('/boot/grub/menu.lst',root=True),
			getinfo.File("/etc/default/grub",root=True),
			getinfo.File("/etc/lilo.conf",root=True),
			)+ disk

	#lspci
	internet = (getinfo.Command(["ping","-c","1","www.kernel.org"]),
		    getinfo.Command(["ifconfig"],root=True),
		    getinfo.Command(["iwconfig"],root=True),
		    getinfo.File("/etc/resolv.conf"),	
		    getinfo.File("/etc/hosts")	
	            )

	package = (getinfo.File('/etc/urpmi/urpmi.cfg',linux='mandriva'),
			getinfo.File('/etc/urpmi.skip.list',linux='mandriva'),
			getinfo.File('/etc/yum.conf',linux='fedora'),
			getinfo.File('/etc/yum.conf',linux='suse'),
			getinfo.File('/etc/apt/preferences',linux='debian'),
			getinfo.File('/etc/apt/source.list',linux='debian'))

	#####################
	# GETOPT
	#####################
	options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hlc:vf:', ['help',
								   'list',
								   'category=',
								   'verbose',
								   'file='
								 ])
								 

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
	
	#####################
	# PASTEBIN
	#####################
#	defaultPB = "http://pastebin.com" #Default pastebin
#
#	# Set defaults
#	website = defaultPB
#	user = os.environ.get('USER')
#	jabberid = ""
#	title = ""
#	permatag = ""
#	format = "text"
#	username = ""
#	password = ""
#	filename = ""
#	content = ""
#	parentpid = ""
#
##This is what we should do
##content should content the content :)
#
#	pastebind = preloadPastebins() #get the config from /etc/pastebin.d/
#	params = getParameters(website, pastebind, content, user, jabberid, version, format, parentpid, permatag, title, username, password) #Get the parameters array
#
#	if not website.endswith("/"):
#		website += "/"
#
#	reLink = None
#	tmp_page = ""
#	if "page" in params:
#		website += params['page']
#		tmp_page = params['page']
#		del params["page"]
#	if "regexp" in params:
#		reLink = params['regexp']
#		del params["regexp"]
#	params = urllib.urlencode(params) #Convert to a format usable with the HTML POST
#
#	url_opener = pasteURLopener()
#	page = url_opener.open(website, params) #Send the informations and be redirected to the final page
#
#	try:
#		if reLink: #Check if we have to apply a regexp
#			website = website.replace(tmp_page, "")
#			if reLink == '(.*)':
#				print page.read().strip()
#			else:
#				print website + re.split(reLink, page.read())[1] #Print the result of the Regexp
#		else:
#			print page.url #Get the final page and show the ur
#	except KeyboardInterrupt:
#		sys.exit(_("KeyboardInterrupt caught."))
#	except:
#		raise
#		sys.exit(_("Unable to read or parse the result page, it could be a server timeout or a change server side, try with another pastebin."))
#
#

	#####################
	# Write in dumpfile
	#####################
	dumpfile_handler= open(dumpfile,'w')

	header = '''
					~~~~~~~~~~~~~~~
					Log generated by 
					  Inforevealer
					~~~~~~~~~~~~~~~
			Distributed under the GNU GPLv2 licence
			Francois Boulogne <fboulogne at april dot org>
			    http://github.com/sciunto/inforevealer
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
	print(header)
	dumpfile_handler.write(header)	

	if category in list_category:
		linux_distrib=getinfo.General_info(dumpfile_handler)
		for i in locals()[category]:
			i.write(linux_distrib,verbosity,dumpfile_handler)
		io.write_header("You didn\'t find what you expected?",dumpfile_handler)
		dumpfile_handler.write('Please, fill in a bug report on\nhttp://github.com/sciunto/inforevealer')
	else:
		print('Error: Wrong category')
		usage()
		list(list_category)
		sys.exit()

	dumpfile_handler.close()
	print("The output has been dumped in "+dumpfile)


#####################
# run main
#####################
if __name__ == "__main__":
	    main(sys.argv[1:])

