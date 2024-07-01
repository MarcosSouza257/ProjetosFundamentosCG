import tkinter as tk

class WidgetCreator:
    def __init__(self, root, load_image, toggle_video, apply_filter, save_image):
        self.root = root
        self.load_image = load_image
        self.toggle_video = toggle_video
        self.apply_filter = apply_filter
        self.save_image = save_image

    def create_widgets(self):
        # Criar um frame para os botões
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=10)

        # Botão para carregar imagem
        self.load_button = tk.Button(button_frame, text="Carregar Imagem", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Botão para capturar vídeo
        self.video_button = tk.Button(button_frame, text="Capturar Vídeo", command=self.toggle_video)
        self.video_button.grid(row=0, column=1, padx=5, pady=5)

        # Menu de opções para filtros
        self.filter_var = tk.StringVar(self.root)
        self.filter_var.set("Escolher filtro")
        self.filter_menu = tk.OptionMenu(button_frame, self.filter_var, "No Filter", "BLUR", "GRAYSCALE", "DETAIL", "EMBOSS","EDGE_ENHANCE","DILATE","BITWISE_NOT","PENCIL_SKETCH","EQ","CANNY", command=self.apply_filter)
        self.filter_menu.grid(row=0, column=2, padx=5, pady=5)

        # Botão para salvar imagem
        self.save_button = tk.Button(button_frame, text="Salvar Imagem/Frame", command=self.save_image)
        self.save_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Canvas para exibir imagem/vídeo
        self.canvas = tk.Canvas(self.root, width=760, height=500, bg='gray')  # Ajusta o tamanho do canvas
        self.canvas.grid(row=1, column=0, padx=10, pady=10)
        
        return self.canvas
