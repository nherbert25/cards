from flask import Flask, render_template, request

app = Flask(__name__)


#@app.route('/')
def hello_world():  # put application's code here
    print('testing')
    print('pls work')
    print('test3')
    return 'Hello World!'


@app.route('/') # this defines the entrance to your code. my_website.com goes HERE as well as my_website.com/home
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]

    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run()
