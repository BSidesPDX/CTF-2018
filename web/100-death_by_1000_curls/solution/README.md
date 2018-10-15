#Web 100 Solution

##Solution


Upon first visiting the page, I'm greeted with the message:
```
Go away

I have not heard the secret knock yet
```

Well that seems friendly, doesn't it? Taking a look into the page source, it seems there's an html comment
```
<!doctype html>
<title>Knock knock knock....</title>
<h1>Go away</h1>
<p>I have not heard the secret knock yet</p>

<!-- /static/dict.txt -->
```

/static/dict.txt? Navigating to that URL, it's a 4000 line long dictionary file with a bunch of words in no particular order. Considering the message from before about not hearing the secret knock, we might need to append some of these words to the URL in some particular order. Let's try visiting some of these URLs and see what happens.

The first few URLS (e.g. /concerned, /learn, /person, and /scared) all return blank pages. However, once we hit /holistic, we get some text back:
```
MTk4
```
Which is a bit strange. After hitting enough of these URLs, it becomes clear this text is actually base64 encoded. The MTk4 decodes to 198. After hitting all the URLs in the dictionary, there are base64 encoded strings for all values from 1 to 1000.

At this point, let's try hitting all the URLs in the correct order. Here's a quick python script to grab the dictionary, parse it, figure out the ordering of the URLs, and then hit the URLs in the correct order:

```
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
```

After hitting all the URLs in the correct order, the script hits the home page once again and we get the flag!

```
<!doctype html>
<title>Who's there?</title>
<h1>BSidesPDX{B3773r_th4n_d34th_By_1000_cu75}</h1>
```