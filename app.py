from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prospect', methods=['POST'])
def prospect():
    secteur = request.form.get('secteur')
    localisation = request.form.get('localisation')

    prompt = "Génère une liste de 10 prospects dans le secteur '{}' à '{}' qui pourraient avoir besoin d'un outil d'automatisation de prospection IA.".format(secteur, localisation)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en prospection B2B."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response['choices'][0]['message']['content']
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)