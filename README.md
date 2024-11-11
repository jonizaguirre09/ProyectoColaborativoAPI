# ProyectoColaborativoAPI - Recomendación de Películas

Este proyecto es una aplicación web que permite a los usuarios obtener recomendaciones de películas basadas en el género y el tipo de entretenimiento que prefieran. Además, incluye autenticación de usuario y una integración con la API de OpenAI (versión 0.28) para mejorar la precisión en las recomendaciones.

## Tabla de Contenidos
- [Instalación](#instalación)
- [Uso](#uso)
- [Características](#características)
- [Rutas Principales](#rutas-principales)


## Instalación

1. **Clona el repositorio** desde GitHub:
    ```bash
    git clone https://github.com/jonizaguirre09/ProyectoColaborativoAPI.git
    ```
   
2. **Navega al directorio del proyecto**:
    ```bash
    cd ProyectoColaborativoAPI
    ```

3. **Crea un entorno virtual** (recomendado para aislar las dependencias):
    ```bash
    python -m venv env
    source env/bin/activate        # En MacOS/Linux
    .\env\Scripts\activate         # En Windows
    ```

4. **Instala los paquetes necesarios**:
   Ejecuta los siguientes comandos para instalar las dependencias requeridas:
   ```bash
   pip install flask              # Framework para construir aplicaciones web
   pip install flask_login        # Autenticación de usuario
   pip install bcrypt             # Para cifrar contraseñas de usuario
   pip install openai==0.28       # Cliente de OpenAI para integrar funcionalidades de IA

## Uso

1. **Ejecución de la aplicación**:
   ```bash
   python app.py
   
2. **Acceder a la aplicación**:
   ```bash
   http://127.0.0.1:5000

   
## Características

1. **Registro y Login de usuarios**:
   Permite a los usuarios no registrados anteriormente registrarse. Sin embargo, si ya estabas registrado solamente hay que iniciar sesión.

2. **Cartelera**:
   En el apartado 'Todas las películas' aparece una lista de X películas. Además puedes ordenarlas alfabeticamente (A-Z o Z-A). También puedes hacer la búsqueda de una película concreta.

3. **Recomendaciones personalizadas**:
   En '¿Que te apetece ver hoy?' debes rellenar varios campos (género, tipo de película, actores preferidos, duración preferida y idioma) para así obtener una lista de películas elegidas a tu gusto.

4. **Recomendaciones**:
   Después de realizar la primera búsqueda en el apartado '¿Que te apetece ver hoy?' saldrá una lista de películas recomendadas teniendo en cuenta los campos rellenados.


## Rutas Principales

1. **GET /**:
   Página principal de la aplicación.

2. **GET /login**:
   Muestra el campo de iniciar sesión (usuario y contraseña).

3. **POST /login**:
   Procesa los datos de inicio de sesión.

4. **GET /registrar**:
   Muestra el campo de registrarse (usuario, contraseña y confirmar contraseña).

5. **POST /registrar**:
   Procesa los datos de registro de usuario.

6. **POST /logout**:
   Cierra sesión del usuario.

7. **POST /recomendadas**:
   Genera recomendaciones de películas basadas en las preferencias del usuario.

8. **POST /todas_peliculas**:
   Muestra la lista de todas las películas.

9. **POST /que_te_apetece**:
   Mediante un breve formulario podrás obtener 10 películas basadas en las características elegidas.
