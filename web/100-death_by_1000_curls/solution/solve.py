import requests

sess = requests.session()

r = sess.get("http://127.0.0.1/static/dict.txt")

ordering = {}

for line in r.text.split('\n'):
    test = sess.get("http://127.0.0.1/%s" % line)
    if test.text.isdigit():
        ordering[int(test.text)] = line

for i in range(1, 1001):
    sess.get("http://127.0.0.1/%s" % ordering[i])

print sess.get("http://127.0.0.1").text
