# Importar las librerías necesarias de Flask
from flask import Flask, render_template, request, jsonify, session
import json

# Crear la aplicación Flask
app = Flask(__name__)

# Clave secreta para manejar las sesiones de usuario de forma segura
# Las sesiones permiten guardar información del usuario entre diferentes peticiones
app.secret_key = 'aventura-programacion-movil'

# Diccionario que contiene todo el contenido de la materia
# Está dividido en 4 secciones principales
CONTENIDO = {

    "camara_reglas": {

        "titulo": "La Cámara de las Reglas",

        "preguntas": [

            {
                "pregunta": "¿Cuál es el porcentaje mínimo de asistencia requerido?",
                "opciones": ["70%", "80%", "90%", "100%"],
                "correcta": 1
            },

            {
                "pregunta": "¿Cuántos minutos de tolerancia hay para llegar a clase?",
                "opciones": [
                    "5 minutos",
                    "10 minutos",
                    "15 minutos",
                    "No hay tolerancia"
                ],
                "correcta": 1
            }
        ]
    },

    "oraculo_notas": {

        "titulo": "El Oráculo de las Notas",

        "preguntas": [

            {
                "pregunta": "¿Qué porcentaje vale el Proyecto Integrador en el Parcial 3?",
                "opciones": ["20%", "30%", "40%", "50%"],
                "correcta": 3
            },

            {
                "pregunta": "¿Qué porcentaje vale la Evidencia de desempeño en los primeros dos parciales?",
                "opciones": ["20%", "30%", "40%", "50%"],
                "correcta": 0
            }
        ]
    },

    "skills": {

        "titulo": "Skills a Desbloquear",

        "preguntas": [

            {
                "pregunta": "¿Cuál es una de las herramientas que se estudiarán para brindar soluciones tecnológicas?",
                "opciones": [
                    "Navegadores",
                    "De comunicación",
                    "Base de Datos",
                    "Compresor de archivos"
                ],
                "correcta": 2
            },

            {
                "pregunta": "¿Cuál de los siguientes elementos forma parte esencial del proceso de desarrollo de aplicaciones móviles?",
                "opciones": [
                    "Patrones de diseño",
                    "Microsoft Excel",
                    "Adobe Photoshop",
                    "Ninguna"
                ],
                "correcta": 0
            }
        ]
    },

    "linea_tiempo": {

        "titulo": "La Línea del Tiempo",

        "preguntas": [

            {
                "pregunta": "¿Cuántos exámenes parciales son?",
                "opciones": ["1", "3", "4", "5"],
                "correcta": 1
            },

            {
                "pregunta": "¿Qué día es el primer exámen parcial?",
                "opciones": [
                    "01 de junio",
                    "05 de junio",
                    "20 de julio",
                    "01 de agosto"
                ],
                "correcta": 0
            }
        ]
    }
}

# Ruta principal que carga la página de inicio
@app.route('/')
def index():
    """
    Función que maneja la página principal
    Inicializa el progreso del usuario si es su primera visita
    """
    # Verificar si el usuario ya tiene un progreso guardado en su sesión
    if 'progreso' not in session:
        # Si no existe, crear un nuevo diccionario de progreso para cada sección
        session['progreso'] = {
            'camara_reglas': {'completado': False, 'preguntas_correctas': 0},
            'oraculo_notas': {'completado': False, 'preguntas_correctas': 0},
            'skills': {'completado': False, 'preguntas_correctas': 0},
            'linea_tiempo': {'completado': False, 'preguntas_correctas': 0}
        }
    
    # Renderizar la plantilla HTML enviando el contenido y el progreso del usuario
    return render_template('index.html', contenido=CONTENIDO, progreso=session['progreso'])

# Ruta para verificar si una respuesta del usuario es correcta
@app.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    """
    Función que recibe una respuesta del usuario y verifica si es correcta
    Recibe: seccion, indice_pregunta, respuesta
    Retorna: si es correcta y cuántas preguntas correctas lleva
    """
    # Obtener los datos enviados desde el navegador en formato JSON
    data = request.get_json()
    seccion = data.get('seccion')  # Ej: "camara_reglas"
    indice_pregunta = data.get('indice_pregunta')  # Ej: 0 o 1
    respuesta = data.get('respuesta')  # Ej: 1 (índice de la opción seleccionada)
    
    # Buscar la pregunta correspondiente en el diccionario CONTENIDO
    pregunta = CONTENIDO[seccion]['preguntas'][indice_pregunta]
    
    # Comparar la respuesta del usuario con la respuesta correcta
    es_correcta = pregunta['correcta'] == respuesta
    
    # Si la respuesta es correcta, actualizar el progreso
    if es_correcta:
        # Verificar que existe la estructura de progreso en la sesión
        if 'progreso' not in session:
            session['progreso'] = {}
        if seccion not in session['progreso']:
            session['progreso'][seccion] = {'completado': False, 'preguntas_correctas': 0}
        
        # Incrementar el contador de preguntas correctas
        session['progreso'][seccion]['preguntas_correctas'] += 1
        # Marcar la sesión como modificada para que Flask la guarde
        session.modified = True
    
    # Devolver la respuesta en formato JSON al navegador
    return jsonify({
        'correcta': es_correcta,
        'preguntas_correctas': session['progreso'][seccion]['preguntas_correctas']
    })

# Ruta para marcar una sección como completada cuando se marca el checkbox
@app.route('/marcar_compromiso', methods=['POST'])
def marcar_compromiso():
    """
    Función que marca una sección como completada
    Esto desbloquea la siguiente sección
    """
    # Obtener el nombre de la sección desde el navegador
    data = request.get_json()
    seccion = data.get('seccion')
    
    # Verificar que la sección existe en el progreso del usuario
    if 'progreso' in session and seccion in session['progreso']:
        # Marcar la sección como completada
        session['progreso'][seccion]['completado'] = True
        session.modified = True
        
        # Responder con éxito
        return jsonify({'exito': True})
    
    # Si algo salió mal, responder con error
    return jsonify({'exito': False})

# Ruta para reiniciar todo el progreso del usuario
@app.route('/reiniciar')
def reiniciar():
    """
    Función que borra todo el progreso guardado
    El usuario vuelve a empezar desde cero
    """
    # Limpiar completamente la sesión del usuario
    session.clear()
    return jsonify({'exito': True})

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Ejecutar el servidor Flask
    # debug=True: muestra errores detallados y recarga automáticamente
    # host='0.0.0.0': permite acceso desde cualquier IP
    # port=5000: el servidor corre en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
