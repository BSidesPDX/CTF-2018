from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
app.config.from_object(__name__)
Session(app)

URL_ORDER_FILE="url_visit_order.txt"
VISIT_ORDER = {}

# A lot of this needs to be cleaned up, and will be, just getting it functional for now

@app.route("/")
def hello():
    html = ''
#    if 'last_url' in session and 'last_url_number' in session:
#        html += "%s: %i" % (session['last_url'],  session['last_url_number'])

    if 'last_url_number' in session and session['last_url_number'] == 1000:
        # set the real key
        html += "<h3>key!!!!!!</h3>"
    else:
        html += "<h3>Not yet....</h3>"
    return html

@app.route('/<path:word>')
def check_path(word):
    if 'last_url_number' not in session:
        session['last_url_number'] = 0
    if 'last_url' not in session:
        session['last_url'] = ''


    if word in VISIT_ORDER:
        last_url_number = session['last_url_number']
        this_url_number = VISIT_ORDER[word]
        if this_url_number == last_url_number + 1:
            session['last_url_number'] = this_url_number
        else:
            session['last_url_number'] = 0
    else:
        session['last_visit_number'] = 0

    session['last_url'] = word

    # should obfuscate this to make things a bit harder....
    if word in VISIT_ORDER:
        return str(VISIT_ORDER[word])
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
    app.run(host='0.0.0.0', port=80)
