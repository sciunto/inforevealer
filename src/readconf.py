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
		#could not be something else thanks to the config check
	return ret_list



