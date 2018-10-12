from flask import Flask, make_response, g, request, jsonify, render_template
from flask_cors import cross_origin
from threading import Timer
import os
import random
import sqlite3

app = Flask(__name__)

CURRENT_TOKEN_DATA=""
CURRENT_TOKEN = -1

TOKEN_UPDATE_INTERVAL=60

app.database = "trollsec.db"

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

@app.route("/_search", methods=['GET'])
def _search():
    if request.method == 'GET':
        print request.args
        query = request.args.get("query")
        token = request.headers.get("token")
        if query is not None and token is not None:
            if not check_token(token):
                return "TOKEN ERROR"

            g.db = connect_db()
            query = "SELECT url,name FROM trolls WHERE name LIKE '%{}%'".format(query)
            curs = g.db.execute(query)
            rows = curs.fetchall()
            g.db.close()
            print rows
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


#@app.errorhandler(404)
@app.errorhandler(Exception)
@cross_origin()
def http_error_handler(error):
    video = random.randint(1, NUM_TROLL_VIDS + 1)
    return render_template('error.html', video=video), 418

def check_token(token):
    global CURRENT_TOKEN

    #print token
    #print CURRENT_TOKEN

    if token == CURRENT_TOKEN:
        return True
    else:
        return False

def connect_db():
    return sqlite3.connect(app.database)


def update_token():
    global CURRENT_TOKEN_DATA
    global CURRENT_TOKEN

    Timer(TOKEN_UPDATE_INTERVAL, update_token).start()

    token_file = random.choice(os.listdir("images"))
    
    CURRENT_TOKEN = token_file[:-4]

    with open("images/" + token_file, 'rb') as img:
        CURRENT_TOKEN_DATA = img.read()
        
update_token()



if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=80)
