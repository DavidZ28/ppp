from flask import Flask, render_template, request
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def index():
    return render_template("index.html")


def handle_request(prompt):
    if request.method == 'POST':
        requirement = request.form.get('requirement')
        file = request.files.get('file')

        if requirement and file:
            err = 'Solo texto o archivo, no ambos.'
            return render_template('index.html', error=err)
        
        elif not requirement and not file:
            err = 'Te falta poner algo.'
            return render_template('index.html', error=err)

        file_content = ""
        if file:
            file_content = file.read().decode('utf-8')
        
        content_text = requirement if requirement else file_content
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{prompt} {content_text}"
                        }
                    ]
                }
            ]
        }
        
        url = app.config.get('URL_API') + app.config.get('API_KEY')
        
        try: 
            response = requests.post(url, json=data)
            response_data = response.json()
            return render_template('index.html', response=response_data)
        
        except requests.exceptions.RequestException as e:
            return f'Error al conectar con la API: {str(e)}'


@app.route("/review", methods=["POST"])
def review():
    prompt = "De forma muy simple, verifica si esto es un requisito de software:"
    return handle_request(prompt)

@app.route("/analyze", methods=["POST"])
def analyze():
    prompt = ("De forma muy simple, resumida y teniendo en cuenta los criterios 'INVEST' (Independiente, Negociable, Valiosa, Estimable, Pequeña y Comprobable, Por favor proporciona retroalimentación sobre cada uno de estos aspectos para la historia. HISTORIA DE USUARIO: ")
    return handle_request(prompt)

@app.route("/verify", methods=["POST"])
def verify():
    prompt = ("De forma muy simple, resumida y teniendo en cuenta  los criterios (Claridad, Integridad, Precisión, Relevancia, Formato),Verifica si este es un informe de gestión de software adecuado. INFORME:")
    return handle_request(prompt)


if __name__ == "__main__":
    app.run(debug=True, host=app.config.get("HOST"), port=app.config.get("PORT"))