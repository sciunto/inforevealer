
import os
import time
from subprocess import PIPE,Popen


def write_header(string):
	header= '#############################################'
	header= header + '\n' + '#   ' + string + '\n'
	header=header+'#############################################'
	print(header)



class Command:
	"get a command output"
	def __init__(self, com="uname", root=False):
		self.command=com
		self.root=root

	def write(self):
		write_header(self.command)
		os.system(self.command)



class File:
	"get a file"
	def __init__(self, file="uname", root=False):
		self.file=file
		self.root=root

	def write(self):
		write_header(self.file)
		if (exists(self.file)):
			fhandler= open(self.file,'r')
			t = fhandler.read()
			print(t)
			fhandler.close()
		else:
			print("the file self.file does not exist!")
		



disk = (Command("df -h"),
		Command("fdisk -l",True),
		Command("blkid",True))







#####################
#Main part
####################



print('''
		Software title
		licence
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
		''')

write_header('General information')

time = time.gmtime()
print("date: "+ str(time[0])+"-"+str(time[1])+"-"+str(time[2])+" "+str(time[3])+ ":"+str(time[4]))

uname = Popen(args=["uname","-a"],stdout=PIPE).communicate()[0]
print("uname: "+str(uname))

# detect linux distribution

if(exists(/etc/fedora-release):
	os=fedora
else if(exists(/etc/SuSe-release):
	os=suse
else if(exists(/etc/mandriva-release):
	os=mandriva
else if(exists(/etc/readhat-release):
	os=redhat
else if(exists(/etc/debian_version)):
	os=debian
else:
	os=unknown




for i in disk:
	i.write()




