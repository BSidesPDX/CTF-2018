target: pwn

pwn:
	make -C ./pwn-re/200-secureshell/src
	make -C ./pwn-re/300-pwnclub/src

clean:
	make -C ./pwn-re/200-secureshell/src clean
	make -C ./pwn-re/300-pwnclub/src clean
