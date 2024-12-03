# Variables
PYTHON = python
PYINSTALLER = pyinstaller
PIP = pip
NPM = npm
DIST_DIR = ..
ACTIVATE = source backend/Gomoku-env/bin/activate

# Targets
.PHONY: all build env install-backend build-backend install-frontend build-frontend install start clean fclean re

all: build

install: install-frontend install-backend

build: install build-frontend build-backend
	@echo Building frontend and backend complited

start: build
	./Gomoku.exe


#################### BACK END ####################

env:
	@echo Creating virtual environment
	cd backend && [ ! -d Gomoku-env ] && $(PYTHON) -m venv Gomoku-env || true
	$(ACTIVATE) && $(PYTHON) -m pip install --upgrade pip

install-backend: env
	@echo Installing backend dependencies
	$(ACTIVATE) && $(PIP) install -r backend/requirements.txt

build-backend:
	@echo Building backend
	$(ACTIVATE) && cd backend && $(PYINSTALLER) --onefile --distpath $(DIST_DIR) --name Gomoku --add-data "render_dist:render_dist" --add-data "./server.py:." --add-data "api:api" --add-data "srcs:srcs" --hidden-import=numpy server.py


#################### FRONT END ####################

install-frontend:
	@echo Installing frontend dependencies
	cd render && $(NPM) install


build-frontend:
	@echo Building frontend
	cd render && $(NPM) run build
	@echo Copying dist folder to backend/render_dist
	cp -rf render/dist backend/render_dist

#################### UTILS ####################

clean:
	@echo removing Gomoku.exe
	rm -f Gomoku.exe
	@echo removing backend build
	rm -f backend/Gomoku.spec
	rm -rf backend/build
	rm -rf backend/render_dist
	find backend -type d -name '__pycache__' -exec rm -r {} +
	@echo removing frontend build
	rm -rf render/dist

fclean: clean
	rm -rf backend/Gomoku-env
	rm -rf render/node_modules


re: fclean build