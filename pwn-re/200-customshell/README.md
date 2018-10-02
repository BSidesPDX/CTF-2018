# pwn 200 - customshell

## Description

Asks for username and password, if both are correct, it launches a shell.  The username is hardcoded, however, the password is read from a file.  A strfmt vuln can be used to leak this password.

## Deploy

1. `gcc main.c -o secureshell`
2. Create `password.txt` file

## Challenge

Do you have what it takes to join pwnclub?

flag: BSidesPDX{ayy_lma0_my_5h3ll_i5_n0t_v3ry_s3cur3}
