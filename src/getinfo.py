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
import os, re
import subprocess
import time
from pexpect import which


import gettext
_ = gettext.gettext
__version__="0.5"

class Command:
	"get a command output"
	def __init__(self, category, com, root=False,verb=False,linux=None):
		self.category=category
		self.command=com
		self.root=root # need root?
		self.verb=verb # is it verbose?
		self.linux_dependant=linux # need a specific os?

	def write(self,user_os,verbosity,output,output_path,run_as="user",config_out=None):
			# the following condition is equivalent to
			# if user asks verbosity, then print all
			# else print not verb only
		if not (not verbosity and self.verb):
			# correct OS or this info does not dependant on distrib ?
			if self.linux_dependant == user_os or self.linux_dependant == None:
				path_command=which(self.command[0])
				if path_command != None:	
					#correct the command, keep options
					self.command[0]=path_command
					if self.root:
						if run_as == "user":
							io.write_title(self.command,output)
							output.write("To get this, run the script as root\n")
						elif run_as == "substitute":
							config_out.write("["+self.category+"]\n")
							config_out.write("description=\n")
							config_out.write("type=command\n")
							config_out.write("exec="+' '.join(self.command) +"\n")
							config_out.write("root="+str(self.root)+"\n")
							config_out.write("verb="+str(self.verb)+"\n")
							config_out.write("linux_distribution="+str(self.linux_dependant)+"\n")
							config_out.write("dumpfile="+str(output_path)+"\n")
						elif run_as == 'root':
							io.write_title(self.command,output)
							proc = subprocess.Popen(self.command,stdout=subprocess.PIPE)
							output.write( proc.stdout.read() )
					else:
						io.write_title(self.command,output)
						proc = subprocess.Popen(self.command,stdout=subprocess.PIPE)
						output.write( proc.stdout.read() )
				else:
					io.write_title(self.command,output)
					output.write(_("%s not found! \n") %self.command[0])
		else:
			io.write_title(self.command,output)
			output.write('Use verbose option (-v) to print this command.\n')
			
		
			
	
class File:
	"get a file"
	def __init__(self, category, file, root=False,verb=False,linux=None):
		self.category=category
		#replace ~ by $HOME if needed
		self.file=os.path.expanduser(file)			
		self.root=root # need root?
		self.verb=verb # is it verbose?
		self.linux_dependant=linux # need a specific distribution?

	def write(self,user_os,verbosity,output,output_path,run_as="user",config_out=None):
			# the following condition is equivalent to
			# if user asks verbosity, then print all
			# else print not verb only
		if not (not verbosity and self.verb):
			# correct OS or this info does not dependant on distrib ?
			if self.linux_dependant == user_os or self.linux_dependant == None:
				if self.root:
					if run_as == "user":
						io.write_title(self.file,output)
						output.write("To get this, run the script as root\n")
					elif run_as == "substitute":
						config_out.write("["+self.category+"]\n")
						config_out.write("description=\n")
						config_out.write("type=file\n")
						config_out.write("exec="+str(self.file)+"\n")
						config_out.write("root="+str(self.root)+"\n")
						config_out.write("verb="+str(self.verb)+"\n")
						config_out.write("linux_distribution="+str(self.linux_dependant)+"\n")
						config_out.write("dumpfile="+str(output_path)+"\n")
					elif run_as == "root":
						io.write_title(self.file,output)
						if os.path.isfile(self.file):
							fhandler= open(self.file,'r')
							output.write( fhandler.read() )
							fhandler.close()
						else:
							output.write("The file "+str(self.file)+ " does not exist!\n")
				else:
					io.write_title(self.file,output)
					if os.path.isfile(self.file):
						fhandler= open(self.file,'r')
						output.write( fhandler.read() )
						fhandler.close()
					else:
						output.write("The file "+str(self.file)+ " does not exist!\n")
		else:
			io.write_title(self.file,output)
			output.write('Use verbose option (-v) to print this file.\n')		


class Directory:
	"get the content of a directory"
	def __init__(self, category, directory, root=False,verb=False,linux=None):
		self.category=category
		#replace ~ by $HOME if needed
		self.directory=os.path.expanduser(directory)			
		self.root=root # need root?
		self.verb=verb # is it verbose?
		self.linux_dependant=linux # need a specific distribution?
	
	def write(self,user_os,verbosity,output,output_path,run_as="user",config_out=None):
		# the following condition is equivalent to
		# if user asks verbosity, then print all
		# else print not verb only
		if not (not verbosity and self.verb):
			pass
			#TODO
			# correct OS or this info does not dependant on distrib ?
			if self.linux_dependant == user_os or self.linux_dependant == None:
				if self.root:
					if run_as == "user":
						io.write_title(self.file,output)
						output.write("To get this, run the script as root\n")
					elif run_as == "substitute":
						config_out.write("["+self.category+"]\n")
						config_out.write("description=\n")
						config_out.write("type=directory\n")
						config_out.write("exec="+str(self.directory)+"\n")
						config_out.write("root="+str(self.root)+"\n")
						config_out.write("verb="+str(self.verb)+"\n")
						config_out.write("linux_distribution="+str(self.linux_dependant)+"\n")
						config_out.write("dumpfile="+str(output_path)+"\n")
					elif run_as == "root":
						dirList=os.listdir(self.directory)
						for fname in dirList:
							fname=os.path.join(self.directory,fname)		
							io.write_title(fname,output)
							fhandler= open(fname,'r')
							output.write( fhandler.read() )
							fhandler.close()
				else:
					dirList=os.listdir(self.directory)
					for fname in dirList:
						fname=os.path.join(self.directory,fname)		
						io.write_title(fname,output)
						fhandler= open(fname,'r')
						output.write( fhandler.read() )
						fhandler.close()
		else:
			io.write_title(self.directory,output)
			output.write('Use verbose option (-v) to print this directory content.\n')
		


def General_info(output):

	io.write_title('General information',output)

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
	elif(os.path.isfile("/etc/arch-release")):
		myos='archlinux'
		fhandler=open("/etc/arch-release")
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
		output.write(_('Your distribution is unknown. Please, open a bug report with the command output: ls /etc\n'))
	return myos


