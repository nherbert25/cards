from flask import render_template, request, redirect, url_for, flash
from flask_bcrypt import check_password_hash
from cards.app_setup import create_app, socketio, db, bcrypt
from cards.database.user_table_DAO import UserTableDAO
from cards.forms import RegistrationForm, LoginForm
from cards.database.models import User

# Creating application
app = create_app()

# initializing local class objects
user_table_dao = UserTableDAO(db.session)


@app.route('/health_check')
def health_check():
    return "OK", 200


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        if user_table_dao.get_user_by_username(username=form.username.data):
            flash('Username has already been taken', 'danger')
            return render_template('register.html', title='Register', form=form)

        elif user_table_dao.get_user_by_email(email=form.email.data):
            flash('Email has already been taken', 'danger')
            return render_template('register.html', title='Register', form=form)

        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user_table_dao.add_user_to_database(user)
            flash('Account created, please login!', 'success')
            return redirect(url_for('login'))
    else:
        print('Error validating registration form!')
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', title='login', form=form), 200

    if request.method == 'POST':
        if form.validate():
            db_user = user_table_dao.get_user_by_email(email=form.email.data)

            # TODO: make check_password_hash pull from user_table_dao.verify_password
            if db_user is not None and check_password_hash(db_user.password, form.password.data):
                flash('You have been logged in!', 'success')
                return redirect(url_for('home')), 302
            else:
                flash('Invalid login. Please check username and password', 'danger')
                return render_template('login.html', title='login', form=form), 401
        else:
            flash('Invalid login. Please check username and password', 'danger')
            return render_template('login.html', title='login', form=form), 400


if __name__ == '__main__':
    # socketio.run encapsulates app.run but includes web socket functionality
    socketio.run(app, allow_unsafe_werkzeug=True)
