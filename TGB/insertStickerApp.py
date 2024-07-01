import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
import os

class insertStickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor Sticker")

        # Variáveis para armazenar as imagens e os stickers
        self.image_path = None
        self.image = None
        self.image_tk = None
        self.stickers = []
        self.selected_sticker_index = tk.IntVar(value=-1)  # Índice inicial -1 significa nenhum selecionado

        # Frame para botões
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Botões
        self.btn_load_image = tk.Button(self.button_frame, text="Carregar Imagem", command=self.load_image)
        self.btn_load_image.grid(row=0, column=0, padx=5)

        self.btn_save_image = tk.Button(self.button_frame, text="Salvar Imagem", command=self.save_image)
        self.btn_save_image.grid(row=0, column=1, padx=5)

        # Canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Carregar stickers da pasta "stickers"
        self.load_stickers()
        
        # Criar lista de seleção de stickers
        self.create_sticker_selection()

        # Eventos de clique no canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image.thumbnail((800, 600)) 
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def load_stickers(self):
        stickers_dir = "stickers"
        if not os.path.exists(stickers_dir):    
            print(f"A pasta {stickers_dir} não existe.")
            return

        sticker_files = os.listdir(stickers_dir)
        sticker_paths = [os.path.join(stickers_dir, file) for file in sticker_files if file.endswith((".png"))]

        for path in sticker_paths:
            sticker = Image.open(path)
            sticker.thumbnail((100, 100))  # Redimensiona o sticker
            self.stickers.append(sticker)

    def create_sticker_selection(self):
        if not self.stickers:
            return

        label = tk.Label(self.button_frame, text="Selecione um sticker:")
        label.grid(row=0, column=2, padx=10)

        # Criar dropdown para seleção de stickers
        sticker_names = [os.path.basename(path) for path in os.listdir("stickers")]
        self.sticker_dropdown = ttk.Combobox(self.button_frame, values=sticker_names, state="readonly")
        self.sticker_dropdown.grid(row=0, column=3, padx=5)
        self.sticker_dropdown.current(0)  # Seleciona o primeiro sticker por padrão

        # Evento para atualizar o índice do sticker selecionado
        self.sticker_dropdown.bind("<<ComboboxSelected>>", self.update_selected_sticker_index)

    def update_selected_sticker_index(self, event):
        selected_sticker_name = self.sticker_dropdown.get()
        selected_index = [os.path.basename(path) for path in os.listdir("stickers")].index(selected_sticker_name)
        self.selected_sticker_index.set(selected_index)

    def on_canvas_click(self, event):
        selected_index = self.selected_sticker_index.get()
        if selected_index != -1:
            #x, y = event.x, event.y
            sticker = self.stickers[selected_index].copy()

            # Dimensões do sticker
            sticker_width, sticker_height = sticker.width, sticker.height

            # Calcular a posição onde o centro do sticker deve ser colocado
            x = event.x - sticker_width // 2
            y = event.y - sticker_height // 2

            # Inserir o sticker na imagem original
            self.image.paste(sticker, (x, y), sticker)
            print("Coordenada X: {x}, Coordenada Y: {y}".format(x=x, y=y))
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def save_image(self):
        if self.image_path:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("Arquivos PNG", "*.png"), ("Arquivos JPEG", "*.jpg;*.jpeg")))
            if save_path:
                # Salvar a imagem com stickers
                self.image.save(save_path)
                print(f"Imagem salva em {save_path}")

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = insertStickerApp(root)
    app.mainloop()
