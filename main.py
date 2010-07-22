#!/usr/bin/python
# -*- coding: utf-8 -*-



#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

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





def general_info(output):
	import time
	import os
	import subprocess
	io.write_header('General information',output)

	time = time.gmtime()
	output.write("date: "+ str(time[0])+"-"+str(time[1])+"-"+str(time[2])+" "+str(time[3])+ ":"+str(time[4])+"\n")
	#print("date: "+ str(time[0])+"-"+str(time[1])+"-"+str(time[2])+" "+str(time[3])+ ":"+str(time[4]))

	uname = subprocess.Popen(args=["uname","-a"],stdout=subprocess.PIPE).communicate()[0]
	output.write("uname: "+str(uname)+"\n")
	#print("uname: "+str(uname))



	# detect linux distribution
	if(os.path.isfile("/etc/fedora-release")):
		os='fedora'
		fhandler=open("/etc/fedora-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/SuSe-release")):
		os='suse'
		fhandler=open("/etc/SuSe-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/mandriva-release")):
		os='mandriva'
		fhandler=open("/etc/mandriva-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/redhat-release")):
		os='redhat'
		fhandler=open("/etc/redhat-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/debian_version")):
		os='debian'
		fhandler=open("/etc/debian_version")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	else:
		os='unknown'
		#print('Your distribution is unknown. Please, open a bug report with the command ls /etc.')
		output.write('Your distribution is unknown. Please, open a bug report with the command ls /etc.')
	return os




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
		linux_distrib=general_info(dumpfile_handler)
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

