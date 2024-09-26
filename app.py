from flask import Flask, render_template, send_file, jsonify, request, redirect, url_for, session

import requests
import csv
import io
from datetime import datetime

app = Flask(__name__)

users = {
    "admin": "suape",
}

app.secret_key = 'suape'


dados = [
    {
        "id": "QW12E",
        "categoria": "New Panamax",
        "entrada": "0",
        "saida": "0",
        "dock": "A1",
        "data": "2024-09-15",
    },
    {
        "id": "RT56Y",
        "categoria": "Ultra Large Container Ship",
        "entrada": "0",
        "saida": "0",
        "dock": "A2",
        "data": "2024-07-22",
    },
    {
        "id": "YU78H",
        "categoria": "Post-Panamax",
        "entrada": "0",
        "saida": "0",
        "dock": "A3",
        "data": "2024-06-30",
    },
    {
        "id": "DF34G",
        "categoria": "Container Ship",
        "entrada": "0",
        "saida": "0",
        "dock": "A4",
        "data": "2024-05-10",
    },
    {
        "id": "GH89J",
        "categoria": "Feeder Ship",
        "entrada": "0",
        "saida": "0",
        "dock": "A1",
        "data": "2024-04-20",
    },
    {
        "id": "JK12M",
        "categoria": "General Cargo Ship",
        "entrada": "0",
        "saida": "0",
        "dock": "A2",
        "data": "2024-03-05",
    },
    {
        "id": "LP34N",
        "categoria": "Bulk Carer",
        "entrada": "0",
        "saida": "0",
        "dock": "A3",
        "data": "2024-02-14",
    },
    {
        "id": "ZX56O",
        "categoria": "Roll-on/Rollri-off",
        "entrada": "0",
        "saida": "0",
        "dock": "A4",
        "data": "2024-01-01",
    },
]


