import os
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

import System
from System import getParam
from core.AereiClass import AereiClass
from core.AereoportiClass import AereoportiClass
from core.BigliettiClass import BigliettiClass
from core.CompagnieClass import CompagnieClass
from core.DipendentiClass import DipendentiClass
from core.EffettuanoClass import EffettuanoClass
from core.PasseggeriClass import PasseggeriClass
from core.ViaggiClass import ViaggiClass
from core.VoliClass import VoliClass

from dotenv import load_dotenv
from services.AereoportiRepository import AereoportiRepository
from services.CompagnieRepository import CompagnieRepository
from services.AereiRepository import AereiRepository
from services.DipendentiRepository import DipendentiRepository
from services.ViaggiRepository import ViaggiRepository
from services.PasseggeriRepository import PasseggeriRepository
from services.BigliettiRepository import BigliettiRepository
from services.VoliRepository import VoliRepository
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK-LOGIN-KEY')

login_manager = LoginManager(app)
login_manager.init_app(app)


# CALLBACK OBBLIGATORIO
@login_manager.user_loader
#def load_user(user_id):
#    passeggeri_repo = PasseggeriRepository()
#    return passeggeri_repo.get_by_id(user_id)
def load_user(user_id):
    # user_id stored like "company-123" or "passenger-456"
    role, real_id = user_id.split("-", 1)
    if role == "compagnia":
        return CompagnieRepository().get_by_id(real_id)
    elif role == "passeggeri":
        return PasseggeriRepository().get_by_id(real_id)
    elif role == "dipendenti":
        return DipendentiRepository().get_by_id(real_id)

    return None

def custom_login_user(user, remember):
    if isinstance(user, PasseggeriClass) or isinstance(user, CompagnieClass) or isinstance(user, DipendentiClass):
        login_user(System.BaseUser(id=user.get_id(), nome=user.get_nome(), email=user.get_email(), role= user.get_role()),remember=remember)
        session['role'] = user.__class__.__name__

    return None

@login_required
def check_permissions(class_name:list):
    if session['role'] in class_name:
        return True

    flash("Permission denied. You have been logged out.", "danger")
    logout_user()
    return redirect("/home")

# Home Page
@app.route('/', methods = ["GET", "POST"])
def home():
    nome = ""
    passeggeri_repo = PasseggeriRepository()
    if current_user.is_authenticated:
        nome = passeggeri_repo.get_by_id(current_user.get_id()).nome
    
    if request.method == 'POST':
        tipo_viaggio = request.form.get('tipo', '')
        partenza = request.form.get('partenza', '')
        arrivo = request.form.get('arrivo', '')
        biglietto = request.form.get('biglietto', '')

        data_partenza = request.form.get('dataPartenza', '')
        data_ritorno = request.form.get('dataRitorno') if tipo_viaggio == 'andata-ritorno' else ''

        return redirect(url_for('trip', da=partenza, a=arrivo, dataP=data_partenza, dataR=data_ritorno, biglietto=biglietto))
    
    viaggi_repo = ViaggiRepository()
    partenze = viaggi_repo.get_list_partenze()
    arrivi = viaggi_repo.get_list_arrivi()

    if nome != "":
        return render_template('./public_html/home.html', user=nome, partenze=partenze, arrivi=arrivi)
    return render_template('./public_html/home.html', partenze=partenze, arrivi=arrivi)

@app.route('/trip', methods=['GET', 'POST'])
def trip():
    oper = getParam('oper')
    passeggeri_repo = PasseggeriRepository()
    nome = passeggeri_repo.get_by_id(current_user.get_id()).nome
    
    function_actions()
    if oper is None:
        return render_template('./public_html/trip.html', user=nome)
    else:
        return function_actions()

