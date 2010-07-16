
import os


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
		else:
			print("the file self.file does not exist!")




disk = (Command("df -h"),
		Command("fdisk -l",True),
		Command("blkid",True))


for i in disk:
	i.write()




