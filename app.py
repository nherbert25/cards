from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    print('testing')
    print('pls work')
    print('test3')
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
