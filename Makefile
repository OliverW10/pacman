main: src/evaluate.c
	gcc src/evaluate.c -shared -o src/evaluate.so
# fPIC makes it do position independant code, idk if this is needed but i sa