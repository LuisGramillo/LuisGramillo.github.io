# app.py
import uuid
import os
import pandas as pd
# importing sys
import sys
 

from controllers.main_controller import ControladorPrincipal
from http import HTTPStatus
from os.path import basename
from flask import Flask, render_template, request, url_for, send_file, redirect

app = Flask(__name__)


# Directorio para descargar archivos
UPLOAD_DIRECTORY = "/home/cam/Documents/Codigo/python/Reto_techo/PruebaWeb/uploads"
DOWNLOAD_DIRECTORY = "/home/cam/Documents/Codigo/python/Reto_techo/PruebaWeb/downloads"


@app.route('/', methods=['GET'])
def index():
    return render_template('main_window.html')


@app.route("/downloads/<filename>", methods=["GET"])
def get_downloads(filename):
    file_location = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    return send_file(file_location, as_attachment=True)


@app.route('/procesar', methods=['POST'])
def procesar():
    df = request.files['archivo']
    if not df:
        return {
            "status": HTTPStatus.BAD_REQUEST.value,
            "msg": f"{HTTPStatus.BAD_REQUEST.phrase}: No se ha enviado ningún archivo."
        }
    else:
        try:
            # df = pd.read_excel(archivo, header=0)
            # filename = secure_filename(df.filename)
            file_location = f"{UPLOAD_DIRECTORY}/{uuid.uuid1()}.xlsx"
            print("File Location:", file_location)  # Debugging statement
            df.save(file_location)
            processed_file_location = os.path.join(DOWNLOAD_DIRECTORY, basename(file_location))
            print("Processed File Location:", processed_file_location)  # Debugging statement
            controlador = ControladorPrincipal()


            resultado = controlador.procesar_archivo(file_location)
            with pd.ExcelWriter(processed_file_location) as writer:
                resultado.to_excel(writer, index=False, sheet_name="Sheet1")
            
            mensaje = "El archivo se ha procesado correctamente. Puedes descargarlo desde el siguiente enlace:"
            #return redirect(url_for('resultado', mensaje=mensaje, filename=basename(processed_file_location)))
            return redirect(url_for('resultado') + f"?mensaje={mensaje}&filename={basename(processed_file_location)}")

        except Exception as e:
            return f'Error al procesar el archivo: {str(e)}'


@app.route('/resultado', methods=['GET'])
def resultado():
    mensaje = request.args.get('mensaje', '')
    filename = request.args.get('filename', '')
    if not filename:
        # Handle the case where no filename is provided, redirect to home or show an error message
        return 'Error al procesar el archivo'
    print("Mensaje:", mensaje)
    print("Filename:", filename)
    download_url = url_for('get_downloads', filename=filename)
    return render_template('resultado.html', mensaje=mensaje, download_url=download_url)



'''
@app.route('/resultado', methods=['GET'])
def resultado():
    mensaje = request.args.get('mensaje', '')
    filename = request.args.get('filename', '')
    ruta_descarga = url_for('get_downloads', filename=filename)
    return render_template('resultado.html', mensaje=mensaje, ruta_descarga=ruta_descarga)
'''

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_DIRECTORY
    app.run(debug=False)