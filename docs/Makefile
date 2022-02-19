# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = opengnm
SOURCEDIR     = .
BUILDDIR      = _build


.PHONY: help builddir html builddir_es pots pots_to_pos html_es clean clean_es

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  clean     to clean the directory starting a new compilation from scratch"

builddir:
	mkdir -p $(BUILDDIR)

html: builddir
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

clean:
	rm -rf $(BUILDDIR)
	rm -rf autosummary/*.rst

