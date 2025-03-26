from flask import Flask, request, render_template, jsonify
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prospect', methods=['POST'])
def prospect():
    secteur = request.form.get('secteur')
    localisation = request.form.get('localisation')

    prompt = f"Génère une liste de 10 prospects dans le secteur '{secteur}' à '{localisation}' qui pourraient avoir besoin d'un outil d'automatisation de prospection IA."

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mixtral-8x7b-32768",  # ou llama3-8b si tu préfères
            "messages": [
                {"role": "system", "content": "Tu es un expert en prospection B2B."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content']
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
