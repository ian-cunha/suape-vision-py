# import cv2

# # Função para inicializar o rastreador de objetos (usando CSRT para rastreamento robusto)
# def initialize_tracker():
#     tracker = cv2.TrackerCSRT_create()  # CSRT é robusto para rastreamento
#     return tracker

# # Função principal para rastreamento de container de navio
# def track_container_in_video(video_path):
#     # Carrega o vídeo
#     cap = cv2.VideoCapture(video_path)

#     # Verifica se o vídeo foi carregado com sucesso
#     if not cap.isOpened():
#         print("Erro ao abrir o vídeo.")
#         return

#     # Lê o primeiro frame do vídeo
#     ret, frame = cap.read()
#     if not ret:
#         print("Não foi possível ler o vídeo.")
#         return

#     # Seleciona manualmente o container (retângulo azul) no primeiro frame
#     print("Selecione a área do container no primeiro frame.")
#     bbox = cv2.selectROI("Selecione o Container", frame, fromCenter=False, showCrosshair=True)

#     # Inicializa o rastreador com a área selecionada (bounding box)
#     tracker = initialize_tracker()
#     tracker.init(frame, bbox)

#     while True:
#         # Lê frame por frame do vídeo
#         ret, frame = cap.read()

#         # Se não houver mais frames, termine o loop
#         if not ret:
#             print("Fim do vídeo ou erro ao carregar frames.")
#             break

#         # Atualiza a posição do rastreador
#         success, bbox = tracker.update(frame)

#         # Se o rastreamento foi bem-sucedido, desenha o retângulo ao redor do container
#         if success:
#             x, y, w, h = [int(v) for v in bbox]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 10)  # Retângulo azul
#         else:
#             cv2.putText(frame, "Falha no rastreamento", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

#         # Exibe o frame com o rastreamento
#         cv2.imshow("Rastreamento de Container", frame)

#         # Pressione 'q' para sair
#         if cv2.waitKey(30) & 0xFF == ord('q'):
#             break

#     # Libera o vídeo e fecha todas as janelas
#     cap.release()
#     cv2.destroyAllWindows()

# # Caminho para o vídeo (substitua pelo caminho correto do vídeo)
# video_path = "./video/video.mov"

# # Chama a função para rastrear o container no vídeo
# track_container_in_video(video_path)

import cv2
import os
import time

# Função para inicializar o rastreador de objetos (usando CSRT para rastreamento robusto)
def initialize_tracker():
    tracker = cv2.TrackerCSRT_create()  # CSRT é robusto para rastreamento
    return tracker

# Função para salvar a imagem recortada
def save_cropped_image(frame, bbox, save_dir):
    x, y, w, h = [int(v) for v in bbox]
    cropped_img = frame[y:y+h, x:x+w]  # Recorta a área selecionada do frame

    # Gera um nome único baseado no timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"container_{timestamp}.png"

    # Verifica se o diretório de destino existe; caso contrário, cria-o
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Salva a imagem recortada
    save_path = os.path.join(save_dir, filename)
    cv2.imwrite(save_path, cropped_img)
    print(f"Imagem salva em: {save_path}")

# Função principal para rastreamento de container de navio
def track_container_in_video(video_path, save_dir):
    while True:
        # Carrega o vídeo
        cap = cv2.VideoCapture(video_path)

        # Verifica se o vídeo foi carregado com sucesso
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            return

        # Lê o primeiro frame do vídeo
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível ler o vídeo.")
            return

        # Seleciona manualmente o container (retângulo azul) no primeiro frame
        print("Selecione a área do container no primeiro frame.")
        bbox = cv2.selectROI("Selecione o Container", frame, fromCenter=False, showCrosshair=True)

        # Inicializa o rastreador com a área selecionada (bounding box)
        tracker = initialize_tracker()
        tracker.init(frame, bbox)

        while True:
            # Lê frame por frame do vídeo
            ret, frame = cap.read()

            # Se não houver mais frames, reinicia o vídeo
            if not ret:
                print("Reiniciando o vídeo...")
                cap.release()
                break  # Sai do loop interno para reiniciar o vídeo

            # Atualiza a posição do rastreador
            success, bbox = tracker.update(frame)

            # Se o rastreamento foi bem-sucedido, desenha o retângulo ao redor do container
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 16)  # Retângulo azul

                # Exibe as coordenadas (X, Y) em cima do retângulo
                text = f"X: {x}, Y: {y}"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
                if x < 700:
                    cv2.putText(frame, "Desembarque 1", (999, 700), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)

                # Salva a imagem recortada no diretório "../images/images"
                save_cropped_image(frame, bbox, save_dir)

            else:
                cv2.putText(frame, "Falha no rastreamento", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            # Exibe o frame com o rastreamento
            cv2.imshow("Rastreamento de Container", frame)

            # Pressione 'q' para sair
            if cv2.waitKey(30) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return  # Encerra o programa

# Caminho para o vídeo (substitua pelo caminho correto do vídeo)
video_path = "./getContainers/video/video_fast_4.mov"

# Diretório onde as imagens recortadas serão salvas
save_dir = "./images/images"

# Chama a função para rastrear o container no vídeo e salvar as imagens recortadas
track_container_in_video(video_path, save_dir)