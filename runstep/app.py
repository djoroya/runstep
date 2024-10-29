from flask import Flask, jsonify, request
from runstep.simpath import simpath
from runstep.runstep import lj_init
import os
import glob
import copy
app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return "¡Bienvenido a la API básica en Flask!"

# Ruta de ejemplo que devuelve datos en formato JSON
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hola, este es un ejemplo de datos JSON",
        "status": "success",
        "data": [1, 2, 3, 4, 5]
    }
    return jsonify(data)

# Ruta para recibir datos mediante POST
@app.route('/simulations', methods=['GET'])
def get_simulations():
    simulations = glob.glob(os.path.join(simpath(), '*'))
    return jsonify(simulations)

# Vista de simulaciones html
@app.route('/simulations/html', methods=['GET'])
def get_simulations_html():
    simulations = glob.glob(os.path.join(simpath(), '*'))
    simulations = [os.path.basename(sim) for sim in simulations]
    sim_init = [lj_init(sim) for sim in simulations]

    # Generar el HTML para la tabla
    html = "<h1>Simulaciones</h1>"
    html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    html += "<thead><tr><th>Simulación</th><th>Función</th><th>Metadata</th><th>Otros Datos</th></tr></thead>"
    html += "<tbody>"

    for isi, simulation in zip(sim_init, simulations):
        isi = copy.deepcopy(isi)
        fun = isi.pop('function')
        metadata = isi.pop('metadata')

        # Crear fila de tabla para cada simulación
        html += "<tr>"
        html += f"<td><strong>{simulation}</strong></td>"
        html += f"<td>{fun}</td>"

        # Metadata como una lista en una celda
        metadata_html = "<ul>"
        for key, value in metadata.items():
            metadata_html += f"<li><strong>{key}</strong>: {value}</li>"
        metadata_html += "</ul>"
        html += f"<td>{metadata_html}</td>"

        # Otros datos en la celda final
        other_data_html = "<ul>"
        for key, value in isi.items():
            other_data_html += f"<li><strong>{key}</strong>: {value}</li>"
        other_data_html += "</ul>"
        # html += f"<td>{other_data_html}</td>"

        html += "</tr>"

    html += "</tbody></table>"
    return html



def main():
    app.run(debug=True)
