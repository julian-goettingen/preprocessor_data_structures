all:
	make prepare
	make compile

clean:
	rm -f ppds_interface_desc/*
	rm -f ppds_target_headers/*
	rm -f lib.so

prepare:
	python3 ./../../../script.py

compile:
	clang c_src/functions.c -shared -fPIC -o lib.so -Ippds_target_headers -I../../../ppds_source_headers

#output is an .so - cant run it.
#run:
#	./a.out

