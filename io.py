# -*- coding: utf-8 -*-
def write_header(string,output):
	title=""
	if string.__class__ != str:
		for i in string:
			title+= i+" "
        else:
		title=string

	header= '#############################################'
	header= header + '\n' + '#   ' + title + '\n'
	header=header+'#############################################\n'
	#print(header)
	output.write(header)