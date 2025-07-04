import datetime, os
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from core.UsersClass import UsersClass
from core.AddressClass import AddressClass
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK-LOGIN-KEY')

login_manager = LoginManager(app)
login_manager.init_app(app)

# CALLBACK OBBLIGATORIO
@login_manager.user_loader
def load_user(email):
    return UsersClass.get_by_email(email)


# Home Page
@app.route('/')
def home():
    return 'ziocan'


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if UsersClass.validate_password(email, password):
            user = UsersClass.get_by_email(email)
            login_user(user)
            return redirect(url_for(''))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('public_html/login.html')


@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tel = request.form['telefono']
        civico = request.form['civico']
        via = request.form['via']
        citta = request.form['citta']
        cod_postale = int(request.form['codice_postale'])
        paese = request.form['paese']

        # Controlla che l'indirizzo esista, evita la ridondanza per persone che abitano assieme
        addr = AddressClass.get_address(civico, via, citta, cod_postale, paese)
        if addr:
            id_addr = addr.id
        else:
            addr = AddressClass.add(civico, via, citta, cod_postale, paese)
            id_addr = addr.id

        if UsersClass.get_by_email(email):
            flash('A user with this mail already exists.', 'danger')
        else:
            UsersClass.add(email, generate_password_hash(password), tel, id_addr)
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('public_html/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/ajax/<path:params>", methods=["GET", "POST"])
def ajax(params):
    # Extracting func and oper from the params string
    func, oper = params.split('&')
    func = func.split('=')[1]  # Extracting value of func
    oper = oper.split('=')[1]  # Extracting value of oper

    return jsonify({'error': 'Invalid operation'}), 400


if __name__ == '__main__':
    app.run(debug=True)
