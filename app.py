import os
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from core.IndirizziClass import IndirizziClass
from core.PasseggeriClass import PasseggeriClass
from core.CompagnieClass import CompagnieClass
from core.DipendentiClass import DipendentiClass
from core.ViaggiClass import ViaggiClass
from core.AereiClass import AereiClass
from core.AereoportiClass import AereoportiClass
from core.DataPartenzeClass import DataPartenzeClass
from core.EffettuanoClass import EffettuanoClass
from core.BigliettiClass import BigliettiClass
from core.VoliClass import VoliClass

from dotenv import load_dotenv
from System import getParam
from services.CompagnieRepository import CompagnieRepository
from services.IndirizziRepository import IndirizziRepository
from services.AereiRepository import AereiRepository

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK-LOGIN-KEY')

login_manager = LoginManager(app)
login_manager.init_app(app)

# CALLBACK OBBLIGATORIO
@login_manager.user_loader
def load_user(user_id):
    return PasseggeriClass.get_by_id(user_id)

# Home Page
@app.route('/')
def home():
    if current_user.is_authenticated:
        nome = PasseggeriClass.get_by_id(current_user.get_id()).nome
        return render_template('./public_html/home.html', user = nome)
    
    return render_template('./public_html/home.html')


@app.route('/admin_settings', methods=['GET', 'POST'])
def admin_settings():
    print(request.method)
    option = getParam("oper")
    print(request.args)
    print(option)
    if option is None:
        return render_template('./public_html/admin_settings.html')
    else:
        return function_actions()



@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return 'You are already authenticated'

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remind = request.form.get('remind_me') != None
        
        if PasseggeriClass.validate_password(email, password):
            user = PasseggeriClass.get_by_email(email)
            login_user(user, remember = remind )
            return redirect('/')
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            return redirect('/user_login')
        
    return render_template('public_html/login.html')

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        #Informazioni principali passeggero
        email = request.form['email']
        password = request.form['password']
        nome = request.form['nome']
        cognome = request.form['cognome']
        prefisso = request.form['prefisso']
        tel = request.form['tel']
        nascita = request.form['nascita']
        saldo = 0.0

        #Indirizzo passeggero
        civico = request.form['civico']
        via = request.form['via']
        citta = request.form['citta']
        cod_postale = int(request.form['cod_postale'])
        paese = request.form['paese']

        # Controlla che l'indirizzo esista, evita la ridondanza per persone che abitano assieme
        addr = IndirizziClass.get_address(civico, via, citta, cod_postale, paese)
        if addr:
            id_addr = addr.address_id
        else:
            addr = IndirizziClass.add(civico, via, citta, cod_postale, paese)
            id_addr = addr.address_id

        if PasseggeriClass.get_by_email(email):
            flash('A user with this mail already exists.', 'danger')
        else:
            PasseggeriClass.add(email, generate_password_hash(password), nome, cognome, prefisso+tel, nascita, saldo, id_addr)
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('home'))
    return render_template('public_html/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login'))


def function_actions():
    target = getParam("fun")
    action = getParam("oper")

    # datatable standard
    draw = int(request.args.get('draw', 1))
    start = int(request.args.get('start', 0))  # offset
    length = int(request.args.get('length', 10))  # page size
    search_value = request.args.get('search[value]', '')
    ####

    if target == "compagnia_aerea":

        compagnie_repo = CompagnieRepository()

        if action == "add":
            return compagnie_repo.add(email=getParam("email"),
                                      password=getParam("password"),
                                      tel=getParam("tel"),
                                      nome=getParam("nome"),
                                      civico=getParam("civico"),
                                      via=getParam("via"),
                                      citta=getParam("citta"),
                                      cod_postale=getParam("cod_postale"),
                                      paese=getParam("paese"),
                                      id_address=getParam("id_address"))

        elif action == "getAllDatatable":
            return compagnie_repo.get_datatable(draw,start,length,search_value)
        elif action == "getById":
            return compagnie_repo.get_by_id(getParam("id_compagnia"))
        if action == "get_for_select":
            return compagnie_repo.get_all()


    elif target == "indirizzi":

        indirizziRepo = IndirizziRepository()

        if action == "get_for_select":
            return jsonify(indirizziRepo.get_all())
    elif target == "aerei":
        aerei_repo = AereiRepository()

        if action == "add":
            return aerei_repo.add(
                capacita =getParam("capacita"),
                modello=getParam("modello"),
                consumoMedio=getParam("consumoMedio"),
                dimensione=getParam("dimensione"),
                id_compagnia=getParam("id_compagnia")
            )

        elif action == "getAllDatatable":
            return aerei_repo.get_datatable(draw,start,length,search_value)
        elif action == "getById":
            return aerei_repo.get_by_id(getParam("id_aereo"))



    return jsonify({"error": "Invalid action"}), 400


if __name__ == '__main__':
    app.run(debug=True)



