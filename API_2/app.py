import json
import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import openai

app = Flask(__name__)

app.secret_key = 'mi_clave_secreta'  # Aqui tenemos que poner un clave secreta
openai.api_key = ''

# Configuración de flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

USER_FILE = 'usuarios.txt'
PELICULAS_FILE = 'peliculas.json'



def cargar_usuarios():
    usuarios = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    username, password_hash = linea.split(':')
                    usuarios[username] = password_hash.encode()
    return usuarios


def registrar_usuario(username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(USER_FILE, 'a') as f:
        f.write(f"{username}:{password_hash.decode()}\n")

# Cargar todas las películas
def cargar_peliculas():
    with open(PELICULAS_FILE, 'r') as f:
        peliculas_data = json.load(f)
    return peliculas_data['peliculas']

class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Redirigir a la página de login por defecto
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = cargar_usuarios()

        if username in users and bcrypt.checkpw(password.encode(), users[username]):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Usuario o contraseña incorrectos", 401

    return render_template('login.html')


@app.route('/pagina_registro')
def pagina_registro():
    return render_template('registrar.html')


@app.route('/registrar', methods=['POST'])
def registrar():
    username = request.form['username']
    password = request.form['password']

    users = cargar_usuarios()

    if username in users:
        return "El nombre de usuario ya existe", 400
    else:
        registrar_usuario(username, password)
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    todas_peliculas = cargar_peliculas()
    return render_template(
        'paginaWeb.html',
        todas_peliculas=todas_peliculas,
    )



if __name__ == '__main__':
    app.run(debug=True)
