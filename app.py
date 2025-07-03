import datetime
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from core.UsersClass import UsersClass

app = Flask(__name__, static_folder='static')
app.secret_key = '112233'
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in


def getParam(param: str):
    if request.method == 'POST':
        # Accessing POST data
        data = request.form.get(param)
    elif request.method == 'GET':
        # Accessing GET data
        data = request.args.get(param)
    return data


@app.route('/')
@login_required
def hello_world():
    # Redirect the user to /shop
    return redirect(url_for('shop'))


@app.route('/shop')
@login_required
def shop():
    return render_template('public_html/shop.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    userController = UsersClass.UsersClass()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = userController.get_by_username(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('shop'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('public_html/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    userController = UsersClass.UsersClass()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        id_user_group = request.form['id_user_group']
        sha1 = "some_sha1_value"

        if userController.get_by_username(username):
            flash('Username already exists. Please choose another.', 'danger')
        else:
            userController.add(username, generate_password_hash(password), email, id_user_group, sha1)
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
