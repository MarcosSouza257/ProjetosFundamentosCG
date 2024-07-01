import cv2 as cv
from PIL import Image, ImageFilter
import numpy as np

class FilterApplier:
    def __init__(self, image_loader, video_manager=None):
        self.image_loader = image_loader
        self.video_manager = video_manager
        self.filtered_image = None
        self.current_filter = None

        # Dicionário de filtros
        self.filters = {
            "No filter": self.no_filter,
            "BLUR": self.blur_filter,
            "GRAYSCALE": self.grayscale_filter,
            "DETAIL": self.detail_filter,
            "EMBOSS": self.emboss_filter,
            "EDGE_ENHANCE": self.edge_enhance_filter,
            "DILATE": self.dilate_filter,
            "BITWISE_NOT": self.bitwise_not_filter,
            "PENCIL_SKETCH": self.pencil_sketch_filter,
            "EQ": self.eq_filter,
            "CANNY": self.canny_filter,
        }

    def apply_filter(self, filter_name, is_video=False):
        if filter_name:
            self.current_filter = filter_name
        
        img = self.video_manager.original_image if is_video else self.image_loader.original_image
        if img is None:
            return

        # Aplica o filtro
        self.filtered_image = self.filters.get(self.current_filter, self.no_filter)(img)
        
        if is_video:
            self.video_manager.display_image(self.filtered_image)
        else:
            self.image_loader.display_image(self.filtered_image)
    
    def no_filter(self, img):
        return img

    def blur_filter(self, img):
        img_pil = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        img_pil = img_pil.filter(ImageFilter.BLUR)
        return cv.cvtColor(np.array(img_pil), cv.COLOR_BGR2RGB)

    def grayscale_filter(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    def detail_filter(self, img):
        return cv.detailEnhance(img, sigma_s=10, sigma_r=0.15)

    def emboss_filter(self, img):
        kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        return cv.filter2D(img, -1, kernel)

    def edge_enhance_filter(self, img):
        img_pil = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        img_pil = img_pil.filter(ImageFilter.EDGE_ENHANCE)
        return cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)

    def dilate_filter(self, img):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        return cv.dilate(img, kernel)

    def bitwise_not_filter(self, img):
        return cv.bitwise_not(img)

    def pencil_sketch_filter(self, img):
        _, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
        return sk_color

    def eq_filter(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return cv.equalizeHist(img)

    def canny_filter(self, img):
        return cv.Canny(img, 25, 75)
