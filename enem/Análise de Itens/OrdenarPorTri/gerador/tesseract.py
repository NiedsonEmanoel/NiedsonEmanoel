import cv2
import numpy as np
import requests
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt


pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\Tesseract.exe'
img = cv2.imdecode('../1. Itens BNI/158974.png')
print(pytesseract.image_to_string(img, lang='por'))


def ocrImage(code):
    code = 158974
    code = 'https://niedsonemanoel.com.br/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/'+str(str(code) + '.png')
    try:
      response = requests.get(code)
      img_array = np.array(bytearray(response.content), dtype=np.uint8)

      # Decodificar a imagem usando o OpenCV
      img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
      ocrT = str(pytesseract.image_to_string(img, lang='por'))
    except:
        ocrT = 'N/A'
    return ocrT



ocrImage(158974)