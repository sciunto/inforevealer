#!/usr/bin/env python
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

import getinfo
import os
import re
import locale
import sys

import configobj
from validate import Validator
from configobj import ConfigObj

def find_categories_conf():
	#what locale is used?
	lang = locale.getdefaultlocale()[0]
	if lang!=None:
		lang = re.sub('_.*','',lang)
		loc_path=os.path.join('inforevealer.d/',lang,'categories.conf')
	else:
		loc_path=os.path.join('inforevealer.d/','categories.conf')
	filename=None
	#look for categories.conf in differents directories for the current locale
	if os.access('/etc/'+loc_path,os.R_OK):
		filename='/etc/'+loc_path
	elif os.access(os.path.join(os.path.dirname(__file__), '../'+loc_path),os.R_OK):
		filename='../'+loc_path
	if filename==None: #not yet found
		#use the default file (english)
		if os.access('/etc/inforevealer.d/categories.conf',os.R_OK):
			filename="/etc/inforevealer.d/categories.conf"
		elif os.access(os.path.join(os.path.dirname(__file__), '../inforevealer.d/categories.conf'),os.R_OK):
			filename="../inforevealer.d/categories.conf"
		else:
			sys.stderr.write(_("Error: No categories.conf available.\n"))
			sys.exit(1)
	return filename

def find_validator_conf():
	#look for validator.conf in differents directories
	if os.access('/etc/inforevealer.d/validator.conf',os.R_OK):
		spec_filename="/etc/inforevealer.d/validator.conf"
	elif os.access(os.path.join(os.path.dirname(__file__), '../inforevealer.d/validator.conf'),os.R_OK):
		spec_filename="../inforevealer.d/validator.conf"
	else:
		sys.stderr.write(_("Error: No validator.conf available.\n"))
		sys.exit(1)
	return spec_filename

	###########
	# Open config files
	###########
def open_config_file(filename,spec_filename):
	try:
		configspec = ConfigObj(spec_filename, interpolation=False, list_values=False,_inspec=True)
	except configobj.ConfigObjError, e:
		sys.stderr.write('%s: %s' % (filename, e))
		sys.exit(1)

	try:
		configfile = ConfigObj(filename, configspec=configspec)
	except configobj.ConfigObjError, e:
		sys.stderr.write('%s: %s' % (filename, e))
		sys.exit(1)
	#check if configfile respects specs
	if configfile.validate(Validator()) == True:
		return configfile
	else:
		sys.stderr.write(_("Error: the configuration file %(file1)s is not valid.\nSee %(file2)s for a template.\n") % {'file1':filename,'file2':spec_filename})  
		sys.exit(1)



#Load category list
def LoadCategoryList(config):
	list_category=dict()
	for section in config.sections:
		list_category[section]=config[section]['description'] 
	return list_category

#Load info on a category
def LoadCategoryInfo(config,category):
	ret_list = list()
	for subsection in config[category].sections:
		descr=config[category][subsection]['description']
		e_type=config[category][subsection]['type']
		execu=config[category][subsection]['exec']
		root=config[category][subsection]['root']
		verb=config[category][subsection]['verbose']
		linux=config[category][subsection]['distribution']

		if e_type == 'command':	
			ret_list.append(getinfo.Command(subsection,execu.split(" "),root,verb,linux))
		elif e_type == 'file':
			ret_list.append(getinfo.File(subsection,execu,root,verb,linux))
		elif e_type == 'directory':
			ret_list.append(getinfo.Directory(subsection,execu,root,verb,linux))
		#could not be something else thanks to the config check
	return ret_list


def ReadAndMakeInternalDesire(tmp_configfile):
	try:
		config = ConfigObj(tmp_configfile)
	except configobj.ConfigObjError, e:
		sys.stderr.write('%s: %s' % (filename, e))
		sys.exit(1)
	for section in config.sections:
		descr=config[section]['description']
		e_type=config[section]['type']
		execu=config[section]['exec']
		root=config[section]['root']
		verb=config[section]['verb']
		linux=config[section]['linux_distribution']
		dumpfile=config[section]['dumpfile']
		if e_type == 'command':
			com=getinfo.Command(section,execu.split(" "),root,verb,linux)
		elif e_type == 'file':
			com=getinfo.File(section,execu,root,verb,linux)
		elif e_type == 'directory':
			com=getinfo.Directory(section,execu,root,verb,linux)
		dumpfile_handler= open(dumpfile,'a')
		com.write(linux,verb,dumpfile_handler,dumpfile,"root",None)
		dumpfile_handler.close()
