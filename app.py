from flask import Flask, render_template, send_file, jsonify

import csv
import io
from datetime import datetime

app = Flask(__name__)

dados = [
    {'id': 'XL45C', 'navio': 'Navio A', 'embarque': '0', 'desembarque': '0', 'dock': 'A1', 'data': '2024-11-01'},
    {'id': 'OSK54', 'navio': 'Navio B', 'embarque': '0', 'desembarque': '0', 'dock': 'A2', 'data': '2024-10-02'},
    {'id': 'AIK45', 'navio': 'Navio C', 'embarque': '0', 'desembarque': '0', 'dock': 'A3', 'data': '2024-08-03'},
    {'id': 'QW12E', 'navio': 'Navio D', 'embarque': '0', 'desembarque': '0', 'dock': 'B1', 'data': '2024-09-15'},
    {'id': 'RT56Y', 'navio': 'Navio E', 'embarque': '0', 'desembarque': '0', 'dock': 'B2', 'data': '2024-07-22'},
    {'id': 'YU78H', 'navio': 'Navio F', 'embarque': '0', 'desembarque': '0', 'dock': 'B3', 'data': '2024-06-30'},
    {'id': 'DF34G', 'navio': 'Navio G', 'embarque': '0', 'desembarque': '0', 'dock': 'C1', 'data': '2024-05-10'},
    {'id': 'GH89J', 'navio': 'Navio H', 'embarque': '0', 'desembarque': '0', 'dock': 'C2', 'data': '2024-04-20'},
    {'id': 'JK12M', 'navio': 'Navio I', 'embarque': '0', 'desembarque': '0', 'dock': 'C3', 'data': '2024-03-05'},
    {'id': 'LP34N', 'navio': 'Navio J', 'embarque': '0', 'desembarque': '0', 'dock': 'D1', 'data': '2024-02-14'},
    {'id': 'ZX56O', 'navio': 'Navio K', 'embarque': '0', 'desembarque': '0', 'dock': 'D2', 'data': '2024-01-01'},
    {'id': 'CV78P', 'navio': 'Navio L', 'embarque': '0', 'desembarque': '0', 'dock': 'D3', 'data': '2023-12-12'},
]

@app.route('/')
def index():
    video_data = {
        'title': 'CAM-01',
        'url': 'vxqQyW4b9jA'
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
                    background-color: #004A2E;
                    color: #333;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    }

                    .logo img {
                    max-width: 100px;
                    height: auto;
                    }

                    .logo {
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    justify-content: center;
                    }

                    .name-logo {
                    margin-left: 8px;
                    color: #004A2E;
                    font-weight: lighter;
                    font-size: 2.3em;
                    letter-spacing: -2px;
                    line-height: 30px;
                    }
                    .container {
                    text-align: center;
                    background-color: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    }
                    h1 {
                    color: #004A2E;
                    }
                    button {
                    background-color: #004A2E;
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
                    <div class="logo">
                        <img width="80px" src="https://raw.githubusercontent.com/ian-cunha/suape-vision-py/refs/heads/main/src/logo.png" alt="SUAPE Vision">
                        <h1 class="name-logo"><b>SUAPE</b><br />Vision</h1>
                    </div>
                    <h1>Bem-vindos, API SUAPE Vision!</h1>
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
