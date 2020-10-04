# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
# SPHINXOPTS    =
SPHINXOPTS    = -c "./"
# SPHINXBUILD   = sphinx-build
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = climate
SOURCEDIR     = .
BUILDDIR      = _build
BUILDWEBSITE  = _build/website
BUILDCOVERAGE = _build/coverage
BUILDPDF      = _build/pdf
PORT          = 8888
FILES         = 


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# from jupinx example
website:
ifneq ($(strip $(parallel)),)
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDWEBSITE)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_make_site=1 -D jupyter_generate_html=1 -D jupyter_download_nb=1 -D jupyter_execute_notebooks=1 -D jupyter_target_html=1 -D jupyter_images_markdown=0 -D jupyter_html_template="html.tpl" -D jupyter_coverage_dir=$(BUILDCOVERAGE) -D jupyter_number_workers=$(parallel)
else
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDWEBSITE)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_make_site=1 -D jupyter_generate_html=1 -D jupyter_download_nb=1 -D jupyter_execute_notebooks=1 -D jupyter_target_html=1 -D jupyter_images_markdown=0 -D jupyter_html_template="html.tpl" -D jupyter_coverage_dir=$(BUILDCOVERAGE)
endif