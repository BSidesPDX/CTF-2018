# Forensics 100 Creation

To create the forensics 100 problem, in a Debian virtual machine, I opened up Wireshark and began intercepting traffic. Then, I ran the script `generate.py` in this directory and immediately began browsing random websites such as Reddit, Google, Imgur, etc (to create traffic to make it more difficult to see the real flag's traffic just by looking in Wireshark). Then, I exported the pcap file.

The generation of the flag's traffic is documented in `generate.py` in this directory.
