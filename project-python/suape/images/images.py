import os
import time
from tkinter import *
from PIL import Image, ImageTk
import glob
from tkinter import messagebox

# Função para carregar e atualizar as imagens na tela
def update_images(image_frame, image_list, image_dir):
    # Limpa o frame de imagens anteriores
    for widget in image_frame.winfo_children():
        widget.destroy()

    # Carrega as imagens do diretório
    image_files = glob.glob(os.path.join(image_dir, "*.jpg")) + glob.glob(os.path.join(image_dir, "*.png")) + glob.glob(os.path.join(image_dir, "*.jpeg"))

    # Organiza as imagens em 3 colunas
    columns = 3
    for idx, image_file in enumerate(image_files):
        img = Image.open(image_file)
        img.thumbnail((200, 200))  # Redimensiona para thumbnails de 200x200 pixels
        img = ImageTk.PhotoImage(img)

        # Salva a referência da imagem para que não seja destruída
        image_list.append(img)

        # Cria um label para exibir a imagem
        lbl = Label(image_frame, image=img)
        lbl.grid(row=idx // columns, column=idx % columns, padx=5, pady=5)

    # Atualiza o frame a cada 2 segundos
    image_frame.after(2000, update_images, image_frame, image_list, image_dir)

# Função para simular o treinamento
def train_model():
    messagebox.showinfo("Treinamento", "Iniciando o treinamento do modelo...")
    # Aqui você pode adicionar o código para iniciar o treinamento do seu modelo

# Função principal para iniciar a interface
def start_image_viewer(image_dir):
    root = Tk()
    root.title("Visualizador de Imagens em Tempo Real")
    root.geometry("800x600")  # Tamanho da janela

    # Frame para exibir as imagens
    image_frame = Frame(root)
    image_frame.pack(fill=BOTH, expand=True)

    # Lista para armazenar as imagens carregadas (evita que sejam coletadas pelo garbage collector)
    image_list = []

    # Botão "Treinar" no topo
    train_button = Button(root, text="Treinar Modelo", command=train_model, font=("Arial", 14), bg="green", fg="black")
    train_button.pack(pady=10)

    # Atualiza as imagens no frame
    update_images(image_frame, image_list, image_dir)

    # Inicia o loop da interface gráfica
    root.mainloop()

# Caminho do diretório de imagens (substitua pelo diretório que deseja monitorar)
image_dir = "./images/images"

# Inicia o visualizador de imagens
start_image_viewer(image_dir)