from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_bcrypt import check_password_hash
from app_setup import create_app, socketio
from networking.client import Client
from forms import RegistrationForm, LoginForm
from database.models import User

# application factory pattern
app, db, sess, bcrypt = create_app()


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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created, please login!', 'success')
        print('Form validated!')
        return redirect(url_for('login'))
    else:
        print('Error validating registration form!')
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        db_user = User.query.filter_by(email=form.email.data).first()

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
