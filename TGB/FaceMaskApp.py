import cv2 as cv
import mediapipe as mp
from PIL import Image
import numpy as np

webcam = cv.VideoCapture(0)

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection()

# Carregar a mascara 
mask_path = "mascaras/gato.png"
mask = Image.open(mask_path).convert("RGBA")

while True:
    validacao, frame = webcam.read()  # Ler o frame da webcam
    if not validacao:
        break
    
    # Converter o frame para RGB (o MediaPipe usa RGB)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    # Detectar rostos na imagem
    results = face_detection.process(frame_rgb)
    
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            # Redimensionar a mascara
            mask_resized = mask.resize((w, h))

            # Converter a mascara para formato OpenCV (BGR)
            mask_np = np.array(mask_resized)
            mask_cv = cv.cvtColor(mask_np, cv.COLOR_RGBA2BGRA)

            # Aplicar a transparência
            alpha_s = mask_cv[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            # Ajustar a posição da mascara
            y -= int(0.2 * h)

            # Limitar a posição y
            y = max(0, y)

            # Sobrepor a mascara sobre o rosto
            for c in range(0, 3):
                frame[y:y+h, x:x+w, c] = (alpha_s * mask_cv[:, :, c] +
                                           alpha_l * frame[y:y+h, x:x+w, c])

    # Exibir
    cv.imshow('FaceMackApp', frame)

    key = cv.waitKey(1)
    if key == 27 or cv.getWindowProperty('FaceMackApp', cv.WND_PROP_VISIBLE) < 1:
        break

webcam.release()
cv.destroyAllWindows()