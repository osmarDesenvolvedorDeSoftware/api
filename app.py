import os
from flask import Flask, request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Pasta onde as imagens serão salvas
UPLOAD_FOLDER = 'fotos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return "API online e funcionando!"

@app.route("/upload", methods=["POST"])
def upload():
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

if __name__ == "__main__":
    app.run(debug=True)
