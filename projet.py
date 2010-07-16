
import os

class Command:
	"get a command output"
	def __init__(self, my_com="uname"):
		self.command=my_com

	def write(self):
		os.system(self.command)



class File:
	"get a file"
	def __init__(self, my_file="uname"):
		self.file=my_file

	def write(self):
		fhandler= open(self.file,'r')
		t = fhandler.read()
		print(t)


disk = (Command("fdisk -l"),
		Command("blkid"))


for i in disk:
	i.write()



