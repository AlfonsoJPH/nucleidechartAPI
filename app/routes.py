from flask import Blueprint, request, jsonify
import nucleidchartlib

api = Blueprint('api', __name__)

@api.route('/generar_tabla', methods=['POST'])
def generar_tabla():
    configuracion = request.json
    tabla = nucleidchartlib.generar_tabla(configuracion)
    return jsonify(tabla)
