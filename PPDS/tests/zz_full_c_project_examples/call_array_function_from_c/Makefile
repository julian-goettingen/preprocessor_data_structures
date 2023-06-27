

all:
	make prepare
	make compile

clean:
	rm -f ppds_interface_desc/*
	rm -f ppds_target_headers/*
	rm -f ./a.out

prepare:
	python3 ./../../../script.py

compile:
	${CC} main.c -Ippds_target_headers -I../../../ppds_source_headers

run:
	./a.out

