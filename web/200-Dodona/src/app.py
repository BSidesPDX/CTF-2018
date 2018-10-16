from flask import Flask, make_response, request, abort, render_template
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Padding
import base64
import hashlib
import json
import urllib
import random

app = Flask(__name__)

IV = Random.new().read(AES.block_size)

random.seed()

KEY = ''.join(chr(random.randint(0,255)) for i in range(16))

PADDING_STYLE = "pkcs7"

# Default cookie data
STARTING_COOKIE_DATA = {'username': 'guest', 'whats_the_answer_to_life_the_universe_and_everything': '', 'security_put_some_text_here': ''}
COOKIE_NAME = "wisdom_of_the_gods"


@app.route("/")
def index():
    current_cookie = request.cookies.get(COOKIE_NAME)

    has_query = False
    answer = ''
    
    # Completely pointless, just a little fun..
    if "q" in request.args:
        has_query = True
        if "flag" in request.args["q"].lower():
            answer = "The answer is not that simple..."
        else:
            answer = magic_8_ball()

    # If user doesn't have a cookie set, set them up with one
    if current_cookie is None:
        encrypted_cookie = encrypt_cookie(STARTING_COOKIE_DATA)
        resp = make_response(render_template('index.html', query=has_query))
        resp.set_cookie(COOKIE_NAME, encrypted_cookie)
        return resp

    # Otherwise, attempt to decrypt the cookie. Gives useful info during padding oracle attack.
    else:
        decrypted_cookie = decrypt_cookie(current_cookie)

        resp = make_response(render_template('index.html', query=has_query, answer=answer))

        return resp

# If correct cookie has been set, show the user the flag. Otherwise, they get a 403 Forbidden as a hint there is something here
@app.route("/admin")
def admin():
    solved = False

    current_cookie = request.cookies.get(COOKIE_NAME)
    if current_cookie is not None:
        decrypted_cookie = decrypt_cookie(current_cookie)
        solved = check_cookie(decrypted_cookie)

    if not solved:
        abort(403)
    else:
        return render_template('admin.html')

def magic_8_ball():
    answers = [
            "As I see it, yes",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "My reply is no",
            "The gods say no",
            "Outlook good",
            "Outlook not so good",
            "Reply hazy, try again",
            "Signs point to yes",
            "Very doubtful",
            "Without a doubt",
            "Yes",
            "Yes, definitely",
            "You may rely on it"
    ]

    return random.choice(answers)


# Encrypt data for the cookie
def encrypt_cookie(cookie_data):
    cookie_cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded = Padding.pad(json.dumps(cookie_data), AES.block_size, style=PADDING_STYLE)
    encrypted_cookie = urllib.quote(base64.b64encode(IV + cookie_cipher.encrypt(padded)))

    return encrypted_cookie

# Attempt to decrypt the cookie
def decrypt_cookie(encrypted_cookie):
    cookie_cipher = AES.new(KEY, AES.MODE_CBC, IV)
    
    # Cookie decryption may fail if user has messed with the data
    try:
        b64_decoded_cookie = base64.b64decode(urllib.unquote(encrypted_cookie))
        decrypted_cookie = cookie_cipher.decrypt(b64_decoded_cookie)
        unpadded_cookie = Padding.unpad(decrypted_cookie, AES.block_size, style=PADDING_STYLE)
        unpadded_cookie = unpadded_cookie[len(IV):] #remove beginning IV
        return unpadded_cookie

    # If cookie decryption fails for any reason, throw up a 500. Gives useful info to user during padding oracle attack
    except Exception, e:
        print str(e)
        abort(500)


# Check if the cookie has all the correct data to solve the challenge
# Username should be 'admin'
# whats_the_answer_to_life_the_universe_and_everything should be 42
# and security_put_some_text_here should just contain something
def check_cookie(cookie_data):
    cookie = json.loads(cookie_data)

    if (    'username' in cookie and 
            cookie.get('username').lower() == 'admin' and
            'whats_the_answer_to_life_the_universe_and_everything' in cookie and
            cookie.get('whats_the_answer_to_life_the_universe_and_everything') == '42' and
            'security_put_some_text_here' in cookie and
            len(cookie.get('security_put_some_text_here')) > 0
       ):
        return True

    return False


# Useful feature during debugging so I didn't have to manually remove the cookie every time :)
# will leave in just in case it's useful during the CTF
@app.route("/clear_cookie")
def clear_cookie():
    resp = make_response()
    resp.delete_cookie(COOKIE_NAME)
    return resp

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=4738)
