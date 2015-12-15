PY?=python
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
GITHUB_PAGES_BRANCH=gh-pages

help:
	@echo 'Makefile for a Authentiq Examples site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make devserver [PORT=8000]          start/restart develop_server.sh    '
	@echo '   make stopserver                     stop local server                  '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '

devserver:
ifdef PORT
	$(BASEDIR)/develop_server.sh restart $(PORT)
else
	$(BASEDIR)/develop_server.sh restart
endif

stopserver:
	$(BASEDIR)/develop_server.sh stop
	@echo 'Stopped BrowserSync process running in background.'

gh_pages:
	ghp-import -m "Generate Authentiq Examples site" -b $(GITHUB_PAGES_BRANCH) $(BASEDIR)
	git push origin $(GITHUB_PAGES_BRANCH)
