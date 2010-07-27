#!/usr/bin/env python


from configobj import ConfigObj

filename="conf.conf"
spec_filename="validator.conf"
#config = ConfigObj(filename)

from validate import Validator
configspec = ConfigObj(spec_filename, interpolation=False, list_values=False,
		                       _inspec=True)
config = ConfigObj(filename, configspec=configspec)

val = Validator()
test = config.validate(val)
if test == True:
	print 'Succeeded.'
else:
	print 'failed'


#Load category list
def LoadCategoryList():
	list_category=dict()
	for section in config.sections:
		list_category[section]=config[section]['descr'] 
	return list_category

#Load info on a category
def LoadCategoryInfo(category):
	ret_list = list()
	for subsection in config[category].sections:
		print subsection
		descr=config[category][subsection]['descr']
		type=config[category][subsection]['type']
		execu=config[category][subsection]['exec']
		root=config[category][subsection]['root']
		verb=config[category][subsection]['verb']
		#linux=config[category][subsection]['linux']
		print verb
		if type == 'command':	
			ret_list.append("")
		elif type == 'file':
			ret_list.append("")
		else:
			print('Error') #TODO
	return ret_list

LoadCategoryInfo('disk')


