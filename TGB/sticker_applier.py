import cv2 as cv
import numpy as np

class StickerApplier:
    def __init__(self, image_loader, video_manager=None):
        self.image_loader = image_loader
        self.video_manager = video_manager
        self.sticker_image = None
        self.current_sticker = None
        self.mouse_position = (0, 0)

        self.stickers = {
            "No Sticker": None,
            "Sticker 1": "stickers/sticker1.png",
            "Sticker 2": "stickers/sticker2.png",
            "Sticker 3": "stickers/sticker3.png",
            "Sticker 4": "stickers/sticker4.png",
            "Sticker 5": "stickers/sticker5.png",
        }

    def apply_sticker(self, sticker_name, x=None, y=None, is_video=False):
        if sticker_name:
            self.current_sticker = sticker_name
        
        if is_video:
            img = self.video_manager.original_image
        else:
            img = self.image_loader.original_image
        
        if img is None:
            return
        
        if x is None or y is None:
            x, y = self.mouse_position
        
        self.sticker_image = self.apply_sticker_to_image(img, self.stickers.get(self.current_sticker), x, y)
        
        if is_video:
            self.video_manager.display_image(self.sticker_image)
        else:
            self.image_loader.display_image(self.sticker_image)

    def apply_sticker_to_image(self, img, sticker_path, x, y):
        if not sticker_path:
            return img
        
        sticker = cv.imread(sticker_path, cv.IMREAD_UNCHANGED)
        sticker = self.resize_sticker(sticker, 100)
        
        # Ensure the sticker fits within image bounds
        sticker_h, sticker_w, _ = sticker.shape
        img_h, img_w, _ = img.shape
        
        x = max(0, min(x, img_w - sticker_w))
        y = max(0, min(y, img_h - sticker_h))
        
        return self.overlay_sticker(img, sticker, x, y)

    def resize_sticker(self, sticker, scale_percent):
        width = int(sticker.shape[1] * scale_percent / 100)
        height = int(sticker.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv.resize(sticker, dim, interpolation=cv.INTER_AREA)

    def overlay_sticker(self, background, sticker, x, y):
        sticker_h, sticker_w, _ = sticker.shape
        
        for c in range(3):
            background[y:y+sticker_h, x:x+sticker_w, c] = sticker[:, :, c] * (sticker[:, :, 3] / 255.0) + \
                                                           background[y:y+sticker_h, x:x+sticker_w, c] * \
                                                           (1.0 - sticker[:, :, 3] / 255.0)

        return background

    def set_mouse_callback(self, canvas):
        self.canvas = canvas
        self.canvas.bind("<Button-1>", self.mouse_click_internal)

    def mouse_click_internal(self, event):
        x, y = event.x, event.y
        self.mouse_position = (x, y)
        self.apply_sticker(self.current_sticker, x, y)
