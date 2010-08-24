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

import gettext, sys
gettext.textdomain('inforevealer')
_ = gettext.gettext
__version__="devel"

def print_write_header(fhandler):
        header=''' 
                                                ~~~~~~~~~~~~~~~
                                                Log generated by 
                                                 Inforevealer v%s
                                                ~~~~~~~~~~~~~~~
                                   Distributed under the GNU GPLv2 licence
                                Francois Boulogne <fboulogne at april dot org>
                                    http://github.com/sciunto/inforevealer
                                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' %__version__
	print(header)
	fhandler.write(header)
                


def write_title(output, string, substring=None):
	title=""
	if string.__class__ != str:
		for i in string:
			title+= i+" "
        else:
		title=string

	header= '============================================'
	header= header + '\n' + '|   ' + title + '\n'
	if (substring!=None and substring!='True'): #FIXME
		header=header+'|-------------------------------------------\n'
		header=header+'| '+substring+"\n"
	header=header+'============================================\n'
	output.write(header)

def usage():
	print(_("""
Usage:		%s [options]

Options:
		-h or --help: print this help
		-l or --list: print the category list
		-c or --category [arg]: choose a category
		-f or --file [arg]: dump file
		-p or --pastebin: send the report on pastebin
		-w or --website [arg]: specify pastebin website
		--verbose: increase verbosity
		--gui: run a graphic interface (other options are ignored)
		""") %sys.argv[0] )
			
		
def list(categories):
	print _("""
List of categories:""")

	for i in categories:
		print ("\t* "+i+" -> "+categories[i])
	print(_("\nReminder: %(command)s -c %(option)s") % {'command':sys.argv[0], 'option':categories.keys()[0]})
