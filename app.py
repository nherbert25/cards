from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from black_jack.routes import black_jack_blueprint
from networking.client import Client
from forms import RegistrationForm, LoginForm
from flask_login import UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'anA194$38@na.dn0832A'
app.register_blueprint(black_jack_blueprint)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)


# this defines the entrance to your code. my_website.com goes HERE
# (because @app.route('/')) as well as my_website.com/home (because @app.route('/home'))
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]

    return render_template('index.html', name=name)


@app.route('/join_game', methods=['POST'])
def join_game():
    ip_address = request.form['ip_address']
    port = int(request.form['port'])

    # Connect to the game server
    try:
        # Create a socket
        client = Client(server_ip=ip_address, server_port=port)

        # Ask for player name
        session['player_name'] = input("Enter your player name: ")
        client.send_data(session['player_name'])

        # Receive a response from the server
        data = client.receive_data()

        return render_template('black_jack.html', player_name=session['player_name'])
    except Exception as e:
        return 'Error: {}'.format(e)


@app.route('/player_choice', methods=['POST'])
def player_choice():
    # player_card = "{{ url_for('static', filename='playing_cards/BACK.png') }}"
    if request.form.get('hit') == 'Hit':
        hit = True
        print('Player chose to hit!')
        player_name = session.get('player_name')
        return render_template('black_jack.html', player_name=session['player_name'], hit=hit)

    elif request.form.get('stay') == 'Stay':
        print('Player chose to stay!')
        player_name = session.get('player_name')
        return render_template('black_jack.html', player_name=session['player_name'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        print('Form validated!')
        return redirect(url_for('black_jack.black_jack'))
    else:
        print('Error validating registration form!')
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid login. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
