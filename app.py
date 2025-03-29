from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv  # Si tu es en local

# Si tu es en local, charge le fichier .env (si tu n'utilises pas Render)
# load_dotenv()

app = Flask(__name__)

# La clé API est lue à partir de la variable d'environnement
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prospect', methods=['POST'])
def prospect():
    secteur = request.form.get('secteur')
    localisation = request.form.get('localisation')

    prompt = f"Génère une liste de 10 prospects dans le secteur '{secteur}' à '{localisation}' qui pourraient avoir besoin d'un outil d'automatisation de prospection IA."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",  # ou autre modèle que tu veux tester
        "messages": [
            {"role": "system", "content": "Tu es un expert en prospection B2B."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        response.raise_for_status()  # Vérifie si la requête a échoué
        result = response.json()['choices'][0]['message']['content']
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
