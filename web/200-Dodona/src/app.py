from flask import Flask, make_response, request, abort
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Padding
import base64
import hashlib
import json
import urllib

app = Flask(__name__)

IV = Random.new().read(AES.block_size)

#KEY = hashlib.sha256("testing").digest()
KEY = "testing1testing1"

PADDING_STYLE = "pkcs7"


STARTING_COOKIE = {'username': 'user', 'whats_the_answer_to_life_the_universe_and_everything': 42, 'put_some_text_here': ''}
#STARTING_COOKIE = {'u': 'u'}
@app.route("/")
def hello():
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    test = request.cookies.get('WhatIsThis')

    if test is None:
        padded = Padding.pad(json.dumps(STARTING_COOKIE), AES.block_size, style=PADDING_STYLE)
#        padded = json.dumps(STARTING_COOKIE)
        resp = make_response()
        resp.set_cookie("WhatIsThis", urllib.quote(base64.b64encode(IV + cipher.encrypt(padded))))
        return resp
    else:
        try:
            print test
            test1 = base64.b64decode(urllib.unquote(test))
            print test1
            unencrypted = cipher.decrypt(test1)
            print unencrypted
            unpadded = Padding.unpad(unencrypted, AES.block_size, style=PADDING_STYLE)
            return unpadded

        except Exception, e:
            print str(e)
            abort(500)
#    return str(AES.block_size)

@app.route("/clear_cookie")
def clear_cookie():
    resp = make_response()
    resp.delete_cookie("WhatIsThis")
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
