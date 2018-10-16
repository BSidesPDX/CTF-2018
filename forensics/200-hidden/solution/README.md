# Forensics 200 Solution

## Solution

This challenge uses a few layers of protection on the flag.

1. Use `steghide` (hinted in the problem description) to extract the file that was stored with a blank password
```
$ steghide extract -sf output.wav
Enter passphrase:
wrote extracted data to "message".
$ cat message
Progress, but where is the key hidden?
```
2. Open up the audio file in Audacity.
    a. Select the track, then from the dropdown menu, choose `Split Stereo to Mono`
    b. Select one of the tracks (doesn't matter which), then do `Effects > Invert`
    c. Select all tracks, then choose `Tracks > Mix and Render`
    d. From the new track's dropdown menu, choose `Spectrogram`
    e. Copy down each dot (`.`) and dash (`-`), then morse decode
```
FILE KEY IN CAPS IS L0LWEAK
```
3. Extract the file using the new password from the audio file
```
$ steghide extract -sf output.wav
Enter passphrase: L0LWEAK
wrote extracted data to "cooltar".
$ file cooltar
cooltar: gzip compressed data, last modified: Wed Jul  4 23:36:13 2018, from Unix, original size 10240
```
4. Now we know what type of file it is. Let's extract the archive.
```
$ tar -xzvf cooltar
.wow
$ cat .wow
cat: .wow: Permission denied
$ ls -lah .wow
---------- 1 <user> <user> 111 Jul  4 16:22 .wow
```
5. Permission denied?! Well, that's easy to fix.
```
$ chmod 777 .wow
$ cat .wow
the flag must be somewhere around here, right?
```
6. Well, did you notice that when you ran `ls -lah .wow`, it said the filesize was 111 bytes? Well, the text that was printed out was only 46 bytes. Perhaps there is some kind of character covering up the flag? Otherwise, where are the other 65 bytes?
```
$ hexdump -C .wow
42 53 69 64 65 73 50 44  58 7b 6c 31 6b 65 5f 61  |BSidesPDX{l1ke_a|
73 63 49 49 2d 62 40 63  6b 24 70 61 63 33 3f 7d  |scII-b@ck$pac3?}|
08 08 08 08 08 08 08 08  08 08 08 08 08 08 08 08  |................|
74 68 65 20 66 6c 61 67  20 6d 75 73 74 20 62 65  |the flag must be|
20 73 6f 6d 65 77 68 65  72 65 20 61 72 6f 75 6e  | somewhere aroun|
64 20 68 65 72 65 2c 20  72 69 67 68 74 3f 0a     |d here, right?. |
```

There's the flag! As it turns out, the flag was hidden with the ASCII character 0x08, which is a BS (Backspace) character. `hexdump` is a useful tool. Another tool that could've been used is `strings`:

```
$ strings .wow
BSidesPDX{l1ke_ascII-b@ck$pac3?}
the flag must be somewhere around here, right?
```

or even `vim` of all things:

```
$ vim .wow
BSidesPDX{l1ke_ascII-b@ck$pac3?}^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^H^Hthe flag must be somewhere around here, right?
```
