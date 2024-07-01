import cv2
from tkinter import NW
from PIL import Image, ImageTk

class VideoManager:
    def __init__(self, canvas, filter_applier):
        self.canvas = canvas
        self.cap = None
        self.video_streaming = False
        self.filter_applier = filter_applier
        self.original_image = None
        self.filtered_image = None

    def toggle_video(self):
        if not self.video_streaming:
            self.video_streaming = True
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                print("Erro ao abrir a câmera")
                self.video_streaming = False
            self.video_stream()
        else:
            self.video_streaming = False
            if self.cap is not None:
                self.cap.release()

    def video_stream(self):
        if self.video_streaming:
            ret, frame = self.cap.read()
            if ret:
                self.original_image = frame
                self.filter_applier.apply_filter(None, is_video=True)
            else:
                print("Falha ao capturar o quadro da câmera")
            self.canvas.after(10, self.video_stream)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil.resize((760, 500), Image.LANCZOS))  # Ajusta o tamanho da imagem exibida no canvas
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        print("Frame do vídeo exibido no canvas.")