@app.route('/admin_settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    option = getParam("oper")
    compagnie_repo = CompagnieRepository()
    nome = compagnie_repo.get_by_id(current_user.get_id()).nome
    
    if option is None:
        return render_template('./public_html/admin_settings.html', compagnia=nome)
    else:
        return function_actions()



@app.route('/gestione_compagnia', methods=['GET', 'POST'])
@login_required
def gestione_compagnia():
    option = getParam("oper")
    compagnie_repo = CompagnieRepository()
    nome = compagnie_repo.get_by_id(current_user.get_id()).nome

    if option is None:
        return render_template('./public_html/gestione_compagnia.html', compagnia=nome)
    else:
        return function_actions()


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return 'You are already authenticated'

    passeggeri_repo = PasseggeriRepository()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remind = request.form.get('remind_me') != None
        
        if passeggeri_repo.validate_password(email, password):
            user = passeggeri_repo.get_by_email(email)
            custom_login_user(user, remember = remind )
            return redirect('/')
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            return redirect('/user_login')
        
    return render_template('public_html/login.html')


@app.route('/authorized_user_login', methods=['GET', 'POST'])
def authorized_user_login():
    if current_user.is_authenticated and ( isinstance(current_user,CompagnieRepository) or isinstance(current_user,DipendentiClass)):
        return 'You are already authenticated'

    option = getParam("oper")

    if option is None:
        return render_template('public_html/authorized_user_login.html')
    else:
        return function_actions()

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    passeggeri_repo = PasseggeriRepository()
    if request.method == 'POST':
        #Informazioni principali passeggero
        email = request.form['email']
        password = request.form['password']
        nome = request.form['nome']
        cognome = request.form['cognome']
        prefisso = request.form['prefisso']
        tel = request.form['tel'].replace(' ', '')
        nascita = request.form['nascita']
        saldo = 0.0

        #Indirizzo passeggero
        via = request.form['via']
        civico = request.form['civico']
        cod_postale = int(request.form['cod_postale'])
        citta = request.form['citta']
        paese = request.form['paese']

        if passeggeri_repo.get_by_email(email):
            flash('A user with this mail already exists.', 'danger')
        else:
            passeggeri_repo.add(email, generate_password_hash(password), nome, cognome, prefisso+tel, nascita, saldo, via, civico, cod_postale, citta, paese)
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('home'))
    return render_template('public_html/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route('/mytriviaggi', methods=['GET', 'POST'])
@login_required
def personal_area():
    oper = getParam("oper")
    nome = PasseggeriRepository().get_by_id(current_user.get_id()).nome

    if oper is None: 
        if not current_user.is_authenticated:
            return redirect(url_for(login_user))
        
        return render_template("public_html/personal_area.html", user=nome)
    else:
        return function_actions()

def function_actions():
    target = getParam("fun")
    action = getParam("oper")

    # datatable standard

    draw = getParam('draw')
    start = getParam('start')  # offset
    length = getParam('length')  # page size
    search_value = getParam('search[value]')

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
                                      )

        elif action == "getAllDatatable":
            return compagnie_repo.get_datatable(draw,start,length,search_value)
        elif action == "getById":
            return compagnie_repo.get_by_id(getParam("id_compagnia"))
        elif action == "get_for_select":
            return compagnie_repo.get_all()
        elif action == "edit":
            return compagnie_repo.update(
                                         compagnie_id=getParam("id_compagnia"),
                                         email=getParam("email"),
                                         tel=getParam("tel"),
                                         nome=getParam("nome"),
                                         civico=getParam("civico"),
                                         via=getParam("via"),
                                         citta=getParam("citta"),
                                         cod_postale=getParam("cod_postale"),
                                         paese=getParam("paese"),)
        elif action == "login":

            if compagnie_repo.validate_password(email=getParam("email"),
                                                password=getParam("password")):
                user = compagnie_repo.get_by_email(email=getParam("email"))
                custom_login_user(user, remember = getParam("remind_me") )

                return jsonify(success=True, next_url=url_for("gestione_compagnia"))
            else:
                return jsonify(success=False, message="Invalid credentials")

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
        elif action == "edit":
            return aerei_repo.update(
                id_aereo= getParam("id_aereo"),
                capacita =getParam("capacita"),
                modello=getParam("modello"),
                consumoMedio=getParam("consumoMedio"),
                dimensione=getParam("dimensione"),
                id_compagnia=getParam("id_compagnia")
            )
        elif action == "get_for_select":
            # permessi admin TODO
            return aerei_repo.get_all()
        elif action == "get_for_select_compagnia":
            check_permissions([CompagnieClass])
            return aerei_repo.get_all(id_compagnia = current_user.get_id())


    elif target == "dipendenti":

        dipendenti_repo = DipendentiRepository()

        if action == "add":
            return dipendenti_repo.add(email=getParam("email"),
                                      password=getParam("password"),
                                      tel=getParam("tel"),
                                      nome=getParam("nome"),
                                      cognome=getParam("cognome"),
                                      ruolo=getParam("ruolo"),
                                      id_compagnia=getParam("id_compagnia"),
                                      )

        elif action == "getAllDatatable":
            return dipendenti_repo.get_datatable(draw,start,length,search_value,id_compagnia = getParam("id_compagnia"))
        elif action == "getById":
            return dipendenti_repo.get_by_id(getParam("id_dipendente"))
        elif action == "get_for_select":
            return dipendenti_repo.get_all()
        elif action == "edit":
            return dipendenti_repo.update(
                dipendente_id=getParam("id_dipendente"),
                email=getParam("email"),
                tel=getParam("tel"),
                nome=getParam("nome"),
                cognome=getParam("cognome"),
                ruolo=getParam("ruolo"),
                id_compagnia=getParam("id_compagnia")
            )
    elif target == "aereoporti":
        aereoporti_repo = AereoportiRepository()
        if action == "add":
            return aereoporti_repo.add(id_aereoporto = getParam("id_aereoporto"),
                                       nome = getParam("nome"),
                                       civico = getParam("civico"),
                                       via = getParam("via"),
                                       cod_postale = getParam("cod_postale"),
                                       citta = getParam("citta"),
                                       paese = getParam("paese"))
        elif action == "getAllDatatable":
            return aereoporti_repo.get_datatable(draw,start,length,search_value)
        elif action == "getById":
            return aereoporti_repo.get_by_id(getParam("id_aereoporto"))
        elif action == "get_for_select":
            return aereoporti_repo.get_all()
        elif action == "edit":
            return aereoporti_repo.update(
                id_aereoporto=getParam("id_aereoporto"),
                nome = getParam("nome"),
                civico = getParam("civico"),
                via = getParam("via"),
                cod_postale = getParam("cod_postale"),
                citta = getParam("citta"),
                paese = getParam("paese")
            )
    elif target == "personalArea":
        passeggeri_repo = PasseggeriRepository()

        if action == "getCurrentInfo":
            return passeggeri_repo.get_by_id_json(current_user.get_id())

        if action == "update":
            element = getParam("element")
            val = getParam("value")
            id_passeggero = current_user.get_id()
            pk_field = passeggeri_repo.pk_field
            res = False
            
            if element == "nome_cognome":
                nome = val.split(" ")[0]
                cognome = val.split(" ")[1]
                res = passeggeri_repo.update(id_passeggero, pk_field, nome=nome, cognome=cognome)
            
            elif element == "email":
                res = passeggeri_repo.update(id_passeggero, pk_field, email=val)
            elif element == "password":
                password = generate_password_hash(val)
                res = passeggeri_repo.update(id_passeggero, pk_field, password=password)
            elif element == "telefono":
                tel = val.replace(' ', '')
                res = passeggeri_repo.update(id_passeggero, pk_field, tel=tel)
            elif element == "nascita":
                res = passeggeri_repo.update(id_passeggero, pk_field, nascita=val)
            elif element == "indirizzo":
                civico = val.split(' ')[0]
                via = val.split(' ')[1]
                citta = val.split(' ')[2]
                cod_postale = val.split(' ')[3]
                paese = val.split(' ')[4]
                res = passeggeri_repo.update(id_passeggero, pk_field,  
                                                civico=civico,
                                                via=via,
                                                citta=citta,
                                                cod_postale=cod_postale,
                                                paese=paese
                                            )
            return jsonify({ 'success': res })

    elif target == "tickets":
        biglietti_repo = BigliettiRepository()

        if action == "getTickets":
            return biglietti_repo.get_by_user(current_user.get_id())
    elif target == "viaggi":
        viaggi_repo = ViaggiRepository()
        if action == "add":
            return viaggi_repo.add(sosta = getParam("sosta"),
                                   durata= getParam("durata"),
                                   id_aereoporto_partenza= getParam("id_aereoporto_partenza"),
                                   id_aereoporto_arrivo= getParam("id_aereoporto_arrivo"),
                                   sconto_biglietto= getParam("sconto_biglietto"),
                                   data_partenza= getParam("data_partenza"),
                                   orario_partenza= getParam("orario_partenza"))
        elif action == "getAllDatatable":
            return viaggi_repo.get_datatable(draw,start,length,search_value)
        elif action == "getById":
            return viaggi_repo.get_by_id(getParam("id_viaggio"))
        elif action == "get_for_select":
            return viaggi_repo.get_all()
        elif action == "edit":
            return viaggi_repo.update(
                id_viaggio=getParam("id_viaggio"),
                sosta = getParam("sosta"),
                durata= getParam("durata"),
                id_aereoporto_partenza= getParam("id_aereoporto_partenza"),
                id_aereoporto_arrivo= getParam("id_aereoporto_arrivo"),
                sconto_biglietto= getParam("sconto_biglietto"),
                data_partenza= getParam("data_partenza"),
                orario_partenza= getParam("orario_partenza")
            )
    elif target == "voli":
        voli_repo = VoliRepository()
        if action == "add":
            return voli_repo.add(
                comandante=getParam("comandante"),
                ritardo=getParam("ritardo"),
                id_viaggio=getParam("id_viaggio"),
                id_aereo =getParam("id_aereo"),
                id_aereoporto_partenza= getParam("id_aereoporto_partenza"),
                id_aereoporto_arrivo=getParam("id_aereoporto_arrivo"))
        elif action == "getAllDatatable":
            return voli_repo.get_datatable(draw,start,length,search_value,getParam("id_viaggio"))
        elif action == "getById":
            return voli_repo.get_by_id(getParam("id_volo"))
        elif action == "get_for_select":
            return voli_repo.get_all()
        elif action == "edit":
            return voli_repo.update(
                id_volo=getParam("id_volo"),
                comandante=getParam("comandante"),
                ritardo=getParam("ritardo"),
                id_viaggio=getParam("id_viaggio"),
                id_aereo =getParam("id_aereo"),
                id_aereoporto_partenza= getParam("id_aereoporto_partenza"),
                id_aereoporto_arrivo=getParam("id_aereoporto_arrivo")
            )
        elif action == "add_from_json":
            return voli_repo.add_from_json(getParam("voli_json"))
        elif action == "delete_all":
            return voli_repo.delete_all(getParam("id_viaggio"))
    elif target == "trips":
        viaggi_repo = ViaggiRepository()

        if action == "getSelectedTrips":
            partenza = getParam('da')
            destinazione = getParam('a')
            dataP = getParam('dataP')
            dataR = getParam('dataR')
            biglietto = getParam('biglietto')

            return viaggi_repo.get_viaggi(partenza=partenza, destinazione=destinazione, dataP=dataP, dataR=dataR, biglietto=biglietto)

    return jsonify({"error": "Invalid action"}), 400


if __name__ == '__main__':
    app.run(debug=True)