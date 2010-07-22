# -*- coding: utf-8 -*-

import io
import os
import subprocess
import time



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
			
			
			
			
			
			
			


def General_info(output):

	io.write_header('General information',output)

	mytime = time.gmtime()
	output.write("date: "+ str(mytime[0])+"-"+str(mytime[1])+"-"+str(mytime[2])+" "+str(mytime[3])+ ":"+str(mytime[4])+"\n")
	#print("date: "+ str(time[0])+"-"+str(time[1])+"-"+str(time[2])+" "+str(time[3])+ ":"+str(time[4]))

	uname = subprocess.Popen(args=["uname","-a"],stdout=subprocess.PIPE).communicate()[0]
	output.write("uname: "+str(uname)+"\n")
	#print("uname: "+str(uname))



	# detect linux distribution
	if(os.path.isfile("/etc/fedora-release")):
		myos='fedora'
		fhandler=open("/etc/fedora-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/SuSe-release")):
		myos='suse'
		fhandler=open("/etc/SuSe-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/mandriva-release")):
		myos='mandriva'
		fhandler=open("/etc/mandriva-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/redhat-release")):
		myos='redhat'
		fhandler=open("/etc/redhat-release")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	elif(os.path.isfile("/etc/debian_version")):
		myos='debian'
		fhandler=open("/etc/debian_version")
		foo=fhandler.read()
		fhandler.close()
		output.write(foo)
		#print(fhandler.read())
	else:
		myos='unknown'
		#print('Your distribution is unknown. Please, open a bug report with the command ls /etc.')
		output.write('Your distribution is unknown. Please, open a bug report with the command ls /etc.')
	return myos


