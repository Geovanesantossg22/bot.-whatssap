
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ZAPI_INSTANCE_URL = "https://api.z-api.io/instances/3E1E0F007CC3E0BD1B7942BEA3E5411D/token/CDDA84AC78D7C028AB054E15/send-text"
GEMINI_API_KEY = os.getenv("AIzaSyBb65yaxUjzQ8GeMR6-CLbRGzmumDXWBo0")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    try:
        mensagem = data['message']['body']
        numero = data['message']['from']

        print(f"Recebido de {numero}: {mensagem}")

        resposta = gerar_resposta_ia(mensagem)
        enviar_mensagem_whatsapp(numero, resposta)

    except Exception as e:
        print("Erro no processamento:", e)

    return jsonify({"status": "ok"})

def gerar_resposta_ia(mensagem_usuario):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [{"text": mensagem_usuario}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Desculpe, algo deu errado com a IA."

def enviar_mensagem_whatsapp(numero, mensagem):
    payload = {
        "phone": numero,
        "message": mensagem
    }
    response = requests.post(ZAPI_INSTANCE_URL, json=payload)
    print("Mensagem enviada:", response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
