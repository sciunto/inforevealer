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

#TODO 
#translations categories.conf
# uninstall

import os
import sys
import shutil
import getopt

source_dir = os.path.dirname(os.path.realpath(__file__))
install_dir = '/usr/local/'

translations = ('fr')

# files: source, destination
files = (
		('src/action.py', 'share/inforevealer/src'),  
		('src/getinfo.py', 'share/inforevealer/src'),   
		('src/gui.py',  'share/inforevealer/src'),  
		('src/inforevealer.py',  'share/inforevealer/src'),  
		('src/io.py',  'share/inforevealer/src'),  
		('src/pastebin.py',  'share/inforevealer/src'),  
		('src/readconf.py', 'share/inforevealer/src'),
		('icons/icon.svg', 'share/inforevealer/icons'),
		('inforevealer.d/categories.conf','/etc/inforevealer.d'),
		('inforevealer.d/validator.conf','/etc/inforevealer.d'),
		('inforevealer.d/validator.conf','/etc/inforevealer.d'),
		('inforevealer.d/pastebin/fpaste.org.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/paste2.org.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/pastebin.ca.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/pastebin.com.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/paste.debian.net.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/paste.ubuntu.com.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/pastie.org.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/slexy.org.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/stikked.com.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer.d/pastebin/yourpaste.net.conf','/etc/inforevealer.d/pastebin'),
		('inforevealer;desktop','share/man/'),
		('man/inforevealer.1','share/applications/')
		)

# symlinks: source, destination
links = (('../share/inforevealer/src/inforevealer.py','bin/inforevealer'),)


def info():
	print(__doc__)
	sys.exit(1)

def install(src, dst):
	"""Copy <src> to <dst>. The <src> path is relative to the source_dir and
	the <dst> path is a directory relative to the install_dir.
	"""
	try:
		dst = os.path.join(install_dir, dst, os.path.basename(src))
		src = os.path.join(source_dir, src)
		assert os.path.isfile(src)
		assert not os.path.isdir(dst)
		if not os.path.isdir(os.path.dirname(dst)):
			os.makedirs(os.path.dirname(dst))
		shutil.copy(src, dst)
		print('Installed', dst)
	except Exception:
		print('Could not install', dst)
		
		
def uninstall(path):
	"""Remove the file or directory at <path>, which is relative to the 
	install_dir.
	"""
	try:
		path = os.path.join(install_dir, path)
		if os.path.isfile(path) or os.path.islink(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)
		else:
			return
		print 'Removed', path
	except Exception:
		print 'Could not remove', path
				

def make_link(src, link):
	try:
		link = os.path.join(install_dir, link)
		if os.path.isfile(link) or os.path.islink(link):
			os.remove(link)
		if not os.path.exists(os.path.dirname(link)):
			os.makedirs(os.path.dirname(link))
		os.symlink(src, link)
		print 'Symlinked', link
	except:
		print 'Could not create symlink', link

# ---------------------------------------------------------------------------
# Parse the command line.
# ---------------------------------------------------------------------------
try:
	opts, args = getopt.gnu_getopt(sys.argv[1:], '', ['dir=', 'no-mime'])
except getopt.GetoptError:
	info()
for opt, value in opts:
	if opt == '--dir':
		install_dir = value
		if not os.path.isdir(install_dir):
			print '\n!!! Error:', install_dir, 'does not exist.' 
			info()

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------
if args == ['install']:
	#    check_dependencies()
	print 'Installing Inforevealer to', install_dir, '...\n'
	if not os.access(install_dir, os.W_OK):
		print 'You do not have write permissions to', install_dir
		sys.exit(1)
	for src, dst in files:
		install(src, dst)
	for lang in translations:
		pass
		install(os.path.join('po', lang, 'LC_MESSAGES/inforevealer.mo'),
		    os.path.join('share/locale/', lang, 'LC_MESSAGES'))
	for src, link in links:
		make_link(src, link)
	#os.utime(os.path.join(install_dir, 'share/icons/hicolor'), None)


# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------
elif args == ['uninstall']:
    print 'Uninstalling Inforevealer from', install_dir, '...\n'
    uninstall('share/inforevealer')
    uninstall('share/man/man1/inforevealer.1')
    uninstall('share/applications/inforevealer.desktop')
	#TODO /etc...
    #uninstall('share/icons/hicolor/16x16/apps/comix.png')
    #uninstall('share/icons/hicolor/22x22/apps/comix.png')
    #uninstall('share/icons/hicolor/24x24/apps/comix.png')
    #uninstall('share/icons/hicolor/32x32/apps/comix.png')
    #uninstall('share/icons/hicolor/48x48/apps/comix.png')
    #uninstall('share/icons/hicolor/scalable/apps/comix.svg')
    for _, link in links:
        uninstall(link)
    for lang in translations:
        uninstall(os.path.join('share/locale', lang, 'LC_MESSAGES/inforevealer.mo'))
    
else:
    info()