@app.route("/")
def index():
    video_data = {"title": "CAM-01", "url": "vxqQyW4b9jA"}
    return render_template("index.html", video=video_data, planilha=dados)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validação das credenciais
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("webhooks"))

        return "Credenciais inválidas. Tente novamente.", 401

    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - SUAPE Vision</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 400px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            input[type="text"], input[type="password"] {
                width: 95%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #004A2E;
                border: none;
                color: white;
                padding: 10px;
                cursor: pointer;
                width: 100%;
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
            <h1>Login</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Usuário" required>
                <input type="password" name="password" placeholder="Senha" required>
                <button type="submit">Entrar</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/api/webhooks", methods=["GET", "POST"])
def webhooks():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        webhook_url = request.form.get("webhook_url")
        payload = {"message": "Webhook enviado com sucesso!"}
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                return "Webhook enviado com sucesso!", 200
            else:
                return f"Falha ao enviar webhook: {response.text}", response.status_code
        except requests.exceptions.RequestException as e:
            return f"Erro ao enviar webhook: {e}", 500

    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Webhooks - SUAPE Vision</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            input[type="text"] {
                width: 98%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #004A2E;
                border: none;
                color: white;
                padding: 10px;
                cursor: pointer;
                border-radius: 5px;
                transition: background-color 0.3s;
                margin-top: 20px;
                width: 100%;
            }
            button:hover {
                background-color: #333;
            }
            @media (max-width: 600px) {
                button {
                    width: 100%;
                }
                .container {
                    width: 90%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gerenciador de Webhooks</h1>
            <p>Aqui você pode gerenciar seus webhooks.</p>
            <form method="post">
                <input type="text" name="webhook_url" placeholder="URL do Webhook" required>
                <button type="submit">Enviar Webhook</button>
            </form>
            <button onclick="location.href='/'">Voltar</button>
            <button onclick="location.href='/logout'">Logout</button>
        </div>
    </body>
    </html>
    """


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



@app.route("/api/guia")
def guia():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Guia de Uso da API SUAPE Vision</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #004A2E;
                font-size: 2em;
                margin-bottom: 10px;
            }
            h2 {
                color: #333;
                font-size: 1.5em;
                margin-top: 20px;
            }
            h3 {
                color: #555;
                font-size: 1.2em;
                margin-top: 15px;
            }
            pre {
                background-color: #eee;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            button {
                background-color: #004A2E;
                border: none;
                color: white;
                padding: 12px 20px;
                text-align: center;
                cursor: pointer;
                border-radius: 5px;
                transition: background-color 0.3s;
                margin-top: 20px;
                display: block;
                width: 100%;
            }
            button:hover {
                background-color: #333;
            }
            @media (max-width: 600px) {
                h1 {
                    font-size: 1.8em;
                }
                h2 {
                    font-size: 1.4em;
                }
                h3 {
                    font-size: 1.1em;
                }
                pre {
                    font-size: 14px;
                }
                button {
                    padding: 10px;
                    font-size: 16px;
                }
            }
        </style>
    </head>
    <body>

    <div class="container">
        <h1>Guia de Uso da API SUAPE Vision</h1>
        
        <h2>1. URL Base</h2>
        <p>A URL base da API é <code>/api</code>.</p>

        <h2>2. Página de Boas-Vindas</h2>
        <p><strong>GET</strong> <code>/api</code>: Exibe a página de boas-vindas da API com opções de navegação.</p>

        <h2>3. Obter Todos os Dados</h2>
        <p><strong>GET</strong> <code>/api/dados</code>: Recupera todas as entradas em formato JSON.</p>

        <h2>4. Filtrar por ID</h2>
        <p><strong>GET</strong> <code>/api/dados/id/&lt;id&gt;</code>: Substitua <code>&lt;id&gt;</code> pelo ID desejado (por exemplo, <code>/api/dados/id/GH89J</code>) para recuperar os dados daquela entrada específica.</p>

        <h2>5. Filtrar por Data</h2>
        <p><strong>GET</strong> <code>/api/dados/data/&lt;data&gt;</code>: Substitua <code>&lt;data&gt;</code> pela data desejada no formato <code>YYYY-MM-DD</code> (por exemplo, <code>/api/dados/data/2024-04-20</code>).</p>

        <h2>6. Filtrar por ID e Data</h2>
        <p><strong>GET</strong> <code>/api/dados/id/&lt;id&gt;/data/&lt;data&gt;</code>: Use este endpoint para filtrar por ID e data (por exemplo, <code>/api/dados/id/ZX56O/data/2024-01-01</code>).</p>

        <h2>Formato da Resposta</h2>
        <p>Todas as respostas serão retornadas em formato JSON. Se nenhum dado for encontrado, será retornado um erro 404.</p>

        <h2>Exemplos de Uso</h2>
        
        <h3>Usando curl</h3>
        <pre>
        curl -X GET https://suapevision.vercel.app/api/dados
        curl -X GET https://suapevision.vercel.app/api/dados/id/GH89J
        curl -X GET https://suapevision.vercel.app/api/dados/data/2024-04-20
        curl -X GET https://suapevision.vercel.app/api/dados/id/ZX56O/data/2024-01-01
        </pre>

        <h3>Usando JavaScript (Fetch API)</h3>
        <pre>
        fetch('https://suapevision.vercel.app/api/dados')
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Erro:', error));

        fetch('https://suapevision.vercel.app/api/dados/id/GH89J')
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Erro:', error));

        fetch('https://suapevision.vercel.app/api/dados/data/2024-04-20')
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Erro:', error));

        fetch('https://suapevision.vercel.app/api/dados/id/ZX56O/data/2024-01-01')
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Erro:', error));
        </pre>

        <h3>Usando Java</h3>
        <pre>
        import java.io.BufferedReader;
        import java.io.InputStreamReader;
        import java.net.HttpURLConnection;
        import java.net.URL;

        public class ApiExample {
            public static void main(String[] args) {
                try {
                    URL url = new URL("https://suapevision.vercel.app/api/dados");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");

                    BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    String inputLine;
                    StringBuffer response = new StringBuffer();

                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();

                    System.out.println(response.toString());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
        </pre>

        <p>Se precisar de mais detalhes sobre algum endpoint específico, é só avisar!</p>

        <button onclick="location.href='/'">Voltar</button>
    </div>

    </body>
    </html>
    """


@app.route("/download_csv")
def download_csv():
    output = io.StringIO()
    writer = csv.DictWriter(
        output, fieldnames=["id", "categoria", "entrada", "saida", "dock", "data"]
    )
    writer.writeheader()
    writer.writerows(dados)

    output.seek(0)
    csv_bytes = output.getvalue().encode("utf-8")
    output.close()

    data_primeira_entrada = dados[0]["data"]
    data_formatada = datetime.strptime(data_primeira_entrada, "%Y-%m-%d").strftime(
        "%Y%m%d"
    )
    nome_arquivo = f"suape_vision_{data_formatada}.csv"

    return send_file(
        io.BytesIO(csv_bytes),
        mimetype="text/csv",
        as_attachment=True,
        download_name=nome_arquivo,
    )



@app.route("/api", methods=["GET"])
def get_api_welcome():
    return """
        <html>
            <head>
                <title>API SUAPE VISION</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                        padding: 0 20px;
                        box-sizing: border-box;
                    }

                    .logo img {
                        max-width: 80px;
                        height: auto;
                    }

                    .logo {
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                        justify-content: center;
                        margin-bottom: 20px;
                    }

                    .name-logo {
                        margin-left: 8px;
                        color: #004A2E;
                        font-weight: lighter;
                        font-size: 1.8em;
                        letter-spacing: -1px;
                        line-height: 30px;
                    }

                    .container {
                        text-align: center;
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                        max-width: 600px;
                        width: 100%;
                    }

                    h1 {
                        color: #004A2E;
                        font-size: 1.5em;
                    }

                    button {
                        background-color: #004A2E;
                        border: none;
                        color: white;
                        padding: 12px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 14px;
                        margin: 4px 0;
                        cursor: pointer;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                        width: 100%;
                    }

                    button:hover {
                        background-color: #333;
                    }

                    @media (max-width: 600px) {
                        .name-logo {
                            font-size: 1.5em;
                        }

                        h1 {
                            font-size: 1.2em;
                        }

                        button {
                            padding: 10px;
                            font-size: 16px;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo">
                        <img src="https://raw.githubusercontent.com/ian-cunha/suape-vision-py/refs/heads/main/src/logo.png" alt="SUAPE Vision">
                        <h1 class="name-logo"><b>SUAPE</b><br />Vision</h1>
                    </div>
                    <h1>Bem-vindos, API SUAPE Vision!</h1>
                    <button onclick="location.href='/api/guia'">Guia de uso da API</button>
                    <button onclick="location.href='/api/webhooks'">Acessar Webhooks</button>
                    <p>Exemplos de acessos de dados:</p>
                    <button onclick="location.href='/api/dados'">Todos os Dados</button>
                    <button onclick="location.href='/api/dados/id/GH89J'">Filtrar por ID (GH89J)</button>
                    <button onclick="location.href='/api/dados/data/2024-04-20'">Filtrar por Data (2024-04-20)</button>
                    <button onclick="location.href='/api/dados/id/ZX56O/data/2024-01-01'">Filtrar por ID e Data</button>
                </div>
            </body>
        </html>
        """


@app.route("/api/dados", methods=["GET"])
@app.route("/api/dados/id/<id>", methods=["GET"])
@app.route("/api/dados/data/<data>", methods=["GET"])
@app.route("/api/dados/id/<id>/data/<data>", methods=["GET"])
def get_dados(id=None, data=None):
    filtrados = dados
    if id:
        filtrados = [item for item in filtrados if item["id"] == id]
    if data:
        filtrados = [item for item in filtrados if item["data"] == data]

    return jsonify(filtrados) if filtrados else ("", 404)

def handler(request):
    return app(request)


if __name__ == "__main__":
    app.run()
