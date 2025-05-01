import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Token secreto
API_TOKEN = "e50604"hx[b9Mys/ofgc"

def verificar_token():
    token = request.headers.get("Authorization", "")
    return token == f"Bearer {API_TOKEN}"

# Pasta onde as imagens serão salvas
UPLOAD_FOLDER = 'fotos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return "API online e funcionando!"

@app.route("/upload", methods=["POST"])
def upload():
    if not verificar_token():
        return jsonify({"erro": "Não autorizado"}), 401

    pedido_id = request.form.get("pedido_id")
    if not pedido_id:
        return jsonify({"erro": "pedido_id obrigatório"}), 400

    arquivos = request.files
    if not arquivos:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    caminho_pedido = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pedido_id))
    os.makedirs(caminho_pedido, exist_ok=True)

    salvos = []
    for key, imagem in arquivos.items():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nome_arquivo = f"{key}_{timestamp}.jpg"
        caminho_completo = os.path.join(caminho_pedido, nome_arquivo)
        imagem.save(caminho_completo)
        salvos.append(nome_arquivo)

    return jsonify({"status": "sucesso", "arquivos_salvos": salvos})

@app.route("/fotos")
def listar_pedidos():
    if not verificar_token():
        return jsonify({"erro": "Não autorizado"}), 401
    try:
        pedidos = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify({"pedidos": pedidos})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/fotos/<pedido_id>")
def listar_fotos_pedido(pedido_id):
    if not verificar_token():
        return jsonify({"erro": "Não autorizado"}), 401
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pedido_id))
    if not os.path.exists(caminho):
        return jsonify({"fotos": []})
    fotos = os.listdir(caminho)
    return jsonify({"fotos": fotos})

@app.route("/fotos/<pedido_id>/<filename>")
def ver_foto(pedido_id, filename):
    if not verificar_token():
        return jsonify({"erro": "Não autorizado"}), 401
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pedido_id))
    return send_from_directory(caminho, filename)

if __name__ == "__main__":
    app.run(debug=True)
