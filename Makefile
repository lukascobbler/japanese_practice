PC=pyinstaller
PI=python3
PC_ARGS=--onefile --windowed

REQS=requirements.txt
VENV_LINUX=jp_linux_venv

COMPRESS=zip
COMPRESS_ARGS=-r
FINAL_FILENAME=japanese_practice.$(COMPRESS)

INSTALL_DEST_NAME="Japanese Practice"

all: deps compress

help:
	@echo "You may decide to make a custom venv for building the application. The easiest way is to run" \
	"\"make venv\" and to source the displayed activation script path. Running \"make all\" installs all of the" \
	"required dependencies and builds the project to a zip file which can be redistributed further."

run:
	cd ./src/ && $(PI) main.py

deps:
	pip install -r $(REQS)

venv:
	$(PI) -m venv ./$(VENV_LINUX)/
	@echo "To use the new venv use \"source ./$(VENV_LINUX)/bin/activate\""

compile:
	rm -rf ./dist/
	$(PC) $(PC_ARGS) ./src/main.py -n "japanese_practice"

runnable: compile
	rm -rf ./$(INSTALL_DEST_NAME)/
	mkdir ./$(INSTALL_DEST_NAME)/
	cp ./dist/japanese_practice ./$(INSTALL_DEST_NAME)/
	cp ./src/*.ui ./$(INSTALL_DEST_NAME)/
	cp ./src/icon.png ./$(INSTALL_DEST_NAME)/

compress: runnable
	$(COMPRESS) $(COMPRESS_ARGS) $(FINAL_FILENAME) ./$(INSTALL_DEST_NAME)/

clean:
	rm -rf ./$(INSTALL_DEST_NAME)/
	rm -rf ./dist/
	rm -rf $(FINAL_FILENAME)

mr-proper: clean
	rm -rf ./build/
	rm -rf ./src/__pycache__/
	rm -rf ./$(VENV_LINUX)/
	rm -rf *.spec