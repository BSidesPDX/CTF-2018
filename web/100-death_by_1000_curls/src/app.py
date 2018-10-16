from flask import Flask, session, render_template
from flask_session import Session
import base64

app = Flask(__name__)

# Used to store session information on the server end rather than in a cookie
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False

app.config.from_object(__name__)
Session(app)

URL_ORDER_FILE="url_visit_order.txt"
VISIT_ORDER = {}

# Either spits out the key if correct URLs were visited, or just tells the user to go away
@app.route("/")
def hello():
    if 'last_url_number' in session and session['last_url_number'] == 1000:
        # set the real key
        return render_template('key.html')
    else:
        return render_template('not_yet.html')

# Checks the word in the path against the next expected word for this user
@app.route('/<path:word>')
def check_path(word):

    # We haven't seen this user before, so set them up
    if 'last_url_number' not in session:
        session['last_url_number'] = 0
    if 'last_url' not in session:
        session['last_url'] = ''

    # Check if this word is one of the 1000
    if word in VISIT_ORDER:
        last_url_number = session['last_url_number']
        this_url_number = VISIT_ORDER[word]

        # If this is the next URL expected to be visited by this user, increment their counter
        if this_url_number == last_url_number + 1:
            session['last_url_number'] = this_url_number

        # Otherwise, URLs were visited in the wrong order, reset
        else:
            session['last_url_number'] = 0

    # Word was not in list of 1000
    else:
        session['last_visit_number'] = 0

    session['last_url'] = word

    # If this word is in the 1000 list, base encode it's ordering number and return to the user
    if word in VISIT_ORDER:
        return base64.b64encode(str(VISIT_ORDER[word]))
    return "" 


def setup_app(app):
    setup_url_order()

def setup_url_order():
    with open(URL_ORDER_FILE, 'r') as f:
        count = 1
        for line in f.readlines():
            VISIT_ORDER[line.strip()] = count
            count += 1

setup_app(app)

if __name__ == "__main__":
    app.run(threaded=True,host='0.0.0.0', port=43478)
