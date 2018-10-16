# pwn 200 - customshell

## Description

Asks for username and password, if both are correct, it launches a shell.  The username is hardcoded, however, the password is read from a file.  A strfmt vuln can be used to leak this password.

Provide user with binary

## Deploy

1. Create `password.txt` file

## Challenge

I made my own shell, it's very secure.

flag: BSidesPDX{ayy_lma0_my_5h3ll_i5_n0t_v3ry_s3cur3}
