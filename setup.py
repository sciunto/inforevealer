#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is a modified copy of
# the one used in comix project
# released under GNU GPLv2


"""
This script installs or uninstalls Comix on your system.
-------------------------------------------------------------------------------
Usage: install.py [OPTIONS] COMMAND

Commands:
install                  Install to /usr/local

uninstall                Uninstall from /usr/local

Options:
--dir <directory>        Install or uninstall in <directory>
instead of /usr/local

--no-mime                Do not install the file manager thumbnailer
or register new mime types for x-cbz,
x-cbt and x-cbr archive files.
"""

import os
import sys
import shutil
import getopt

source_dir = os.path.dirname(os.path.realpath(__file__))
install_dir = '/usr/local/'
conf_dir = '/etc/'

translations = ('fr',)


def info():
	print(__doc__)
	sys.exit(1)


# ---------------------------------------------------------------------------
# Parse the command line.
# ---------------------------------------------------------------------------
try:
	opts, args = getopt.gnu_getopt(sys.argv[1:], '', ['dir='])
except getopt.GetoptError:
	info()
for opt, value in opts:
	if opt == '--dir':
		install_dir = value
		if not os.path.isdir(install_dir):
			print('\n!!! Error: %s does not exist.' %install_dir) 
			info()


# files: source, destination
files = [
		('src/action.py', 'share/inforevealer/src', install_dir),  
		('src/getinfo.py', 'share/inforevealer/src', install_dir),   
		('src/gui.py',  'share/inforevealer/src', install_dir),  
		('src/inforevealer.py',  'share/inforevealer/src', install_dir),  
		('src/io.py',  'share/inforevealer/src', install_dir),  
		('src/pastebin.py',  'share/inforevealer/src', install_dir),  
		('src/readconf.py', 'share/inforevealer/src', install_dir),
		('icons/inforevealer.svg', 'share/icons/hicolor/scalable/apps', install_dir),
		('inforevealer.d/categories.conf','inforevealer.d', conf_dir),
		('inforevealer.d/validator.conf','inforevealer.d', conf_dir),
		('inforevealer.d/validator.conf','inforevealer.d', conf_dir),
		('inforevealer.d/pastebin/fpaste.org.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/paste2.org.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/pastebin.ca.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/pastebin.com.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/paste.debian.net.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/paste.ubuntu.com.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/pastie.org.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/slexy.org.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/stikked.com.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.d/pastebin/yourpaste.net.conf','inforevealer.d/pastebin', conf_dir),
		('inforevealer.desktop','share/applications/', install_dir),
		('man/inforevealer.1','share/man/man1', install_dir)
		]

#add translations for conf files
for lang in translations:
	source = 'inforevealer.d/'+str(lang)+'/categories.conf'
	dest = 'inforevealer.d/'+str(lang)
	files.append( (source,dest,conf_dir) )

# symlinks: source, destination
links = (('../share/inforevealer/src/inforevealer.py','bin/inforevealer'),)



def install(src, dst, prefix):
	"""Copy <src> to <dst>. The <src> path is relative to the source_dir and
	the <dst> path is a directory relative to the dir prefix.
	"""
	try:
		dst = os.path.join(prefix, dst, os.path.basename(src))
		src = os.path.join(source_dir, src)
		assert os.path.isfile(src)
		assert not os.path.isdir(dst)
		if not os.path.isdir(os.path.dirname(dst)):
			os.makedirs(os.path.dirname(dst))
		shutil.copy(src, dst)
		print('Installed %s' %dst)
	except Exception:
		print('Could not install %s' %dst)
		print('from %s' %src)
		
		
def uninstall(prefix, path):
	"""Remove the file or directory at <path>, which is relative to the 
	prefix.
	"""
	try:
		path = os.path.join(prefix, path)
		if os.path.isfile(path) or os.path.islink(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)
		else:
			return
		print('Removed %s' %path)
	except Exception:
		print('Could not remove %s' %path)
				

def make_link(src, link):
	try:
		link = os.path.join(install_dir, link)
		if os.path.isfile(link) or os.path.islink(link):
			os.remove(link)
		if not os.path.exists(os.path.dirname(link)):
			os.makedirs(os.path.dirname(link))
		os.symlink(src, link)
		print('Symlinked %s' %link)
	except:
		print('Could not create symlink %s' %link)


# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------
if args == ['install']:
	#    check_dependencies()
	print('Installing Inforevealer')
	if not os.access(install_dir, os.W_OK):
		print('You do not have write permissions to %s' %install_dir)
		sys.exit(1)
	for src, dst, prefix in files:
		install(src, dst, prefix)
	for lang in translations:
		install(os.path.join('po/', lang, 'inforevealer.mo'),
		    os.path.join('share/locale/', lang, 'LC_MESSAGES'),install_dir)
	for src, link in links:
		make_link(src, link)


# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------
elif args == ['uninstall']:
    print('Uninstalling Inforevealer from %s ...\n' %install_dir)
    uninstall(install_dir,'share/inforevealer')
    uninstall(install_dir,'share/man/man1/inforevealer.1')
    uninstall(install_dir,'share/applications/inforevealer.desktop')
    uninstall(install_dir,'share/icons/hicolor/scalable/apps/inforevealer.svg')
    for lang in translations:
        uninstall(install_dir,os.path.join('share/locale', lang, 'LC_MESSAGES/inforevealer.mo'))
    for _, link in links:
        uninstall(install_dir,link)
    print('Uninstalling Inforevealer from %s ...\n' %confdir)
    uninstall(conf_dir,'inforevealer.d')
else:
    info()
