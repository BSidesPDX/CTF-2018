# re 100 - goxor

## Description

golang binary with a XOR routine that hides the secret flag. Requires reversing of golang binary to identify the flag.

Give player binary from `distFiles`

## Deploy

1. change flag in flag file
2. run xor.py and copy the result to line 13 in goxor.go where the challenge byte array is
3. go build -ldflags '-w' goxor.go

## Challenge

I hide a flag in this file. Can you be a good Gopher and find it?

flag: BSidesPDX{g0ph3r_rul35_t3h_w0r1d}
