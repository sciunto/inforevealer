XGETTEXT=xgettext
MSGFMT=msgfmt
POA=po4a
POACONF=po4a.cfg
SRC=$(wildcard src/*.py)
XGETPOT='po/inforevealer.pot'
POAPOT='po/categories.conf.pot'
POFILES=$(wildcard po/*/inforevealer.po)
MOFILES=$(POFILES:.po=.mo)

.PHONY: all pot
all: mo

#TODO
#update po
#msgmerge -U .po .pot

#Create mo files 
mo: $(MOFILES)

#Create pot files
pot: $(POAPOT) $(XGETPOT) 


install: $(SRC)
		chmod +x setup.py
		python setup.py install --dir=/usr

uninstall:
		chmod +x setup.py
		python setup.py uninstall --dir=/usr

%.mo : %.po
		$(MSGFMT) $< -o $@

$(XGETPOT): $(SRC)
		$(XGETTEXT) -o $(XGETPOT) $(SRC)

$(POAPOT): $(SRC)
		$(POA) -k0 $(POACONF)



