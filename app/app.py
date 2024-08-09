from flask import Flask, request, send_file, jsonify
from nucleidechartlib import load_elements_csv, gen_chart
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generar_tabla():
    data = {}
    if request.json:
        data = request.json

    # Cargar elementos desde el archivo CSV
    elements = load_elements_csv(data['ruta_archivo'])

    config = {}

    if 'config' in data:
        config = data['config']


    style = "None"

    if 'style' in data:
        style = data['style']

    # Crear un archivo temporal en /tmp con un nombre único
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.svg', dir='/tmp')
    temp_file_path = temp_file.name
    temp_file.close()  # Cerrar el archivo para que pueda ser escrito por gen_chart

    # Generar la tabla y guardar el archivo en el archivo temporal
    gen_chart(elements, output=temp_file_path, config=config, style=style)

    # Enviar el archivo temporal como respuesta
    return send_file(temp_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
