from flask import Flask, request, jsonify
from nucleidechartlib import load_elements_csv, gen_chart

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generar_tabla():
    data = {}
    if request.json:
        data = request.json
    elements = load_elements_csv(data['ruta_archivo'])
    gen_chart(elements, output="output.svg", config={}, style="None")
    return jsonify({"message": "Tabla generada con éxito", "output": "output.png"})

if __name__ == '__main__':
    app.run(debug=True)
