import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\Tesseract.exe'
img = cv2.imread('../1. Itens BNI/158974.png')
print(pytesseract.image_to_string(img, lang='por'))