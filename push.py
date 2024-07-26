from flask import Flask

app = Flask(__name__)

sk = "sk-proj-zCq1qZN9XUcIAqXUu5TwT3BlbkFJpB3QepxWvntDU0EtrMOw"


@app.route('/')
def index():
    return 'Hello from Flask!'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
