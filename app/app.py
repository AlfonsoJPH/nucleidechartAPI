from flask import Flask, request, send_file, jsonify, send_from_directory
from nucleidechartlib import load_element_csv, load_elements_csv, gen_chart, gen_element, fix_config
import json
import uuid
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'tmp')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/gen_table/', methods=['POST'])
def generar_tabla():
    requestID = request.form.get('sessionID', uuid.uuid4().hex)
    files = request.files

    config = {}
    style = "None"

    try:
        source_file = os.path.join(UPLOAD_FOLDER, f"{requestID}.csv")
        if 'source' in files:
            with open(source_file, 'wb') as f:
                f.write(files['source'].read())
        if not os.path.exists(source_file):
            source_file = os.path.join(UPLOAD_FOLDER, 'default.csv')

        elements = load_elements_csv(source_file)

        if 'config' in files:
            config = json.load(files['config'])
            config = fix_config(config)

        if 'style' in files:
            style = files['style']

        temp_file_path = os.path.join(UPLOAD_FOLDER, f"table_{requestID}.svg")
        gen_chart(elements, output=temp_file_path, config=config, style=style)

        return send_file(temp_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/get_config/', methods=['POST'])
def check_config():
    requestID = request.form.get('sessionID', uuid.uuid4().hex)
    files = request.files

    try:
        if 'config' in files:
            config = files['config']
            config = json.load(files['config'])
            config = fix_config(config)
            config_path = os.path.join(UPLOAD_FOLDER, f"{requestID}.json")
            with open(config_path, 'w') as f:
                json.dump(config, f)
            return send_file(config_path, as_attachment=True)
        else:
            return jsonify({"error": "No config file provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/gen_element_box/', methods=['POST'])
def generar_element_box():
    requestID = request.form.get('sessionID', uuid.uuid4().hex)
    print(requestID)
    files = request.files

    element_name = request.form.get('element_box', '1H')

    try:
        source_file = os.path.join(UPLOAD_FOLDER, f"{requestID}.csv")
        if 'source' in files:
            with open(source_file, 'wb') as f:
                f.write(files['source'].read())
        if not os.path.exists(source_file):
            source_file = os.path.join(UPLOAD_FOLDER, 'default.csv')

        element = load_element_csv(source_file, element_name)

        print("element")
        config = {}
        if 'config' in files:
            config = json.load(files['config'])
            config = fix_config(config)

        temp_file_path = os.path.join(UPLOAD_FOLDER, f"box_{requestID}.svg")
        gen_element(element, temp_file_path, config)

        return send_file(temp_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400




# Ruta al archivo OpenAPI
SWAGGER_PATH = os.path.join(os.path.dirname(__file__), '../docs', 'openapi.yaml')

@app.route('/swagger.json/')
def swagger_json():
    return send_from_directory(directory='../docs', path='openapi.yaml')

@app.route('/swagger-ui/')
def swagger_ui():
    return send_from_directory(directory='../docs', path='index.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
