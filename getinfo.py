# -*- coding: utf-8 -*-

import io
import os
import subprocess

class Command:
	"get a command output"
	def __init__(self, com=["uname"], root=False,verb=False,linux=None):
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
					#print("To get this, run the script as root")
					output.write("To get this, run the script as root\n")
				else:
					pass #FIXME
					#proc = subprocess.Popen(self.command,stdout=subprocess.PIPE)
					#foo = proc.stdout.read()
					#proc.wait()
					#print(foo)
					#output.write(foo)
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
					#print("To get this, run the script as root")
					output.write("To get this, run the script as root\n")
				else:
					if os.path.isfile(self.file):
						fhandler= open(self.file,'r')
						t = fhandler.read()
						#print(t)
						output.write(t)
						fhandler.close()
					else:
						#print("The file "+str(self.file)+ " does not exist!")
						output.write("The file "+str(self.file)+ " does not exist!")
		else:
			output.write('Use verbose option (-v) to print this file.')
