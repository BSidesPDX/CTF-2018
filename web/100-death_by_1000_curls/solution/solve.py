import requests

sess = requests.session()

URL="127.0.0.1"
PORT="4000"

r = sess.get("http://%s:%s/static/dict.txt" % (URL, PORT))

ordering = {}

for line in r.text.split('\n'):
    test = sess.get("http://%s:%s/%s" % (URL, PORT, line))
    if test.text.isdigit():
        ordering[int(test.text)] = line

for i in range(1, 1001):
    sess.get("http://%s:%s/%s" % (URL, PORT, ordering[i]))

print sess.get("http://%s:%s" % (URL, PORT)).text
