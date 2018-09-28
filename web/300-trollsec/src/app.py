from flask import Flask, make_response, g, request, jsonify
from threading import Timer
import os
import random
import sqlite3

app = Flask(__name__)

CURRENT_TOKEN_DATA=""
CURRENT_TOKEN = -1

TOKEN_UPDATE_INTERVAL=60

app.database = "trollsec.db"

@app.route("/")
def hello():
    return "hi"

@app.route("/search", methods=['GET'])
def search():
    if request.method == 'GET':
        print request.form
        print request.data
        print request.json
        if request.args.get("text") is not None and request.headers.get("token") is not None:
            
            if not check_token(request.headers.get("token")):
                return "TOKEN ERROR"

            g.db = connect_db()
            query = "SELECT url FROM trolls WHERE url LIKE '%{}%'".format(request.args.get("text"))
            curs = g.db.execute(query)
            rows = curs.fetchall()
            g.db.close()
            all_users = [{'name':user[0]} for user in rows]
            return jsonify(all_users)
    else:
        return "ERROR"

    return "Wat"

@app.route("/token")
def show_token():
    global CURRENT_TOKEN_DATA
    response = make_response(CURRENT_TOKEN_DATA)
    response.headers.set('Content-Type', 'image/jpeg')
    #response.headers.set('Content-Disposition', 'attachment', filename='token.jpg')
    return response

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
    app.run(host='0.0.0.0', port=80)
