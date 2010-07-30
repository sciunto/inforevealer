# -*- coding: utf-8 -*-

import sys, os, os.path
# this function partially comes from a bug report
# see http://bugs.python.org/issue444582
def which(file, mode=os.X_OK, path=None,pathext=None):

  filepath, file = os.path.split(file)

  if filepath:
      path = (filepath,)
  elif path is None:
      path = os.environ.get('PATH', os.defpath).split(os.pathsep)
  elif isinstance(path, basestring):
      path = path.split(os.pathsep)

  if pathext is None:
      pathext = ['']
  elif isinstance(pathext, basestring):
      pathext = pathext.split(os.pathsep)

  if not '' in pathext:
      pathext.insert(0, '') # always check command without extension, even for an explicitly passed pathext

  seen = set()


  for dir in path:
	if dir: # only non-empty directories are searched
	    id = os.path.normcase(os.path.abspath(dir))
	    if not id in seen: # each directory is searched only once
		seen.add(id)
		woex = os.path.join(dir, file)
		for ext in pathext:
		    name = woex + ext
		    if os.path.exists(name) and os.access(name, mode):
			return name



def findPath(executable):
	if which(executable) != None:
		return which(executable)
	else:
		my_path=['/bin','/usr/bin','/sbin','/usr/sbin'] #this should be a common path for our usage
		for p in my_path:
			exec_test=p+'/'+executable
			print "test"
			print exec_test
			if os.access(exec_test,os.F_OK):
				return exec_test
		return None			
