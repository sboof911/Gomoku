# Variables
PYTHON = python
PYINSTALLER = pyinstaller
PIP = pip
NPM = npm
DIST_DIR = ..

build: build-frontend build-backend
	@echo Building frontend and backend complited

env:
	@echo Creating virtual environment
	cd backend && if not exist Gomoku-env ($(PYTHON) -m venv Gomoku-env)
	backend\Gomoku-env\Scripts\activate
	python.exe -m pip install --upgrade pip

build-backend: env
	@echo Installing backend dependencies
	$(PIP) install -r backend/requirements.txt
	cd backend && $(PYINSTALLER) --onefile --distpath $(DIST_DIR) --name Gomoku --add-data "render_dist:render_dist" --add-data "./server.py:." --add-data "api:api" --add-data "srcs:srcs" --hidden-import=numpy server.py

build-frontend:
	@echo Installing frontend dependencies
	cd render && $(NPM) install
	cd render && $(NPM) run build
	@echo Copying dist folder to backend/render_dist
ifeq ($(OS),Windows_NT)
	xcopy /E /I /Y render\dist backend\render_dist
else
	cp -rf render/dist backend/render_dist
endif

start: build
	./Gomoku.exe

clean:
ifeq ($(OS),Windows_NT)
	@echo removing Gomoku.exe
	del /Q /F Gomoku.exe
	@echo removing backend build
	del /Q /F backend\Gomoku.spec
	if exist backend\build rmdir /S /Q backend\build
	if exist backend\render_dist rmdir /S /Q backend\render_dist
	for /d /r ./backend %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@echo removing frontend build
	if exist render\dist rmdir /S /Q render\dist

else
	@echo removing Gomoku.exe
	rm -f Gomoku.exe
	@echo removing backend build
	rm -f backend/Gomoku.spec
	rm -rf backend/build
	rm -rf backend/render_dist
	find backend -type d -name '__pycache__' -exec rm -r {} +
	@echo removing frontend build
	rm -rf render/dist
endif

fclean: clean
ifeq ($(OS),Windows_NT)
	rmdir /S /Q backend\Gomoku-env
	rmdir /S /Q render\node_modules
else
	rm -rf backend/Gomoku-env
	rm -rf render/node_modules
endif

re: fclean build
