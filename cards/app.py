from flask import render_template, request, redirect, session, url_for, flash
from flask_bcrypt import check_password_hash
from cards.app_setup import create_app, socketio
from cards.database.user_table_DAO import UserTableDAO
from cards.networking.client import Client
from cards.forms import RegistrationForm, LoginForm
from cards.database.models import User

# application factory pattern
app, db, sess, bcrypt = create_app()

# initializing local classes
MyUserTableDAO = UserTableDAO(db.session)


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

        return render_template('blackjack.html', player_name=session['player_name'])
    except Exception as e:
        return 'Error: {}'.format(e)


@app.route('/player_choice', methods=['POST'])
def player_choice():
    # player_card = "{{ url_for('static', filename='playing_cards/BACK.png') }}"
    if request.form.get('hit') == 'Hit':
        hit = True
        print('Player chose to hit!')
        player_name = session.get('player_name')
        return render_template('blackjack.html', player_name=session['player_name'], hit=hit)

    elif request.form.get('stay') == 'Stay':
        print('Player chose to stay!')
        player_name = session.get('player_name')
        return render_template('blackjack.html', player_name=session['player_name'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        if MyUserTableDAO.get_user_by_username(username=form.username.data):
            flash('Username has already been taken', 'danger')
            return render_template('register.html', title='Register', form=form)

        elif MyUserTableDAO.get_user_by_email(email=form.email.data):
            flash('Email has already been taken', 'danger')
            return render_template('register.html', title='Register', form=form)

        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            MyUserTableDAO.add_user_to_database(user)
            flash('Account created, please login!', 'success')
            return redirect(url_for('login'))
    else:
        print('Error validating registration form!')
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        db_user = MyUserTableDAO.get_user_by_email(email=form.email.data)

        if db_user is not None and check_password_hash(db_user.password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid login. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


if __name__ == '__main__':
    # socketio.run encapsulates app.run but includes web socket functionality
    socketio.run(app, allow_unsafe_werkzeug=True)
    # app.run(debug=True)
