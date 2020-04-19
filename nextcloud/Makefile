SHELL := /bin/bash

help: ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

pull: ## Pull service images
	docker-compose pull

up: ## Start containers in the background and display logs
	docker-compose up -d
	$(MAKE) logs

stop: ## Stop containers
	docker-compose stop

restart: ## Restart containers by stop&start and display logs
	$(MAKE) stop
	$(MAKE) up
	$(MAKE) logs

logs: ## Display container logs
	docker-compose logs --tail=500 --follow
