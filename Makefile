DC = docker compose
SERVICE_NAME = main-app
APP_FILE = docker_compose/app.yaml
STORAGE_FILE = docker_compose/storage.yaml
REDIS_FILE = docker_compose/redis.yaml

.PHONY: app
app-start:
	${DC} -f ${APP_FILE} up -d

.PHONY: app-drop
app-drop:
	${DC} -f ${APP_FILE} down

.PHONY: app-remove
app-rebuild:
	${DC} -f ${APP_FILE} build --no-cache

.PHONY: app-remove
app-remove:
	${DC} -f ${APP_FILE} down
	${DC} -f ${APP_FILE} rm -f ${SERVICE_NAME}

.PHONY: logs
app-logs:
	${DC} -f ${APP_FILE} logs -f

.PHONY: shell
shell:
	${DC} -f ${APP_FILE} exec ${SERVICE_NAME} /bin/sh

# === Storage Section ===
.PHONY: storage
storage-start:
	${DC} -f ${STORAGE_FILE} up -d

.PHONY: storage-drop
storage-drop:
	${DC} -f ${STORAGE_FILE} down

.PHONY: storage-remove
storage-rebuild:
	${DC} -f ${STORAGE_FILE} build --no-cache

# === Redis Section ===
.PHONY: redis-start
redis-start:
	${DC} -f ${REDIS_FILE} up -d

.PHONY: redis-drop
redis-drop:
	${DC} -f ${REDIS_FILE} down

.PHONY: redis-remove
redis-rebuild:
	${DC} -f ${REDIS_FILE} build --no-cache
