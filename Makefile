XGETTEXT=xgettext
MSGFMT=msgfmt
POA=po4a
POACONF=po4a.cfg
SRC=$(wildcard src/*.py)
XGETPOT='po/inforevealer.pot'
POAPOT='po/categories.conf.pot'
POFILES=$(wildcard po/*/*.po)
MOFILES=$(POFILES:.po=.mo)

.PHONY: all pot
all: mo

#Create mo files 
mo: $(MOFILES)

#Create pot files
pot: $(POAPOT) $(XGETPOT) 





%.mo : %.po
		$(MSGFMT) $< -o $@

$(XGETPOT): $(SRC)
		$(XGETTEXT) -o $(POT) $(SRC)

$(POAPOT): $(SRC)
		$(POA) -k0 $(POACONF)



