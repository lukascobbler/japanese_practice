REQS=requirements.txt
PC=pyinstaller
PC_ARGS=--onefile --windowed

COMPRESS=zip
COMPRESS_ARGS=-r
FINAL_FILENAME=japanese_practice.$(COMPRESS)

deps:
	while read -r req; do \
	pip install "$$req"; \
	done < $(REQS)

compile:
	rm -rf ./dist/
	$(PC) $(PC_ARGS) ./src/main.py -n "japanese_practice"

runnable: compile
	rm -rf ./runnable/
	mkdir ./runnable/
	cp ./dist/japanese_practice ./runnable/
	cp ./src/*.ui ./runnable/
	cp ./src/icon.png ./runnable/

compress: runnable
	$(COMPRESS) $(COMPRESS_ARGS) $(FINAL_FILENAME) ./runnable/

clean:
	rm -rf ./runnable/
	rm -rf ./dist/
	rm -rf $(FINAL_FILENAME)

mr-proper: clean
	rm -rf ./build/
	rm -rf *.spec