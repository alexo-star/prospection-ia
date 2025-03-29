from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Assure-toi que cette variable est bien définie sur Render
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prospect', methods=['POST'])
def prospect():
    # Récupérer les données envoyées en JSON
    data = request.get_json()  
    secteur = data.get('secteur')
    localisation = data.get('localisation')

    # Créer le prompt
    prompt = f"Génère une liste de 10 prospects dans le secteur '{secteur}' à '{localisation}' qui pourraient avoir besoin d'un outil d'automatisation de prospection IA."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data_to_send = {
        "model": "gpt-3.5-turbo",  # Utilisation d'un modèle générique
        "messages": [
            {"role": "system", "content": "Tu es un expert en prospection B2B."},
            {"role": "user", "content": prompt}
        ]
    }

    # Afficher les données envoyées pour débogage
    print("Données envoyées à l'API Groq :", data_to_send)

    try:
        # Effectuer la requête API
        response = requests.post(GROQ_URL, headers=headers, json=data_to_send)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content']
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
