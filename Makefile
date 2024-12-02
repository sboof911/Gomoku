# Variables
PYTHON = python
PYINSTALLER = pyinstaller
PIP = pip
NPM = npm
DIST_DIR = ..
BACKEND_ENV = backend/Gomoku-env
FRONTEND_DIST = render/dist
BACKEND_DIST = backend/render_dist
BACKEND_EXECUTABLE = Gomoku.exe
BACKEND_REQUIREMENTS = backend/requirements.txt
SERVER_SCRIPT = backend/server.py

ifeq ($(OS),Windows_NT)
    ACTIVATE = backend\Gomoku-env\Scripts\activate
	TOUCH = echo. >
else
    ACTIVATE = source $(BACKEND_ENV)/bin/activate
	TOUCH = touch
endif

# Targets
.PHONY: all build env install-backend build-backend install-frontend build-frontend install start clean fclean re

all: build

install: install-frontend install-backend

build: install build-frontend build-backend
	@echo Building frontend and backend completed

start: build
	./$(BACKEND_EXECUTABLE)

#################### BACKEND ####################

env: $(BACKEND_ENV)

$(BACKEND_ENV):
	@echo Creating virtual environment
	cd backend && if not exist Gomoku-env ($(PYTHON) -m venv Gomoku-env)
	$(ACTIVATE) && python.exe -m pip install --upgrade pip

install-backend: $(BACKEND_INSTALLED_MARKER)

$(BACKEND_INSTALLED_MARKER): $(BACKEND_ENV) $(BACKEND_REQUIREMENTS)
	@echo Installing backend dependencies
	$(ACTIVATE) && $(PIP) install -r $(BACKEND_REQUIREMENTS)
	$(TOUCH) $(BACKEND_INSTALLED_MARKER)

build-backend: $(BACKEND_EXECUTABLE)

$(BACKEND_EXECUTABLE): $(SERVER_SCRIPT) $(BACKEND_REQUIREMENTS)
	@echo Building backend
	$(ACTIVATE) && cd backend && $(PYINSTALLER) --onefile --distpath $(DIST_DIR) --name Gomoku --add-data "render_dist:render_dist" --add-data "./server.py:." --add-data "api:api" --add-data "srcs:srcs" --hidden-import=numpy server.py

#################### FRONTEND ####################

install-frontend: .installed-frontend

.installed-frontend: render/package.json
	@echo Installing frontend dependencies
	cd render && $(NPM) install
	$(TOUCH) .installed-frontend


build-frontend: $(BACKEND_DIST)

$(BACKEND_DIST): $(FRONTEND_DIST)
	@echo Copying dist folder to backend/render_dist
ifeq ($(OS),Windows_NT)
	xcopy /E /I /Y render\dist backend\render_dist
else
	cp -rf render/dist backend/render_dist
endif

$(FRONTEND_DIST): render/src/*
	@echo Building frontend
	cd render && $(NPM) run build

#################### UTILS ####################

clean:
ifeq ($(OS),Windows_NT)
	@echo Removing $(BACKEND_EXECUTABLE)
	del /Q /F $(BACKEND_EXECUTABLE)
	@echo Removing backend build
	del /Q /F backend\Gomoku.spec
	if exist backend\build rmdir /S /Q backend\build
	if exist $(BACKEND_DIST) rmdir /S /Q $(BACKEND_DIST)
	for /d /r ./backend %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@echo Removing frontend build
	if exist $(FRONTEND_DIST) rmdir /S /Q $(FRONTEND_DIST)
	del /Q /F .installed-backend .installed-frontend
else
	@echo Removing $(BACKEND_EXECUTABLE)
	rm -f $(BACKEND_EXECUTABLE)
	@echo Removing backend build
	rm -f backend/Gomoku.spec
	rm -rf backend/build
	rm -rf $(BACKEND_DIST)
	find backend -type d -name '__pycache__' -exec rm -r {} +
	@echo Removing frontend build
	rm -rf $(FRONTEND_DIST)
	rm -f .installed-backend .installed-frontend
endif

fclean: clean
ifeq ($(OS),Windows_NT)
	rmdir /S /Q $(BACKEND_ENV)
	rmdir /S /Q render\node_modules
else
	rm -rf $(BACKEND_ENV)
	rm -rf render/node_modules
endif

re: fclean build
