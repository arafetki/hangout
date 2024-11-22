## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m

## Help
help:
	@printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	@printf " make [target]\n\n"
	@printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	@awk '/^[a-zA-Z\-0-9\.@]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf " ${COLOR_INFO}%-16s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

.PHONY: start-dev
## Starts the API in development mode with auto-reload
start-dev:
	PYTHONPATH=./app uvicorn app.main:app --reload --host 0.0.0.0 --port $(HTTP_PORT) --loop asyncio


.PHONY: migration/new
## Add a new database migration
migration/new:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

.PHONY: migration/up
## apply all database migrations
migration/up:
	alembic upgrade head

.PHONY: migration/down
## apply all down database migrations
migration/down:
	alembic downgrade base