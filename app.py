from flask import Flask, render_template, send_file
import csv
import io

app = Flask(__name__)

# Dados da planilha
planilha_data = [
    {'id': 'XL45C', 'navio': 'Navio A', 'embarque': '0', 'desembarque': '0', 'dock': 'A1', 'data': '2024-11-01'},
    {'id': 'OSK54', 'navio': 'Navio B', 'embarque': '0', 'desembarque': '0', 'dock': 'A2', 'data': '2024-10-02'},
    {'id': 'AIK45', 'navio': 'Navio C', 'embarque': '0', 'desembarque': '0', 'dock': 'A3', 'data': '2024-08-03'},
]

@app.route('/')
def index():
    # Dados do vídeo
    video_data = {
        'title': 'CAM-01',
        'url': '/static/video.mov'
    }
    return render_template('index.html', video=video_data, planilha=planilha_data)

@app.route('/download_csv')
def download_csv():
    # Criar um buffer em memória
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'navio', 'embarque', 'desembarque', 'dock', 'data'])
    writer.writeheader()
    writer.writerows(planilha_data)

    # Mover o ponteiro para o início do buffer
    output.seek(0)

    # Converter para bytes
    csv_bytes = output.getvalue().encode('utf-8')
    output.close()

    # Retornar o arquivo CSV como resposta
    return send_file(io.BytesIO(csv_bytes), mimetype='text/csv', as_attachment=True, download_name='planilha.csv')

if __name__ == '__main__':
    app.run(debug=True)
