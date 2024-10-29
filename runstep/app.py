from flask import Flask, jsonify, request
from runstep.simpath import simpath
from runstep.runstep import lj_info,lj_init
import os
import glob
import copy
app = Flask(__name__)

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
@app.route('/', methods=['GET'])
def get_simulations_html():
    simulations = glob.glob(os.path.join(simpath(), '*'))
    simulations = [os.path.basename(sim) for sim in simulations]
    # sort simulations
    simulations.sort(reverse=True)
    sim_init = [lj_init(sim) for sim in simulations]

    sim_info = []
    for sim in simulations:
        try:
            si = lj_info(sim)
        except:
            si = {}
        sim_info.append(si)

    # compute the size of the simulation in MB
    size = []
    for sim in simulations:
        size.append(sum(os.path.getsize(f) for f in glob.glob(os.path.join(simpath(), sim)) if os.path.isfile(f)))
    size = [s/1e6 for s in size]
    for init,s in zip(sim_init,size):
        init["metadata"]["size"] = s
    # put error is {} in sim_init

    for init,info in zip(sim_init,sim_info):
        if not info:
            init["metadata"]["error_msg"] = "No info file found"

        else:
            init["metadata"]["error_msg"] = "The simulation finished successfully"
            init["metadata"]["error"] = info["error"]
            init["metadata"]["elapsed"] = info["elapsed"]
            init["metadata"]["final_time"] = info["final_time"]
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
        metadata.pop('size')
        metadata.pop('elapsed')
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
        html += f"<td><button onclick='deleteSim(\"{simulation}\")'>Eliminar simulación</button></td>"

        html += "</tr>"

        # add delete button



    html += "</tbody></table>"
    
    
    # Agregar un botón para eliminar la simulación
    script = """
    <script>
        function deleteSim(sim) {
            fetch('/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({sim: sim})
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
        }
    </script>
    """
    html += script
    return html


# delete sim
@app.route('/delete', methods=['POST'])
def delete_sim():
    data = request.json
    sim = data['sim']
    sim = os.path.join(simpath(), sim)
    if os.path.exists(sim):
        os.system(f'rm -rf {sim}')
        return jsonify({'message': 'Simulation deleted', 'status': 'success'})
    else:
        return jsonify({'message': 'Simulation not found', 'status': 'error'})

def main():
    app.run(debug=True)
