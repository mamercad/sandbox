.PHONY: requirements
requirements:
	poetry export --without-hashes --format=requirements.txt | tee requirements.txt
	poetry export --without-hashes --format=requirements.txt | tee docker/requirements.txt

.PHONY: install-vagrant

UNAME := $(shell uname | tr '[:upper:]' '[:lower:]')
VAGRANT_VERSION = 2.3.4

VAGRANT = $(shell command -v vagrant 2>/dev/null)
install-vagrant:
ifeq (,$(VAGRANT))
	@{ \
		case $(UNAME) in \
			darwin) \
				curl -fsSLo tmp/vagrant.dmg 'https://releases.hashicorp.com/vagrant/$(VAGRANT_VERSION)/vagrant_$(VAGRANT_VERSION)_$(UNAME)_amd64.dmg'; \
				hdiutil attach tmp/vagrant.dmg; \
				sudo installer -pkg /Volumes/Vagrant/vagrant.pkg -target /; \
				hdiutil detach /dev/disk2s1; \
				;; \
		esac \
	}
	VAGRANT = $(shell command -v vagrant 2>/dev/null)
endif
