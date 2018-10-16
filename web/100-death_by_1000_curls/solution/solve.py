import requests
import base64
sess = requests.session()

URL="127.0.0.1"
PORT="43478"

r = sess.get("http://%s:%s/static/dict.txt" % (URL, PORT))

ordering = {}

for line in r.text.split('\n'):
    line = line.strip()
    if len(line) == 0:
        pass

    test = sess.get("http://%s:%s/%s" % (URL, PORT, line))
    if len(test.text) > 0:
        try:
            num = base64.b64decode(test.text)
            ordering[int(num)] = line
        except:
            pass

for i in range(1, 1001):
    sess.get("http://%s:%s/%s" % (URL, PORT, ordering[i]))

print sess.get("http://%s:%s" % (URL, PORT)).text
