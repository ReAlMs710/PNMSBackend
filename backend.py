from flask import Flask, request
import hashlib, string, random, json

app = Flask(__name__)

sessions = {}
users = {}


@app.route('/')
def index():
    return open("index.html").read()

@app.route('/script')
def whatever():
    return open("index.js").read()








@app.route('/makeaccount', methods=['POST'])
def makeaccount():
    data = request.json
    if data["username"] in users.keys():
        return "taken"
    salt = ''.join(random.choices(string.ascii_letters, k=5))
    hashed = hashlib.md5((data["password"]+salt).encode()).hexdigest()
    users[data["username"]] = { "email": data["email"], "hash": hashed, "salt": salt }
    with open("users.lol", "w") as file:
        file.write(json.dumps(users))
    return "ok"

@app.route('/startsession', methods=['POST'])
def startsession():
    data = request.json
    return "ok"

@app.route('/api', methods=['POST'])
def api():
    print(request.json)
    return request.json["hi"]

if __name__ == '__main__':
    users = json.loads(open("users.lol").read())
    app.run(host='0.0.0.0', port=5000)
