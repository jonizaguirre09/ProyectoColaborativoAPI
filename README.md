# ProyectoColaborativoAPI - Recomendación de Películas

Este proyecto es una aplicación web que permite a los usuarios obtener recomendaciones de películas basadas en las preferencias escogidas. Además, incluye autenticación de usuario y una integración con la API de OpenAI (versión 0.28) para mejorar la precisión en las recomendaciones.


## Tabla de Contenidos
- [Introducción](#introducción)
- [Instalación](#instalación)
- [Uso](#uso)
- [Características](#características)
- [Rutas Principales](#rutas-principales)
- [Tecnologías_Utilizadas](#tecnologías-utilizadas)
- [Licencia](#licencia)


## Introducción
Este proyecto consiste en desarrollar una aplicación web diseñada para recomendar películas a los usuarios. Para generar estas recomendaciones, la aplicación se basa en distintas preferencias y criterios como el género de la película, el tipo (acción, comedia, drama, bélica, etc), sus actores favoritos, la duración y el idioma. Debido al formulario de preferencias, se crea una buena aplicación de recomendaciones la cual se ajusta a los gustos personales. 
Además, la web de recomendaciones incluye un sistema de autentificación que permite iniciar sesión y registrarse (en el caso de no ser aún usuario) para poder guardar donde han almacenado sus preferencias los diferentes usuarios. También permite el uso de otras funciones adicionales como buscar una película concreta o ordenar la lista de películas alfabéticamente.
Este sistema de recomendación tiene integrado IA mediante la API de OpenAI. Esto influye en que todas las recomendaciones se ajusten mejor a cada usuario y sus preferencias, proporcionando así una mejor experiencia y más personalizada.


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
   En el apartado 'Todas las películas' aparece una lista de todas las películas almacenadas en la base de datos. Además, puedes ordenarlas alfabéticamente (A-Z o Z-A) o por fecha de estreno ascendentemente o descendentemente. También hay un buscador para hacer la búsqueda de una película concreta.

3. **Recomendaciones**:
   Esta dividido en dos apartados. En el primero apareceran 15 películas recomendadas en base a las preferencias del usuario (estan en la base de datos almacenadas) y además todas las películas recomendadas ahí seran obtenidas de todas las películas de la base de datos.
   En el segundo se mostrará un texto generado por ChatGPT, el cual recomendara 3 películas que no pertenecen a la base de datos y estan basadas en las preferencias del usuario. Además muestra algo de información sobre estas.
   Esta sección solo funcionará si anteriormente el usuario ha realizado bsuquedas teniendo así preferencias almacenadas. De lo contrario. aparecera un mensaje difiendonos que aún no nos conoce lo suficiente como para hacernos recomendaciones sobre las películas.

4. **Recomendaciones personalizadas**:
   En '¿Que te apetece ver hoy?' debes rellenar varios campos obligatorios (género, tipo de película) además de otros optativos (actores preferidos, duración preferida y idioma) para así obtener una lista de 10 películas ajustadas a tu gusto. Dependiendo de la precisión de la busqueda, te recomendará películas mas exáctas a las características añadidas. 
   Encima, todas las busquedas realizadas quedaran almacenadas en la base de datos para la utilizacion de futuras recomendaciones.

5. **Breve descripcion**:
   Independientemente del apartado en el que te encuentres, aparecera una losta de peliculas. Clickando sobre su titulo, se mostrara una pequeña pantalla con un texto generado por ChatGPT que incluye los actores prinicpales y una breve sipnosis de la pelicula seleccionada.

6. **Gestion de preferencias almacenadas y cuenta**:
   Los usuarios tienen la opcion de borrar todas sus preferencias almacenadas sin eliminar su cuenta.
   Si el usuario decide eliminar su cuenta, todas las preferencias almacenadas tambien se borrras automaticamente.

7. **Logout de usuarios**:
   Durate la nevagacion, los usuarios pueden cerrar sesion de su cuenta en cuanto deseen.


## Rutas Principales

1. **GET /**:
   Página principal de la aplicación.

2. **GET /login**:
   Muestra el campo de iniciar sesión (usuario y contraseña).

3. **POST /login**:
   Procesa los datos de inicio de sesión redirigiendo a la pagina de recomendaciones si es exitoso.

4. **GET /pagina_registro**:
   Muestra el campo de registrarse (usuario, contraseña y confirmar contraseña).

5. **POST /registrar**:
   Procesa los datos de registro de usuario validando que no exista ya y que las contraseñas coincidan.

6. **GET /perfil**:
   Muestra la pagina del perfil del usuario autenticado.

7. **POST /eliminar_datos**:
   Elimina unicamente las preferencias almacenadas del usuario autenticado.

8. **POST /eliminar_usuario**:
   Elimina la cuenta del usuario y todas las preferencias almacenadas anteriormente.

9. **POST /logout**:
   Cierra sesión del usuario y redirige a la pagina de login.

10. **GET /recomendadas**:
   Genera recomendaciones de películas basadas en las preferencias del usuario.

11. **GET /recomendacion_adicional**:
   Genera recomendaciones adicionales de peliculas en texto basadas en las preferencias del usuario.

12. **GET /todas_peliculas**:
   Muestra la lista de todas las películas disponibles.

13. **GET y POST /que_te_apetece**:
   Mediante un breve formulario podrás obtener 10 películas basadas en las características elegidas.

14. **GET /detalles_pelicula**:
   Clickando sobre una pelicula se muestra actores y sipnosis.


## Tecnologías Utilizadas
   Este proyecto se ha contruido con el uso de varias tecnologías:
   - Python: lenguaje principal del desarrollo de la web.
   - Flask: Framework web para manejar rutas y lógica del servidor.
   - Flask-Login: Autenticación y manejo de sesiones de usuarios.
   - bcrypt: Librería para el cifrado seguro de contraseñas.
   - API de OpenAI: Para generar recomendaciones y sinopsis de películas.
   - HTML/CSS: Para el diseño de interfaces.
   - JavaScript: Para mejorar la interactividad (formulario).
   - JSON: Para el almacenamiento y manjeo de preferencias y datos de usuario.


## Licencia
   En este proyecto se utilizan herramientas de software y bibliotecas de terceros, todas ellas con licencias que permiten su uso en proyectos personales y comerciales. 
   En primer lugar esta Flask que está licenciado bajo los términos de la licencia BSD (Berkeley Software Distribution). Esta licencia es ampliamente permisiva, permitiendo la modificación y redistribución.
   Otras bibliotecas utilizadas, como Flask-Login y bcrypt están distribuidas bajo la licencia MIT, que es a su vez igualmente permisiva para este tipo de proyectos.
   Por último tenemos la API de OpenAI que se emplea bajo los términos específicos de uso establecidos por la empresa. Asegurando que el proyecto cumple con las políticas de OpenAI, siempre respetando el propósito educativo y de entrenamiento para el que ha sido diseñado.
