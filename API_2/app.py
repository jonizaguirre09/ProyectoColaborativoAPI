import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import openai
import json

app = Flask(__name__)
app.secret_key = 'adkfnasñldkfñlavsjdñfljadbsklfjavjdsfskldjf'  # Cambia esto por una clave segura
openai.api_key = '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'  # Reemplaza por tu clave de OpenAI

# Configuración de flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

USER_FILE = 'usuarios.txt'
PELICULAS_FILE = 'peliculas.json'
PREFERENCIAS_FILE = 'preferencias_usuarios.json'


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


def cargar_peliculas():
    with open(PELICULAS_FILE, 'r', encoding='utf-8') as f:
        peliculas_data = json.load(f)
    return peliculas_data['peliculas']

def cargar_titulo_peliculas():
    with open(PELICULAS_FILE, 'r', encoding='utf-8') as f:
        peliculas_data = json.load(f)
    peliculas_titulos = [pelicula['titulo'] for pelicula in peliculas_data['peliculas']]
    return peliculas_titulos


def cargar_preferencias(usuario):
    preferencias = {}
    if os.path.exists(PREFERENCIAS_FILE):
        with open(PREFERENCIAS_FILE, 'r', encoding='utf-8') as f:
            preferencias = json.load(f)
    return preferencias.get(usuario, [])


def guardar_preferencias(usuario, preferencias):
    all_preferencias = {}
    if os.path.exists(PREFERENCIAS_FILE):
        with open(PREFERENCIAS_FILE, 'r', encoding='utf-8') as f:
            all_preferencias = json.load(f)

    all_preferencias[usuario] = preferencias

    with open(PREFERENCIAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_preferencias, f)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


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
            return redirect(url_for('recomendadas'))
        else:
            flash('¡Usuario o contraseña incorrectos! Prueba de nuevo.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/pagina_resgistro')
def pagina_registro():
    return render_template('registrar.html')


@app.route('/registrar', methods=['POST'])
def registrar():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    users = cargar_usuarios()

    if username in users:
        flash('El nombre de usuario ya existe. Por favor elige otro.', 'danger')
        return redirect(url_for('pagina_registro'))
    elif password != confirm_password:
        flash('Las contraseñas no coinciden. Por favor, vuelve a intentarlo.', 'danger')
        return redirect(url_for('pagina_registro'))
    else:
        registrar_usuario(username, password)
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Logout exitoso! Ahora puedes volver a iniciar sesión.', 'success')
    return redirect(url_for('login'))


# Página de Recomendaciones
@app.route('/recomendadas')
@login_required
def recomendadas():
    usuario = current_user.id
    preferencias_anteriores = cargar_preferencias(usuario)
    todas_peliculas = cargar_titulo_peliculas()

    if preferencias_anteriores:
        # Llamada a ChatGPT para obtener recomendaciones basadas en las preferencias
        prompt = f"Eres un recomendador de películas. En base a estas preferencias del usuario: {', '.join(preferencias_anteriores)}  elige SIEMPRE 15 películas que aparezcan ahí: {todas_peliculas}"
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cambia a gpt-4 si lo prefieres
            messages=[{"role": "user", "content": prompt}]
        )
        recomendaciones_chatgpt = respuesta['choices'][0]['message']['content'].strip().splitlines()
    else:
        # Aquí pasas un mensaje en texto plano si no hay preferencias
        recomendaciones_chatgpt = "Aún no te conozco lo suficiente como para recomendarte películas."

    return render_template('recomendadas.html', recomendaciones_anteriores=recomendaciones_chatgpt)


@app.route('/recomendacion_adicional')
@login_required
def obtener_recomendaciones_adicionales():
    usuario = current_user.id
    preferencias_anteriores = cargar_preferencias(usuario)
    todas_canciones = cargar_titulo_peliculas()

    if preferencias_anteriores:
        prompt = f"Genera un texto de recomendación en lenguaje natural recomendando algunas peliculas basadas en las preferencias del usuario: {', '.join(preferencias_anteriores)}. No incluyas ninguna de las siguientes peliculas: {', '.join(todas_canciones)}. El texto debe ser ameno y natural, y al menos me debes recomendar 3 peliculas. Y que la respuesta debe ceñirse unicamente a recomendarme esas peliculas adicionales."

        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        recomendaciones_texto = respuesta['choices'][0]['message']['content'].strip()
    else:
        recomendaciones_texto = "Aún no te conozco lo suficiente como para recomendarte películas."
    return jsonify(recomendaciones_adicionales=recomendaciones_texto)



@app.route('/todas_peliculas')
@login_required
def todas_peliculas():
    todas_peliculas = cargar_peliculas()
    return render_template('todas_peliculas.html', todas_peliculas=todas_peliculas)


@app.route('/que_te_apetece', methods=['GET', 'POST'])
@login_required
def que_te_apetece():
    if request.method == 'POST':
        genero = request.form.get('genero')
        tipoDePelicula = request.form.get('tipo')
        actoresPreferidos = request.form.get('actores')
        duracion = request.form.get('duracion')
        idioma = request.form.get('idioma')

        preferencias = [genero, tipoDePelicula, actoresPreferidos, duracion, idioma]
        guardar_preferencias(current_user.id, preferencias)

        todas_peliculas = cargar_titulo_peliculas()
        prompt = f"Eres un recomendador de películas.En base a las preferencias del usuario, elige SIEMPRE 10 películas que mejor coincidan con: Género: {genero}. Tipo de película: {tipoDePelicula}. Duración de la película: {duracion}. Actores preferidos: {actoresPreferidos}. Idioma de la película: {idioma} Aquí está la lista de películas disponibles, elige peliculas que aparezcan ahí: {todas_peliculas}"
        print(prompt)
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        recomendaciones_chatgpt = respuesta['choices'][0]['message']['content'].strip().splitlines()

        return render_template('recomendadas1.html', recomendaciones_anteriores=recomendaciones_chatgpt)

    return render_template('que_te_apetece.html')




@app.route('/detalles_pelicula')
@login_required
def detalles_pelicula():
    nombre_pelicula = request.args.get('nombre')
    prompt = f"Dame los actores y una breve sinopsis de la película '{nombre_pelicula}'."

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    detalles = respuesta['choices'][0]['message']['content'].strip()

    return jsonify({'detalles': detalles})


if __name__ == '__main__':
    app.run(debug=True)
