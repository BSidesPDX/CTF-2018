# re 100 - goxor solution

goxor is a 64bit golang binary

```
> file goxor
goxor: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```

You can tell it is a golang binary as it is not stripped and contains a plethora og golang statically linked libraries in it. One of these is `main.main`, which showcases a golang binary.

```
readelf -s goxor | grep main.main
  3103: 00000000004833f0   197 FUNC    GLOBAL DEFAULT    1 main.main
```

Because golang is so verbose, finding the relevant information for this challenge is relatively straight forward (this is a 100 level, afterall).

Establishing a `gdb` session with `goxor` will show several function names. Looking at the output of `info functions` we see the three following functions

Note: I am using [peda-gdb](https://github.com/longld/peda)

```
gdb-peda$ info functions

[BREAK]

0x0000000000483210  main.goxor
0x00000000004833f0  main.main
0x00000000004834c0  main.init
```

We now know we have a `main.main` and a `main.goxor` function. If we look at the main.goxor function in gdb we can see that the code has some interesting flows. To get to that code path, I am going to set a breakpoint at 0x0000000000483210 and then examine the instructions of the function

```
gdb-peda$ break * 0x0000000000483210                                                                                      
Breakpoint 1 at 0x483210

gdb-peda$ r "test string"

gdb-peda$ x/70i $rip                                                                                                                                                                                                
=> 0x483210 <main.goxor>:       mov    rcx,QWORD PTR fs:0xfffffffffffffff8
   0x483219 <main.goxor+9>:     lea    rax,[rsp-0x18]
   0x48321e <main.goxor+14>:    cmp    rax,QWORD PTR [rcx+0x10]
   0x483222 <main.goxor+18>:    jbe    0x4833e5 <main.goxor+469>
   0x483228 <main.goxor+24>:    sub    rsp,0x98
   0x48322f <main.goxor+31>:    mov    QWORD PTR [rsp+0x90],rbp
   0x483237 <main.goxor+39>:    lea    rbp,[rsp+0x90]
   0x48323f <main.goxor+47>:    mov    rax,QWORD PTR [rip+0x41c9a]        # 0x4c4ee0 <main.statictmp_0>
   0x483246 <main.goxor+54>:    mov    QWORD PTR [rsp+0x49],rax
   0x48324b <main.goxor+59>:    lea    rdi,[rsp+0x50]
   0x483250 <main.goxor+64>:    lea    rsi,[rip+0x41c90]        # 0x4c4ee7 <main.statictmp_0+7>
   0x483257 <main.goxor+71>:    mov    QWORD PTR [rsp-0x10],rbp
   0x48325c <main.goxor+76>:    lea    rbp,[rsp-0x10]
   0x483261 <main.goxor+81>:    call   0x44fba4 <runtime.duffcopy+868>
   0x483266 <main.goxor+86>:    mov    rbp,QWORD PTR [rbp+0x0]
   0x48326a <main.goxor+90>:    xor    eax,eax
   0x48326c <main.goxor+92>:    mov    rcx,rax
   0x48326f <main.goxor+95>:    mov    rdx,QWORD PTR [rsp+0xa8]
   0x483277 <main.goxor+103>:   cmp    rax,rdx
   0x48327a <main.goxor+106>:   jge    0x483319 <main.goxor+265>
   0x483280 <main.goxor+112>:   mov    QWORD PTR [rsp+0x38],rcx
   0x483285 <main.goxor+117>:   mov    rbx,QWORD PTR [rsp+0xa0]
   0x48328d <main.goxor+125>:   movzx  esi,BYTE PTR [rbx+rax*1]
   0x483291 <main.goxor+129>:   cmp    esi,0x80
   0x483297 <main.goxor+135>:   jge    0x4832e6 <main.goxor+214>
   0x483299 <main.goxor+137>:   inc    rax
   0x48329c <main.goxor+140>:   cmp    rcx,0x27
   0x4832a0 <main.goxor+144>:   jae    0x4833de <main.goxor+462>
   0x4832a6 <main.goxor+150>:   xor    esi,0x7f
   0x4832a9 <main.goxor+153>:   movzx  edi,BYTE PTR [rsp+rcx*1+0x49]
   0x4832ae <main.goxor+158>:   cmp    sil,dil
   0x4832b1 <main.goxor+161>:   jne    0x4832b8 <main.goxor+168>
   0x4832b3 <main.goxor+163>:   inc    rcx
   0x4832b6 <main.goxor+166>:   jmp    0x48326f <main.goxor+95>
   0x4832b8 <main.goxor+168>:   mov    QWORD PTR [rsp+0x40],rax
   0x4832bd <main.goxor+173>:   mov    QWORD PTR [rsp],0xffffffffffffffff
   0x4832c5 <main.goxor+181>:   call   0x45b0a0 <os.Exit>
   0x4832ca <main.goxor+186>:   mov    rax,QWORD PTR [rsp+0x40]
   0x4832cf <main.goxor+191>:   mov    rdx,QWORD PTR [rsp+0xa8]
   0x4832d7 <main.goxor+199>:   mov    rbx,QWORD PTR [rsp+0xa0]
   0x4832df <main.goxor+207>:   mov    rcx,QWORD PTR [rsp+0x38]
   0x4832e4 <main.goxor+212>:   jmp    0x48326f <main.goxor+95>
   0x4832e6 <main.goxor+214>:   mov    QWORD PTR [rsp],rbx
   0x4832ea <main.goxor+218>:   mov    QWORD PTR [rsp+0x8],rdx
   0x4832ef <main.goxor+223>:   mov    QWORD PTR [rsp+0x10],rax
   0x4832f4 <main.goxor+228>:   call   0x449530 <runtime.decoderune>
   0x4832f9 <main.goxor+233>:   mov    esi,DWORD PTR [rsp+0x18]
   0x4832fd <main.goxor+237>:   mov    rax,QWORD PTR [rsp+0x20]
   0x483302 <main.goxor+242>:   mov    rcx,QWORD PTR [rsp+0x38]
   0x483307 <main.goxor+247>:   mov    rdx,QWORD PTR [rsp+0xa8]
   0x48330f <main.goxor+255>:   mov    rbx,QWORD PTR [rsp+0xa0]
   0x483317 <main.goxor+263>:   jmp    0x48329c <main.goxor+140>
   0x483319 <main.goxor+265>:   cmp    rcx,0x26
   0x48331d <main.goxor+269>:   je     0x48332f <main.goxor+287>
   0x48331f <main.goxor+271>:   mov    rbp,QWORD PTR [rsp+0x90]
   0x483327 <main.goxor+279>:   add    rsp,0x98
   0x48332e <main.goxor+286>:   ret    


```

This is somewhat of a long function, but we can quickly identify some important pieces. One of them is the call to `os.Exit` at `0x4832c5`. This is presumably a bad condition we do not want to hit, so hitting that is likely bad. We can also see before the `os.Exit` call we have a `jmp` to `0x48326f` this is an identification pattern of a loop. 

Looking at the instructions between `0x48326f` and `0x4832b6` we can see that there are more signs of a for loop with the `cmp rax, rdx` instruction and `rdx` gets a value put into it. Before that you can see that `eax` is 0'd out with `xor eax, eax` Let's break at `0x483277` and see what those values are. 

``` 
b *0x483277

RAX: 0x0 
RBX: 0x0 
RCX: 0x0 
RDX: 0xb ('\x0b')

=> 0x483277 <main.goxor+103>:   cmp    rax,rdx

```

We can see that RAX at this point is 0 and it is determining if the `RAX` is greater or equal to `rdx`, and if so it will jmp to 0x483319. RDX is 0x0b so we will not take the jump. At this point, note that 0xb is 11, which is the length of our test string "test string". We can also look above at RDX

To determine this, we can break at this instruction `0x48326f <main.goxor+95>:    mov    rdx,QWORD PTR [rsp+0xa8]` and see RDX getting the length of our string. 

From here, we now know we are going through a loop with a case where RAX is not greater than or equal to RDX. This is known due to these instructions `0x483299 <main.goxor+137>:   inc    rax`.  

Looking further, and stepping through the code more, we get to some operations that are important.

```
0x483285 <main.goxor+117>:   mov    rbx,QWORD PTR [rsp+0xa0] # Puts our input string into RBX
```

As we progress, we get to these instructions 

```
0x48328d <main.goxor+125>:   movzx  esi,BYTE PTR [rbx+rax*1] # Moves a byte of a string into ESI. This string can be found with the following

gdb-peda$ x/4s $rbx+$rax*1
0x7fffffffdf7e: "test string"


0x483291 <main.goxor+129>:   cmp    esi,0x80 # compares esi to 0x80 and acts on it by either taking or not taking a jump to 0x4832e6


0x48329c <main.goxor+140>:   cmp    rcx,0x27 # compares rcx, which appears to be used as a counter, to 0x27 (39)

0x4832a6 <main.goxor+150>:   xor    esi,0x7f # XORing a value in ESI with 0x7f. ESI currently contains the first value of our string on the first loop "t". 

0x4832a9 <main.goxor+153>:   movzx  edi,BYTE PTR [rsp+rcx*1+0x49] # After the XOR we move a value into edi that will be compared with the following 

gdb-peda$ x/4b $rsp+$rcx*1+0x49                                                                                                                                                                                     
0xc420053ee1:   61      44      22      27

```

So, we start out by comparing the XOR operation of "T" with 0x7f to "61". with the next instruction

```
0x4832ae <main.goxor+158>:   cmp    sil,dil

```

This will compare the low 8-bit RSI and low 8-bit RDI registers. 

Note: This is somewhat confusing if you have never done x64 before. SIL and DIL are the least significant 8 bits of the 64 bit register. An example of RSI is 

```
RSI - ESI - SI - SIL
64  - 32  - 16 - low-8
``` 

If the values do not match, we wind up taking the route to `Os.Exit`

Let's see what we have right now. Know we are comparing our string to something else and are XORing it against 0x7f. If we make a jump in logic that we are going to compare 39 characters due to that counter we located before, what happens if we dump 39 bytes from 0xc420053ee1 at the 0x4832a9 instruction?

Let's see

```
b *0x4832a9
c
c
c
Thread 1 "goxor" hit Breakpoint 3, 0x00000000004832a9 in main.goxor ()
gdb-peda$ x/39b $rsp+$rcx*1+0x49   
0xc420053ee1:   61      44      22      27      26      12      47      59
0xc420053ee9:   39      4       24      79      15      23      76      13
0xc420053ef1:   32      13      10      19      76      74      32      11
0xc420053ef9:   76      23      32      8       79      13      78      27
0xc420053f01:   32      79      7       72      25      2       117
```

Understanding the logic, we are going to XOR our string in a row over these bytes. What happens if we quickly write a program to do this?

```
// BSidesPDX CTF 2018
// RE-100 Solution

package main

import (
        "fmt"
)

func goxor() {
    var solution string = ""
    challenge := []byte{61,44,22,27,26,12,47,59,39,4,24,79,15,23,76,13,32,13,10,19,76,74,32,11,76,23,32,8,79,13,78,27,32,79,7,72,25,2,117}

    for _, char := range challenge {
        charx := char ^ 0x7f
        solution += string(charx)
    }

    fmt.Println(solution + " is the correct flag!")
}

func main() {

    goxor()

``` 


```
go build gosolution.go 

./gosolution 
BSidesPDX{g0ph3r_rul35_t3h_w0r1d_0x7f}
 is the correct flag!
```

and we get the flag `BSidesPDX{g0ph3r_rul35_t3h_w0r1d_0x7f}`