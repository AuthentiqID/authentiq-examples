BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output

GITHUB_PAGES_BRANCH=gh-pages

help:
	@echo 'Makefile for a Authentiq Examples site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make devserver [PORT=8000]          start/restart develop_server.sh    '
	@echo '   make stopserver                     stop local server                  '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '

html: clean
	rsync -a --exclude='.*' --exclude='Makefile' --exclude='develop_server.sh' $(BASEDIR)/ $(OUTPUTDIR)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

devserver:
ifdef PORT
	$(BASEDIR)/develop_server.sh restart $(PORT)
else
	$(BASEDIR)/develop_server.sh restart
endif

stopserver:
	$(BASEDIR)/develop_server.sh stop
	@echo 'Stopped BrowserSync process running in background.'

gh_pages: html
	ghp-import -m "Generate Authentiq Examples site" -b $(GITHUB_PAGES_BRANCH) $(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)
