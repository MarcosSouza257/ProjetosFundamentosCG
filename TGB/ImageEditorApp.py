import tkinter as tk
from widget_creator import WidgetCreator
from image_loader import ImageLoader
from video_manager import VideoManager
from filter_applier import FilterApplier
from image_saver import ImageSaver
from sticker_applier import StickerApplier

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imagens")
        self.root.geometry("800x600")
        
        self.image_saver = ImageSaver()
        
        # Criar elementos da interface
        self.widget_creator = WidgetCreator(self.root, self.load_image, self.toggle_video, self.apply_filter, self.save_image)
        self.canvas = self.widget_creator.create_widgets()
        
        self.image_loader = ImageLoader(self.canvas)
        self.filter_applier = FilterApplier(self.image_loader, None)
        self.video_manager = VideoManager(self.canvas, self.filter_applier)
        self.filter_applier.video_manager = self.video_manager

    def load_image(self):
        self.image_loader.load_image()
    
    def toggle_video(self):
        self.video_manager.toggle_video()
        
    def apply_filter(self, filter_name):
        self.filter_applier.apply_filter(filter_name)
    
    def save_image(self):
        self.image_saver.save_image(self.image_loader.original_image, self.filter_applier.filtered_image)

    def display_image(self, img):
        self.image_loader.display_image(img)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
    
