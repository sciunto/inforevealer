#!/usr/bin/python
# -*- coding: utf-8 -*-
# Written by Stephane Graber <stgraber@stgraber.org>
#            Daniel Bartlett <dan@f-box.org>
# Last modification : Mon Jan 28 22:33:23 CET 2008

# Modified by Francois Boulogne <fboulogne at april dot org>
# for inforevealer

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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import urllib, os, sys, re, gettext
from gettext import gettext as _
import configobj

gettext.textdomain("pastebinit")

defaultPB = "http://pastebin.com" #Default pastebin
__version__="0.5.1"


class pasteURLopener(urllib.FancyURLopener):
    """Custom urlopener to handle 401's"""
    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
	return None

def preloadPastebins():
    """Check several places for config files:
     - global config in /etc/inforevealer.d/pastebin
     - for source checkout, config in the checkout
     - user's overrides in ~/.inforevealer.d/pastebin
    Files found later override files found earlier."""
    for confdir in ['/etc/inforevealer.d/pastebin',
		    os.path.join(os.path.dirname(__file__), '../inforevealer.d/pastebin'),
		    os.path.expanduser('~/.inforevealer.d/pastebin')]:
	try:
	    confdirlist = os.listdir(confdir)
	except OSError:
	    continue
	pastebind = {}
	for fileitem in confdirlist:
	    if fileitem.startswith('.'):
		continue
	    filename = os.path.join(confdir, fileitem)
	    try:
		bininstance = configobj.ConfigObj(filename)
	    except configobj.ConfigObjError, e:
		print >> sys.stderr, '%s: %s' % (filename, e)
		continue
	    try:
		section = bininstance['pastebin']
	    except KeyError:
		print >> sys.stderr, _('%s: no section [pastebin]') % filename
		continue
	    try:
		basename = section['basename']
	    except KeyError:
		print >> sys.stderr, _("%s: no 'basename' in [pastebin]") % filename
		continue
	    pastebind[basename] = bininstance
	return pastebind


def doParentFixup(website, paramname, parentid):
	"""pastey.net obfuscates parent ids for replies.  Rather than taking the
	post ID given as the parent ID, we must handle this by going to that
	post page and looking up what the invisible parent ID field will be
	set to for children."""
	if parentid == "":
		return ""
	url_opener = pasteURLopener()
	page = url_opener.open(website + '/' + parentid, None)
	matches = re.split('<input.*?name="' + paramname + '".*?value="(.*?)"', page.read())
	if len(matches) <= 1 or re.match(parentid, matches[1]) == None:
		# The obfuscated version didn't begin with the partial version,
		# or unable to find the obfuscated version for some reason!
		# Create a paste with no parent (should we throw, instead?)
		return ""
	return matches[1]


def getParameters(website, pastebind, content, user, jabberid, version, format, parentpid, permatag, title, username, password):
    "Return the parameters array for the selected pastebin"
    params = {}
    for pastebin in pastebind:
	if re.search(pastebind[pastebin]['pastebin']['regexp'], website):
	    for param in pastebind[pastebin]['format'].keys():
		paramname = pastebind[pastebin]['format'][param]
		if param == 'user':
		    params[paramname] = user
		elif param == 'content':
		    params[paramname] = content
		elif param == 'title':
		    params[paramname] = title
		elif param == 'version':
		    params[paramname] = version
		elif param == 'format':
		    params[paramname] = format
		elif param == 'parentpid':
		    params[paramname] = doParentFixup(website, paramname, parentpid)
		elif param == 'permatag':
		    params[paramname] = permatag
		elif param == 'username':
		    params[paramname] = username
		elif param == 'password':
		    params[paramname] = password
		elif param == 'jabberid':
		    params[paramname] = jabberid
		else:
		    params[paramname] = pastebind[pastebin]['defaults'][param]
    if params:
	return params
    else:
	sys.exit(_("Unknown website, please post a bugreport to request this pastebin to be added (%s)") % website)

#XML Handling methods
def getText(nodelist):
    rc = ""
    for node in nodelist:
	if node.nodeType == node.TEXT_NODE:
	    rc = rc + node.data
    return rc.encode('utf-8')

def getNodes(nodes, title):
    return nodes.getElementsByTagName(title)

def getFirstNode(nodes, title):
    return getNodes(nodes, title)[0]

def getFirstNodeText(nodes, title):
    return getText(getFirstNode(nodes, title).childNodes)
    
    
def sendFileContent(filepath,title,website,version):
	"""Send filepath on pastebin,
	    print link on stdout
	    return the link"""
	user = os.environ.get('USER')
	jabberid = ""
	permatag = ""
	format = "text"
	username = ""
	password = ""
	filename = ""
	content = ""
	parentpid = ""
	
	#read dumpfile content	
	dumpfile_handler= open(filepath,'r')
	content = dumpfile_handler.read()
	dumpfile_handler.close()
	
	pastebind = preloadPastebins() #get the config from /etc/pastebin.d/
	params = getParameters(website, pastebind, content, user, jabberid, version, format, parentpid, permatag, title, username, password) #Get the parameters array
	
	
	reLink = None
	tmp_page = ""
	if "page" in params:
		website += params['page']
		tmp_page = params['page']
		del params["page"]
	if "regexp" in params:
		reLink = params['regexp']
		del params["regexp"]
	params = urllib.urlencode(params) #Convert to a format usable with the HTML POST
			
	url_opener = pasteURLopener()
	page = url_opener.open(website, params) #Send the informations and be redirected to the final page
			
	try:
		if reLink: #Check if we have to apply a regexp
			website = website.replace(tmp_page, "")
			if reLink == '(.*)':
				pastelink =  page.read().strip()
			else:
				pastelink = website + re.split(reLink, page.read())[1] #Print the result of the Regexp
		else:
			pastelink = page.url #Get the final page and show the url
		print(_("Pastebin link: ")+pastelink+"\n")
		return pastelink
	except KeyboardInterrupt:
		sys.exit(_("KeyboardInterrupt caught."))
	except:
		raise
		sys.exit(_("Unable to read or parse the result page, it could be a server timeout or a change server side, try with another pastebin."))
							

