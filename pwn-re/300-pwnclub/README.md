# pwn 300 - pwnclub

## Description

The vulnerabilities are easy and straight forward, but all anti-exploit mitigations are enabled.  There is both a string format vuln and stack overflow vuln.  The string format vuln can be used to leak a libc address and stack canary.  With this information, a ret2libc exploit can be used with the stack overflow vuln.

Provide user with binary and `libc.so.6` from the container

## Deploy

1. `libc.so.6` will need to be distributed with the binary (`docker cp <containerId>:/lib/x86_64-linux-gnu/libc-2.27.so ./`)

## Challenge

Do you have what it takes to join pwnclub?

flag: BSidesPDX{w3lc0m3___70_7h3_pWn__club!}
