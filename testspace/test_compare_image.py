# -*-coding:utf-8 -*-
import pytesseract
from PIL import Image


im = Image.open('f:/images/11.png')
text = pytesseract.image_to_string(im)

print(text)
