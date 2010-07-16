
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

	def write(self,filename='output.log'):
		import os
		write_header(self.command)
		if(os.getuid() == 0):
			#os.system(self.command)
			print("TODO")
		else:
			print("To get this, run the script as root")


class File:
	"get a file"
	def __init__(self, file="/dev/null", root=False):
		self.file=file
		self.root=root

	def write(self,filename='output.log'):
		import os
		#import pdb; pdb.set_trace()

		write_header(self.file)
		if(os.getuid() == 0):
			if os.path.isfile(self.file): # FIXME
				fhandler= open(self.file,'r')
				t = fhandler.read()
				print(t)
				fhandler.close()
			else:
				print("the file self.file does not exist!")
		else:
			print("To get this, run the script as root")
###########
# FILES & COMMANDS
###########


disk = (Command("df -h"),
		Command("fdisk -l",True),
		File("/etc/fstab"),
		Command("blkid",True))

#lspci -vvv  Display  VGA
display = (File("/etc/X11/xorg.conf")
		)


#lspci -vvv Audio
sound = ()

bootloader= (File('/boot/grub/menu.lst',True),
		File("/etc/default/grub",True),
		)+ disk

#lspci
internet = (Command('ifconfig',True),
		Command('iwconfig',True))


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




for i in bootloader:
	i.write()




