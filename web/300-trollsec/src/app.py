from flask import Flask, make_response, g, request, jsonify, render_template
from flask_cors import cross_origin
from threading import Timer
import os
import random
import sqlite3

app = Flask(__name__)

# Stores the token image data as well as token value
CURRENT_TOKEN_DATA=""
CURRENT_TOKEN = -1

# How often to update the token in seconds
TOKEN_UPDATE_INTERVAL=60

app.database = "trollsec.db"

# Just used for random video selection
NUM_TROLL_VIDS = 7

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/search")
def search():
    return render_template('search.html')

# Ajax search helper, returns JSON array of results
@app.route("/_search", methods=['GET'])
def _search():
    if request.method == 'GET':
        if __debug__:
            print request.args

        query = request.args.get("query")

        # Note: token value is a header!
        token = request.headers.get("token")

        if query is not None and token is not None:
            if not check_token(token):
                return "TOKEN ERROR"

            g.db = connect_db()
            query = "SELECT url,name FROM trolls WHERE name LIKE '%{}%'".format(query)
            curs = g.db.execute(query)
            rows = curs.fetchall()
            g.db.close()
            all_trolls = [{'url':troll[0], 'name':troll[1]} for troll in rows]
            return jsonify(all_trolls)
    else:
        return "ERROR"

    return "Wat"

@app.route("/token")
def show_token():
    global CURRENT_TOKEN_DATA
    response = make_response(CURRENT_TOKEN_DATA)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


# Have to set cross origin for error handler as we're grabbing various JSs for youtube vids
@app.errorhandler(Exception)
@cross_origin()
def http_error_handler(error):
    video = random.randint(1, NUM_TROLL_VIDS + 1)
    return render_template('error.html', video=video), 418

def check_token(token):
    global CURRENT_TOKEN

    if __debug__:
        print token
        print CURRENT_TOKEN

    if token == CURRENT_TOKEN:
        return True
    else:
        return False

def connect_db():
    return sqlite3.connect(app.database)

# Updates the current token data and sets up timer to change in TOKEN_UPDATE_INTERVAL seconds
def update_token():
    global CURRENT_TOKEN_DATA
    global CURRENT_TOKEN

    Timer(TOKEN_UPDATE_INTERVAL, update_token).start()

    token_file = random.choice(os.listdir("images"))
    
    # Token value is grabbed from filename, minus ".jpg"
    CURRENT_TOKEN = token_file[:-4]

    with open("images/" + token_file, 'rb') as img:
        CURRENT_TOKEN_DATA = img.read()
        
update_token()


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=10101)
