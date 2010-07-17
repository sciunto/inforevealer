#!/usr/bin/python
# -*- coding: utf-8 -*-



import os
import time
import sys
from subprocess import PIPE,Popen


def usage():
	print("""
usage:		sys.argv[0] [options]

options:
		-h or --help: print this help
		-l or --list: print a trouble category list
		-c or --category [arg]: choose a category
		--verbose: increase verbosity
		"""
		)
		
		
def list():
	print("""
List:
	* disk
	* hardware
	* display
	* sound
	* bootloader
	* internet
	* package
Reminder: 
	sys.argv[0] -c internet
	""")


def write_header(string,output):
	header= '#############################################'
	header= header + '\n' + '#   ' + str(string) + '\n'
	header=header+'#############################################'
	print(header)
	output.write(header)


class Command:
	"get a command output"
	def __init__(self, com=["uname"], root=False,verb=False,linux=None):
		self.command=com
		self.root=root
		self.verb=verb
		self.linux_dependant=linux

	def write(self,os,output='output.log'):
		import os
		import subprocess
		# correct OS or this info does not dependant on distrib ?
		if self.linux_dependant == os or self.linux_dependant == None:
			write_header(self.command,output)
			if(not os.getuid() == 0 and self.root):
				print("To get this, run the script as root")
				output.write("To get this, run the script as root\n")
			else:
				proc = subprocess.Popen(self.command,stdout=subprocess.PIPE)
				proc.wait()
				foo = proc.stdout.read()
				print(foo)
				output.write(foo)

class File:
	"get a file"
	def __init__(self, file="/dev/null", root=False,verb=False,linux=None):
		self.file=file
		self.root=root
		self.verb=verb
		self.linux_dependant=linux

	def write(self,os,output='output.log'):
		import os
		#import pdb; pdb.set_trace()

		# correct OS or this info does not dependant on distrib ?
		if self.linux_dependant == os or self.linux_dependant == None:
			write_header(self.file,output)
			if(not os.getuid() == 0 and self.root):
				print("To get this, run the script as root")
				output.write("To get this, run the script as root\n")
			else:
				if os.path.isfile(self.file):
					fhandler= open(self.file,'r')
					t = fhandler.read()
					print(t)
					output.write(t)
					fhandler.close()
				else:
					print("The file "+str(self.file)+ " does not exist!")
					output.write("The file "+str(self.file)+ " does not exist!")


def general_info(output):
	import time
	import os
	import subprocess
	write_header('General information',output)

	time = time.gmtime()
	print("date: "+ str(time[0])+"-"+str(time[1])+"-"+str(time[2])+" "+str(time[3])+ ":"+str(time[4]))

	uname = subprocess.Popen(args=["uname","-a"],stdout=subprocess.PIPE).communicate()[0]
	print("uname: "+str(uname))



	# detect linux distribution
	if(os.path.isfile("/etc/fedora-release")):
		os='fedora'
		fhandler=open("/etc/fedora-release")
		print(fhandler.read())
		fhandler.close()
	elif(os.path.isfile("/etc/SuSe-release")):
		os='suse'
		fhandler=open("/etc/SuSe-release")
		print(fhandler.read())
		fhandler.close()
	elif(os.path.isfile("/etc/mandriva-release")):
		os='mandriva'
		fhandler=open("/etc/mandriva-release")
		print(fhandler.read())
		fhandler.close()
	elif(os.path.isfile("/etc/readhat-release")):
		os='redhat'
		fhandler=open("/etc/mandriva-release")
		print(fhandler.read())
		fhandler.close()
	elif(os.path.isfile("/etc/debian_version")):
		os='debian'
		fhandler=open("/etc/debian_version")
		print(fhandler.read())
		fhandler.close()
	else:
		os='unknown'
		print('Your distribution is unknown. Please, open a bug report with the command ls /etc.')
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

	#http://www.doughellmann.com/PyMOTW/getopt/

	#####################
	# GETOPT
	#####################
	options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hlc:f:', ['help',
								   'list',
								   'category=',
								   'verbosity',
								   'file='
								 ])
								 

	for opt, arg in options:
		if opt in ('-h', '--help'):
			usage()
			sys.exit()
		elif opt in ('-l', '--list'):
			list_args()
			sys.exit()
		elif opt in ('-c', '--category'):	
			category=arg
		elif opt in ('--verbosity'):
			verbosity=True
		elif opt in ('-f','--file'):
			dumpfile=arg
	
	###########
	# FILES & COMMANDS
	###########
	#wiki.mandriva.com/en/Docs/Hardware

	list_category=('disk','hardware','display','sound','bootloader','internet','package')

	disk = (Command(["df","-h"]),
			Command(["fdisk", "-l"],root=True),
			File("/etc/fstab"),
			Command(["blkid"],root=True))


	hardware = (Command(["lsmod"],root=True),
		    Command(["lsusb"],root=True))

	#lspci -vvv  Display  VGA
	#display = (File("/etc/X11/xorg.conf")
	#		)+ hardware


	#lspci -vvv Audio
	sound = (Command(['/sbin/chkconfig','--list', 'sound'],root=True), #configured runlevel 3 ? checkme
		 Command(['/sbin/chkconfig','--list', 'alsa'],root=True),
		 Command(['aumix', '-q']), # Volume ?
		 Command(['/sbin/fuser', '-v', '/dev/dsp']) # what is in use ?
		 )+hardware

	bootloader= (File('/boot/grub/menu.lst',root=True),
			File("/etc/default/grub",root=True),
			)+ disk

	#lspci
	internet = (Command(["ifconfig"],root=True),
			Command(["iwconfig"],root=True))+hardware

	package = (File('/etc/urpmi/urpmi.cfg',linux='mandriva'),
			File('/etc/apt/preferences',linux='debian'),
			File('/etc/apt/source.list',linux='debian'))

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
			https://sourceforge.net/projects/inforevealer/
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			
			'''
	print(header)
	dumpfile_handler.write(header)	

	if category in list_category:
		os=general_info(dumpfile_handler)
		for i in locals()[category]:
			if not (not verbosity and i.verb):
				i.write(os,output=dumpfile_handler)
			# is equivalent to
			# if user asks verbosity, then print all
			# else print not verb only
	else:
		print('Wrong category')
		usage()
		list()
		sys.exit()

	dumpfile_handler.close()


#####################
# run main
#####################
if __name__ == "__main__":
	    main(sys.argv[1:])

