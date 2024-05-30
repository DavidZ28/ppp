from flask import Flask, render_template , jsonify , request
import requests 
from config import Config


app=Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/review",methods=['POST'])
def review():
    if request.method == 'POST':
        requirement = request.form['requirement']

        
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"De forma muy simple, resumida y teniendo en cuenta 'Quién, Qué, Cómo', Verifica si esto es un requisito de software: {requirement}"
                        }
                    ]
                }
            ]
        }
        

        url = app.config.get('URL_API')+app.config.get('API_KEY')
        
        try: 
            
            response = requests.post(url,json=data)
            response_data = response.json()
            return render_template('index.html',response=response_data)
        
        except requests.exceptions.RequestException as e:
            return f'Error al conectar con la API de Gemini: {str(e)}'

"""@app.route("/r3vi3w",methods=['POST'])
def r3vi3w():
    if request.method == 'POST':
        gestion = request.form['gestion']

        
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"De forma muy simple, resumida y teniendo en cuenta 'Quién, Qué, Cómo', Verifica si esto es una gestion de software: {gestion}"
                        }
                    ]
                }
            ]
        }
        

        url = app.config.get('URL_API')+app.config.get('API_KEY')
        
        try: 
            
            response = requests.post(url,json=data)
            response_data = response.json()
            return render_template('index.html',response=response_data)
        
        except requests.exceptions.RequestException as e:
            return f'Error al conectar con la API de Gemini: {str(e)}'"""







if __name__=='__main__':
    app.run(debug=True, host=app.config.get('HOST'), port=app.config.get('PORT'))
   

