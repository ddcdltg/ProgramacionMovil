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
    # Primera sección: Reglas de la materia
    "camara_reglas": {
        "titulo": "La Cámara de las Reglas",
        "contenido": """
        <h3>Normas de Convivencia y Asistencia</h3>
        <ul>
            <li><strong>Asistencia:</strong> Mínimo 80% de asistencia y 80% de trabajos en clase</li>
            <li><strong>Puntualidad:</strong> 10 minutos de tolerancia máximo. Si el alumno llega después de este tiempo puede permanecer en la clase, pero no se tomará la asistencia</li>
            <li><strong>Faltas a clase:</strong> Las faltas deberán estar justificadas mediante el correo institucional con un plazo máximo de 24 horas posteriores a la hora de falta en clase mediante correo del tutor (a)</li>
            <li><strong>Entregas:</strong> Las tareas y trabajos deberán subirlas al Classroom de forma individual y no se recibirán de manera extemporánea. La demora de un trabajo o tarea sin justificante y/o con justificante fuera del límite no se aceptan.</li>
            <li><strong>Honestidad académica:</strong> El plagio o copia de trabajos y/o exámenes, será condicionado a reprobar a la asignatura y se reportará al área correspondiente. Cualquier deshonestidad académica será sancionada reprobando el parcial sin derecho a examen final</li>
        </ul>
        """,
        # Lista de preguntas para evaluar esta sección
        # Cada pregunta tiene: texto, opciones de respuesta y el índice de la respuesta correcta
        "preguntas": [
            {
                "pregunta": "¿Cuál es el porcentaje mínimo de asistencia requerido?",
                "opciones": ["70%", "80%", "90%", "100%"],
                "correcta": 1  # La respuesta correcta es la opción en índice 1 (80%)
            },
            {
                "pregunta": "¿Cuántos minutos de tolerancia hay para llegar a clase?",
                "opciones": ["5 minutos", "10 minutos", "15 minutos", "No hay tolerancia"],
                "correcta": 1  # La respuesta correcta es la opción en índice 1 (10 minutos)
            }
        ]
    },
    
    # Segunda sección: Sistema de evaluación
    "oraculo_notas": {
        "titulo": "El Oráculo de las Notas",
        "contenido": """
        <h3>Porcentajes de Evaluación</h3>
        <ul>
            <li><strong>Evidencia de conocimiento:</strong> Parcial 1 y 2: 40% | Parcial 3: 10% </li>
            <li><strong>Evidencia de desempeño:</strong> Parcial 1 y 2: 20% | Parcial 3: 10% </li>
            <li><strong>Evidencia de producto:</strong> 30% para los 3 parciales </li>
            <li><strong>Proyecto Integrador:</strong> Parcial 1 y 2: 10% | Parcial 3: 50% </li>
        </ul>
        """,
        "preguntas": [
            {
                "pregunta": "¿Qué porcentaje vale el Proyecto Integrador en el Parcial 3?",
                "opciones": ["20%", "30%", "40%", "50%"],
                "correcta": 3  # Índice 3 = 50%
            },
            {
                "pregunta": "¿Qué porcentaje vale la Evidencia de desempeño en los primeros dos parciales?",
                "opciones": ["20%", "30%", "40%", "50%"],
                "correcta": 0  # Índice 0 = 20%
            }
        ]
    },
    
    # Tercera sección: Objetivos de la materia
    "skills": {
        "titulo": "Skills a Desbloquear",
        "contenido": """
        <h3>Objetivo General</h3>
        <p>Desarrollará aplicaciones móviles mediante lenguajes de programación, entornos de
        desarrollo, diseño de interfaces de usuario, arquitecturas, patrones de diseño y herramientas de
        programación móvil</p>
        
        <h3>Objetivo Particular</h3>
        <ul>
            <li>Soluciones tecnológicas multiplataforma de software web y móvil utilizando programación
            orientada a objetos, frameworks, bases de datos, estándares de calidad y diseño</li>
        </ul>
        """,
        "preguntas": [
            {
                "pregunta": "¿Cuál es una de las herramientas que se estudiarán para brindar soluciones tecnológicas?",
                "opciones": ["Navegadores", "De comunicación", "Base de Datos", "Compresor de archivos"],
                "correcta": 2  # Índice 2 = Base de Datos
            },
            {
                "pregunta": "¿Cuál de los siguientes elementos forma parte esencial del proceso de desarrollo de aplicaciones móviles?",
                "opciones": ["Patrones de diseño", "Microsoft Excel", "Adobe Photoshop", "Ninguna"],
                "correcta": 0  # Índice 0 = Patrones de diseño
            }
        ]
    },
    
    # Cuarta sección: Calendario del cuatrimestre
    "linea_tiempo": {
        "titulo": "La Línea del Tiempo",
        "contenido": """
        <h3>Fechas Clave del Cuatrimestre</h3>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #f0f0f0;">
                <th style="padding: 10px; border: 1px solid #ddd;">Fecha</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Evento</th>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">01 de junio del 2026</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Primer exámen parcial</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">06 de julio del 2026</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Segundo exámen parcial</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">10 de agosto del 2026</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Tercer exámen parcial</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">17 de agosto del 2026</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Exámen FINAL (por si reprobaste algún parcial :( )</td>
            </tr>
             <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">20 de agosto del 2026</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Fin del cuatrimestre</td>
            </tr>
        </table>
        <ul>
            <li>Intenta estar atento a las fechas importantes y esfuerzate por no reprobar :D </li>
        </ul>
        <ul>
            <li>! Para poder tener derecho a examen FINAL, debes tener al menos un parcial aprobado en la materia</li>
        </ul>
        """,
        "preguntas": [
            {
                "pregunta": "¿Cuántos exámenes parciales son?",
                "opciones": ["1", "3", "4", "5"],
                "correcta": 1  # Índice 1 = 3
            },
            {
                "pregunta": "¿Qué día es el primer exámen parcial?",
                "opciones": ["01 de junio", "05 de junio", "20 de julio", "01 de agosto"],
                "correcta": 0  # Índice 0 = 01 de junio
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
