## Problem Statement
Future Gadget Labs is thought to have a secret secure website where only the most elite customers can purchase their gadgets. The only problem is that it's on a subdomain that doesn't appear in any of our wordlists. We've been having a real hard time finding it, but we're sure there's a log of it somewhere.

## Solution
The secret secure website is using HTTPS via Lets Encrypt, which means that all certificates issued will appear in certificate transparency logs. Tools such as [https://crt.sh](crt.sh) or [https://sslmate.com/foreign_certs](certspotter) comb through these logs and make it easy to secure information about a target domain.


## Flag
BsidesPDX{tr4nsp4r3ncy_1s_c00l}