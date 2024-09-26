import requests
from PIL import Image, ImageDraw
import io

# Função para desenhar um círculo ao redor do container
def draw_bounding_box(image, bounding_box):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    # Calcula as coordenadas da caixa delimitadora
    left = bounding_box['left'] * width
    top = bounding_box['top'] * height
    box_width = bounding_box['width'] * width
    box_height = bounding_box['height'] * height
    # Desenha um retângulo (ou círculo) ao redor do objeto
    draw.rectangle([left, top, left + box_width, top + box_height], outline="red", width=7)

# Defina a URL da API e a chave de predição
url = "https://containers-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/3d375eda-d80f-40e4-861a-a65db828951c/detect/iterations/containers/url"
headers = {
    "Prediction-Key": "c7d3e60a9e5148899457f4fd2768969b",
    "Content-Type": "application/json"
}

# Corpo da requisição com a URL da imagem
body = {
    "Url": "https://containerdesign.com.br/wp-content/uploads/2024/01/alconet-1-4.jpg"
}

# Faz a requisição POST para a API
response = requests.post(url, headers=headers, json=body)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converte a resposta em JSON
    predictions = response.json()
    print(predictions)

    # Carrega a imagem original
    image_url = body['Url']
    image_response = requests.get(image_url)
    image = Image.open(io.BytesIO(image_response.content))

    # Itera sobre as previsões e desenha ao redor de containers detectados
    for prediction in predictions.get("predictions", []):
        if prediction.get("tagName").lower() == "container" and prediction.get("probability") > 0.5:
            print(f"Container detectado com probabilidade de {prediction.get('probability'):.2%}")
            draw_bounding_box(image, prediction.get("boundingBox"))

    # Exibe a imagem com os containers circundados
    image.show()
else:
    print(f"Falha na requisição: {response.status_code}")
    print(response.text)