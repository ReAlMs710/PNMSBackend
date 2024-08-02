from flask import Flask, request, Response, send_from_directory
import hashlib, string, random, json, mimetypes, time
from conversation_runner import ConversationRunner

app = Flask(__name__)

sessions = {}
users = {}


@app.route('/')
def index():
    return open("index.html").read()

@app.route('/Logo.png')
def index():
    return open("Logo.png").read()

@app.route('/assets/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)
    # ext = path.split(".")[-1]
    # print(ext)
    # if ext == "jsx":
    #     r.headers['Content-Type'] = 'text/typescript-jsx'
    # else:
    #     r.headers["Content-Type"] = mimetypes.guess_type(path, strict=False)[0]

    # #return send_from_directory('src', path)
    # return r






@app.route('/makeaccount', methods=['POST'])
def makeaccount():
    data = request.json
    if data["username"] in users.keys():
        return "taken"
    salt = ''.join(random.choices(string.ascii_letters, k=5))
    hashed = hashlib.md5((data["password"]+salt).encode()).hexdigest()
    users[data["username"]] = { "email": data["email"], "hash": hashed, "salt": salt }
    with open("users.json", "w") as file:
        file.write(json.dumps(users))
    return "ok"

@app.route('/startsession', methods=['POST'])
def startsession():
    data = request.json
    hashed = hashlib.md5((data["password"]+users[data["username"]]["salt"]).encode()).hexdigest()
    if hashed != users[data["username"]]["hash"]:
        return "badpass"
    rand = ''.join(random.choices(string.ascii_letters, k=32))
    while rand in sessions.keys():
        rand = ''.join(random.choices(string.ascii_letters, k=32))
    sessions[rand] = { "username": data["username"], "lastactive": time.time(), "chatbot": ConversationRunner() }
    print(sessions)
    return rand

@app.route('/profile', methods=['POST'])
def profile():
    data = request.json
    if data["session"] not in sessions:
        return "session not found"
    if data["type"] == 'get':
        return {
                "username": sessions[data["session"]]["username"],
                "email": users[sessions[data["session"]]["username"]]["email"],
                "firstlang": users[sessions[data["session"]]["username"]]["firstlang"]
        }
    if data["firstlang"]:
        users[sessions[data["session"]]["username"]]["firstlang"] = data["firstlang"]
    if data["email"]:
        users[sessions[data["session"]]["username"]]["email"] = data["email"]
    with open("users.json", "w") as file:
        file.write(json.dumps(users))
    return "ok"

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    if data["session"] not in sessions:
        return "session not found"
    return sessions[data["session"]]["chatbot"].next(data["text"])

if __name__ == '__main__':
    users = json.loads(open("users.json").read())
    app.run(host='0.0.0.0', port=5000)
