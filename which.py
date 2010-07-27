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
			
