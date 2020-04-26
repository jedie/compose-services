include .env

VARS:=$(shell sed -ne 's/ *\#.*$$//; /./ s/=.*$$// p' .env )
$(foreach v,$(VARS),$(eval $(shell echo export $(v)="$($(v))")))

SHELL := /bin/bash
MAX_LINE_LENGTH := 119
POETRY_VERSION := $(shell poetry --version 2>/dev/null)


help: ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo "Found ${POETRY_VERSION}, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry: ## install or update poetry
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo 'Update poetry v$(POETRY_VERSION)' ; \
		poetry self update ; \
	else \
		echo 'Install poetry' ; \
		pip3 install --user -U poetry ; \
	fi

install: check-poetry ## install via poetry
	poetry install

nodes: check-poetry ## BundleWrap - List nodes
	poetry run bw nodes

nextcloud-uptime: ## Just start "uptime" on nextcloud node (for connection test)
	poetry run bw -a run nextcloud "uptime"

nextcloud-apply: ## Setup "nextcloud" node via bundlewrap
	poetry run bw apply nextcloud

nextcloud-apply-debug: ## Setup "nextcloud" node via bundlewrap (with debug output)
	poetry run bw --debug apply nextcloud

nextcloud-pull: ## Pull nextcloud images
	ssh nextcloud 'docker-compose pull'

nextcloud-up: ## Start nextcloud containers
	ssh nextcloud 'docker-compose up -d'
	$(MAKE) nextcloud-logs

nextcloud-admin-password: ## Display default nextcloud "admin" user password
	@poetry run bw debug -c "print('_'*70);print('admin password is:');print(repo.vault.human_password_for('nextcloud admin'));print('-'*70)"

nextcloud-update: ## Update nextcloud node
	ssh nextcloud 'apt update && apt -y dist-upgrade'
	$(MAKE) nextcloud-pull
	$(MAKE) nextcloud-stop
	$(MAKE) nextcloud-up

nextcloud-logs: ## Display nextcloud docker logs
	ssh nextcloud 'docker-compose logs --follow --tail="500"'

nextcloud-stop: ## Stop nextcloud containers
	ssh nextcloud 'docker-compose stop'

nextcloud-cleanup-journald: ## Cleanup nextcloud journald disk space usage
	# display disk usage:
	ssh nextcloud 'sudo journalctl --disk-usage'
	ssh nextcloud 'sudo du -h /var/log/'

	# Status of journald:
	ssh nextcloud 'systemctl status systemd-journald'

	# Delete old journald entries:
	ssh nextcloud 'sudo journalctl --vacuum-size=1G'
	ssh nextcloud 'sudo journalctl --vacuum-time=1years'

nextcloud-cleanup-docker: ## Cleanup nextcloud docker images
	# Remove unused containers, networks, images:
	ssh nextcloud 'docker system prune --force --all --filter until=48h'

nextcloud-delete-all-data: ## DELETE all nextcloud data!
	$(MAKE) nextcloud-stop
	ssh nextcloud 'docker system prune --force --all'
	ssh nextcloud 'sudo rm -Rf docker-volumes'