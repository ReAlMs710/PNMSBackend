from flask import Flask, request, Response, send_from_directory, send_file
import hashlib, string, random, json, mimetypes, time
from conversation_runner import ConversationRunner

app = Flask(__name__)

sessions = {}
users = {}


@app.route('/')
def index():
    return send_file('index.html')

@app.route('/Logo.png')
def logo():
    return send_file('Logo.png')

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
    rand = ''.join(random.choices(string.ascii_letters, k=32))
    while rand in sessions.keys():
        rand = ''.join(random.choices(string.ascii_letters, k=32))
    sessions[rand] = { "username": data["username"], "lastactive": time.time(), "chatbot": None }
    print(sessions)
    return rand

@app.route('/startsession', methods=['POST'])
def startsession():
    data = request.json
    if data["username"] not in users.keys():
        return "badpass"
    hashed = hashlib.md5((data["password"]+users[data["username"]]["salt"]).encode()).hexdigest()
    if hashed != users[data["username"]]["hash"]:
        return "badpass"
    rand = ''.join(random.choices(string.ascii_letters, k=32))
    while rand in sessions.keys():
        rand = ''.join(random.choices(string.ascii_letters, k=32))
    sessions[rand] = { "username": data["username"], "lastactive": time.time(), "chatbot": None }
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
    username = sessions[data["session"]]["username"]
    if 'firstlang' in data:
        users[username]["firstlang"] = data["firstlang"]
    if 'email' in data:
        users[username]["email"] = data["email"]
    if 'level' in data:
        users[username]["level"] = data["level"]
    if 'goals' in data:
        users[username]["goals"] = data["goals"]
    
    # Debug prints to verify the state of the users dictionary
    print("Updated users dictionary:", users)
    print("Received data:", data)
    
    with open("users.json", "w") as file:
        file.write(json.dumps(users))
    
    # Debug print to confirm file write operation
    print("users.json has been updated.")
    
    return "ok"

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    if sessions[data["session"]]["chatbot"] == None:
        sessions[data["session"]]["chatbot"] = ConversationRunner(
            api_key = "sk-proj-nMqG2JPigq7udXlJfFbRT3BlbkFJPXQbeZtbSq4QBV318Bnl",
            lesson_plan = "basic greetings and introductions",
            user_language = users[sessions[data["session"]]["username"]]["firstlang"],
            lesson_questions = [
                "How do you say 'Hello' in english?",
                "What's the phrase for 'How are you?' in english?",
                "How would you introduce yourself in english?"
            ]
        )

    if data["session"] not in sessions:
        return "session not found"
    return sessions[data["session"]]["chatbot"].next(data["text"])

if __name__ == '__main__':
    users = json.loads(open("users.json").read())
    app.run(host='0.0.0.0', port=8080)
