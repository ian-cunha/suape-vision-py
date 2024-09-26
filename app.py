from flask import Flask, render_template, send_file, jsonify

import csv
import io
from datetime import datetime

app = Flask(__name__)

dados = [
    {'id': 'XL45C', 'navio': 'Navio A', 'embarque': '0', 'desembarque': '0', 'dock': 'A1', 'data': '2024-11-01'},
    {'id': 'OSK54', 'navio': 'Navio B', 'embarque': '0', 'desembarque': '0', 'dock': 'A2', 'data': '2024-10-02'},
    {'id': 'AIK45', 'navio': 'Navio C', 'embarque': '0', 'desembarque': '0', 'dock': 'A3', 'data': '2024-08-03'},
]

@app.route('/')
def index():
    video_data = {
        'title': 'CAM-01',
        'url': '/static/video.mov'
    }
    return render_template('index.html', video=video_data, planilha=dados)

@app.route('/download_csv')
def download_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'navio', 'embarque', 'desembarque', 'dock', 'data'])
    writer.writeheader()
    writer.writerows(dados)

    output.seek(0)
    csv_bytes = output.getvalue().encode('utf-8')
    output.close()

    data_primeira_entrada = dados[0]['data']
    data_formatada = datetime.strptime(data_primeira_entrada, '%Y-%m-%d').strftime('%Y%m%d')
    nome_arquivo = f'suape_vision_{data_formatada}.csv'

    return send_file(io.BytesIO(csv_bytes), mimetype='text/csv', as_attachment=True, download_name=nome_arquivo)

@app.route('/api', methods=['GET'])
def get_api_welcome():
    return '''
        <html>
            <head>
                <title>API SUAPE VISION</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #2C3E50;
                        color: #333;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .container {
                        text-align: center;
                        background-color: white;
                        padding: 40px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    }
                    h1 {
                        color: #2C3E50;
                    }
                    button {
                        background-color: #2C3E50;
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                    }
                    button:hover {
                        background-color: #333;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>API SUAPE VISION!</h1>
                    <p>Exemplos de acessos de dados:</p>
                    <button onclick="location.href='/api/dados'">Ver Todos os Dados</button>
                    <button onclick="location.href='/api/dados/id/OSK54'">Filtrar por ID (OSK54)</button>
                    <button onclick="location.href='/api/dados/data/2024-10-02'">Filtrar por Data (2024-10-02)</button>
                    <button onclick="location.href='/api/dados/id/OSK54/data/2024-10-02'">Filtrar por ID e Data</button>
                </div>
            </body>
        </html>
    '''

@app.route('/api/dados', methods=['GET'])
@app.route('/api/dados/id/<id>', methods=['GET'])
@app.route('/api/dados/data/<data>', methods=['GET'])
@app.route('/api/dados/id/<id>/data/<data>', methods=['GET'])
def get_dados(id=None, data=None):
    filtrados = dados
    if id:
        filtrados = [item for item in filtrados if item['id'] == id]
    if data:
        filtrados = [item for item in filtrados if item['data'] == data]

    return jsonify(filtrados) if filtrados else ('', 404)

if __name__ == '__main__':
    app.run()
