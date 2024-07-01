import cv2
from tkinter import filedialog, messagebox

class ImageSaver:
    def save_image(self, original_image, filtered_image):
        if filtered_image is not None:
            img_to_save = filtered_image
        else:
            img_to_save = original_image

        if img_to_save is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")])
            if save_path:
                cv2.imwrite(save_path, img_to_save)
                messagebox.showinfo("Editor de Imagens", "Imagem salva com sucesso.")
        else:
            messagebox.showerror("Editor de Imagens", "Nenhuma imagem para salvar.")
