import pytesseract
from PIL import Image

img = Image.open('123.png')
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

text = pytesseract.image_to_string(img)
print(text)

with open('123.txt', 'w') as text_file:
    text_file.write(text)


