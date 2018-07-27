from scapy.all import *

# import pcap file
print('importing file...')
packets = rdpcap('../distFiles/dump.pcap')

# define some variables to be used later
data = list()
buffer = ''
porthist = list()

# iterate through packets & filter them
print('parsing packets...')
for packet in packets:
    if IP in packet:
        # only keep packets that have 'f.l.a.g' as the IP addr
        if packet[IP].dst == '.'.join([str(ord(i)) for i in 'flag']):
            if TCP in packet:
                sport = int(packet[TCP].sport) # source port
                
                # this is simply to make sure we don't use retransmission packets (er, sort of.)
                if (not sport in porthist):
                    # add port number as character to buffer
                    buffer += chr(int(packet[TCP].dport))
                    
                    # remember that we've seen this source port already
                    porthist.append(sport)

# print out the data
print('complete. here is your output:\n\n%s' % buffer)
