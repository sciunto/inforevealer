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


import io
import os
import subprocess
import time



class Command:
	"get a command output"
	def __init__(self, com, root=False,verb=False,linux=None):
		self.command=com
		self.root=root # need root?
		self.verb=verb # is it verbose?
		self.linux_dependant=linux # need a specific os?

	def write(self,user_os,verbosity,output):
		io.write_header(self.command,output)
			# the following condition is equivalent to
			# if user asks verbosity, then print all
			# else print not verb only
		if not (not verbosity and self.verb):
			# correct OS or this info does not dependant on distrib ?
			if self.linux_dependant == user_os or self.linux_dependant == None:
				if(not os.getuid() == 0 and self.root):
					output.write("To get this, run the script as root\n")
				else:
					proc = subprocess.Popen(self.command,stdout=subprocess.PIPE)
					output.write( proc.stdout.read() )
		else:
			output.write('Use verbose option (-v) to print this command.')
class File:
	"get a file"
	def __init__(self, file="/dev/null", root=False,verb=False,linux=None):
		self.file=file
		self.root=root # need root?
		self.verb=verb # is it verbose?
		self.linux_dependant=linux # need a specific distribution?

	def write(self,user_os,verbosity,output):
		import os
		#import pdb; pdb.set_trace()

			# the following condition is equivalent to
			# if user asks verbosity, then print all
			# else print not verb only
		if not (not verbosity and self.verb):
			# correct OS or this info does not dependant on distrib ?
			if self.linux_dependant == user_os or self.linux_dependant == None:
				io.write_header(self.file,output)
				if(not os.getuid() == 0 and self.root):
					output.write("To get this, run the script as root\n")
				else:
					if os.path.isfile(self.file):
						fhandler= open(self.file,'r')
						output.write( fhandler.read() )
						fhandler.close()
					else:
						output.write("The file "+str(self.file)+ " does not exist!")
		else:
			output.write('Use verbose option (-v) to print this file.')
			
			
			
			
			
			
			


def General_info(output):

	io.write_header('General information',output)

	mytime = time.gmtime()
	output.write("date: "+ str(mytime[0])+"-"+str(mytime[1])+"-"+str(mytime[2])+" "+str(mytime[3])+ ":"+str(mytime[4])+"\n")

	uname = subprocess.Popen(args=["uname","-a"],stdout=subprocess.PIPE).communicate()[0]
	output.write("uname: "+str(uname)+"\n")



	# detect linux distribution
	if(os.path.isfile("/etc/fedora-release")):
		myos='fedora'
		fhandler=open("/etc/fedora-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
	elif(os.path.isfile("/etc/SuSe-release")):
		myos='suse'
		fhandler=open("/etc/SuSe-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
	elif(os.path.isfile("/etc/mandriva-release")):
		myos='mandriva'
		fhandler=open("/etc/mandriva-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
	elif(os.path.isfile("/etc/redhat-release")):
		myos='redhat'
		fhandler=open("/etc/redhat-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
	elif(os.path.isfile("/etc/debian_version")):
		myos='debian'
		fhandler=open("/etc/debian_version")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
	else:
		myos='unknown'
		output.write('Your distribution is unknown. Please, open a bug report with the command ls /etc.')
	return myos


