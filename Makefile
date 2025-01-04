DC = docker compose
SERVICE_NAME = main-app
APP_FILE = docker_compose/app.yaml
STORAGE_FILE = docker_compose/storage.yaml
CACHE_FILE = docker_compose/cache.yaml
WEBSERVER_FILE = docker_compose/web_server.yaml
ENV = --env-file .env

# === API Section ===
.PHONY: app
app-start:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

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

.PHONY: storage-rebuild
storage-rebuild:
	${DC} -f ${STORAGE_FILE} build --no-cache

# === Cache Section ===
.PHONY: cache-start
cache-start:
	${DC} -f ${CACHE_FILE} up -d

.PHONY: cache-drop
cache-drop:
	${DC} -f ${CACHE_FILE} down

.PHONY: cache-remove
cache-rebuild:
	${DC} -f ${CACHE_FILE} build --no-cache

# === Web Server Section ===
.PHONY: webserver-start
webserver-start:
	${DC} -f ${WEBSERVER_FILE} up -d

.PHONY: webserver-drop
webserver-drop:
	${DC} -f ${WEBSERVER_FILE} down

.PHONY: webserver-remove
webserver-rebuild:
	${DC} -f ${WEBSERVER_FILE} build --no-cache

# === All Project ===
.PHONY: all
all:
	${DC} -f ${STORAGE_FILE} -f ${APP_FILE} -f ${CACHE_FILE} -f ${WEBSERVER_FILE} ${ENV} up --build -d

.PHONY: all-drop
all-drop:
	${DC} -f ${STORAGE_FILE} -f ${APP_FILE} -f ${CACHE_FILE}  ${WEBSERVER_FILE} down

.PHONY: all-remove
all-remove:
	${DC} -f ${STORAGE_FILE} -f ${APP_FILE} -f ${CACHE_FILE}  ${WEBSERVER_FILE} rm -f
