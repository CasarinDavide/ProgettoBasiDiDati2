import datetime, os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from core.UsersClass import UsersClass
from core.AddressesClass import AddressesClass
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK-LOGIN-KEY')

login_manager = LoginManager(app)
login_manager.init_app(app)

# CALLBACK OBBLIGATORIO
@login_manager.user_loader
def load_user(user_id):
    return UsersClass.get_by_id(user_id)

# Home Page
@app.route('/')
def home():
    if current_user.is_authenticated:
        mail = UsersClass.get_by_id(current_user.get_id()).email
        return render_template('./public_html/home.html', user = mail)
    
    return render_template('./public_html/home.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return 'You are already authenticated'

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remind = request.form.get('remind_me') != None
        
        if UsersClass.validate_password(email, password):
            user = UsersClass.get_by_email(email)
            login_user(user, remember = remind )
            return redirect('/')
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            return redirect('/user_login')
        
    return render_template('public_html/login.html')

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tel = request.form['tel']
        civico = request.form['civico']
        via = request.form['via']
        citta = request.form['citta']
        cod_postale = int(request.form['cod_postale'])
        paese = request.form['paese']

        # Controlla che l'indirizzo esista, evita la ridondanza per persone che abitano assieme
        addr = AddressesClass.get_address(civico, via, citta, cod_postale, paese)
        if addr:
            id_addr = addr.id
        else:
            addr = AddressesClass.add(civico, via, citta, cod_postale, paese)
            id_addr = addr.id

        if UsersClass.get_by_email(email):
            flash('A user with this mail already exists.', 'danger')
        else:
            UsersClass.add(email, generate_password_hash(password), tel, id_addr)
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('user_login'))
    return render_template('public_html/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login'))

if __name__ == '__main__':
    app.run(debug=True)
