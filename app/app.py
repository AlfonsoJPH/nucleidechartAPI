from flask import Flask, request, send_file, jsonify
from nucleidechartlib import load_elements_csv, gen_chart
import tempfile
import json


app = Flask(__name__)

default_source_file = "assets/source.csv"
@app.route('/', methods=['POST'])
def generar_tabla():

    source_file = default_source_file

    if 'source' in request.files:
        temp_source_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', dir='/tmp')
        temp_source_file.write(request.files['source'].read())
        temp_source_file_path = temp_source_file.name
        temp_source_file.close()  # Cerrar el archivo para que pueda ser escrito por gen_chart
        source_file = temp_source_file_path



    # Cargar elementos desde el archivo CSV
    elements = load_elements_csv(source_file)

    config = {}

    if 'config' in request.files:
        json_file = request.files['config']

        config = json.load(json_file)
    else:
        if 'division' in request.fields and 'detail' in request.fields:
            config_name=request.fields['division']+'_'+request.fields['detail']



    style = "None"

    if 'style' in request.files:
        style = request.files['style']

    # Crear un archivo temporal en /tmp con un nombre único
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.svg', dir='/tmp')
    temp_file_path =temp_file.name
    temp_file.close()  # Cerrar el archivo para que pueda ser escrito por gen_chart

    # Generar la tabla y guardar el archivo en el archivo temporal
    gen_chart(elements, output=temp_file_path, config=config, style=style)

    print("Created chart "+temp_file_path)
    # Enviar el archivo temporal como respuesta
    return send_file(temp_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
