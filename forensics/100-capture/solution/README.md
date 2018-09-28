# Forensics 100 Solution

## Solution

The attacker is following these steps to exfiltrate information:
1. Open the flag file (and *set x = 0*)
2. Read character at position *x*, get the integer value of the character (ASCII), store it in *y*
3. Attempt to connect to 102.108.97.103 (ASCII value of each octet in f.l.a.g) on port *y*
4. Increment *x* by +1
5. If the end of the file has not been reached, jump to step 2

So, to solve this, write a script to parse through each packet, check if the IP is 102.108.97.103, and if so, check if it is a retransmission packet. If not, convert the number to a character, and add to a string buffer. Once this process is complete, printing out the string buffer will give the flag.
