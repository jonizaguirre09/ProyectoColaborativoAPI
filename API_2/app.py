import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
import openai

app = Flask(__name__)

app.secret_key = 'mi_clave_secreta'  # Aqui tenemos que poner una clave segura
openai.api_key = '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'  # Reemplaza por tu clave de OpenAI

@app.route('/')
def home():
    return render_template('paginaweb.html')

@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.json
    pregunta = data.get('mensaje')

    if pregunta:
        try:
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pregunta}]
            )
            respuesta_texto = respuesta['choices'][0]['message']['content'].strip()
            return jsonify({'respuesta': respuesta_texto})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No se hizo ninguna pregunta!'}), 400


if __name__ == '__main__':
    app.run(debug=True)
