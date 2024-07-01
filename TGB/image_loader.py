import cv2 as cv
from tkinter import filedialog, messagebox, NW
from PIL import Image, ImageTk
import tkinter as tk

class ImageLoader:
    def __init__(self, canvas):
        self.canvas = canvas
        self.image_path = None
        self.original_image = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.image_path:
            self.original_image = cv.imread(self.image_path)
            if self.original_image is None:
                messagebox.showerror("Editor de Imagens", "Falha ao carregar a imagem.")
                return
            self.display_image(self.original_image)

    def display_image(self, img):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil.resize((760, 500), Image.LANCZOS))  # Ajusta o tamanho da imagem exibida no canvas
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        print("Imagem carregada e exibida no canvas.")
