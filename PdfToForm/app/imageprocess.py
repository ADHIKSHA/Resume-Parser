from PIL import Image, ImageFilter, ImageChops
import pytesseract
from pytesseract import image_to_string
import cv2
import numpy as np
import os
import sys
import logging
import tempfile


pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'
        
IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

size = None


def get_size_of_scaled_image(im):
    global size
    if size is None:
        length_x, width_y = im.size
        factor = max(1, int(IMAGE_SIZE / length_x))
        size = factor * length_x, factor * width_y
    return size

def process_image_for_ocr(imgcv,imp,extension):
    logging.info('Processing image for text Extraction')
    temp_filename = set_image_dpi(imp,extension)
    im_new = remove_noise_and_smooth(imgcv)
    return im_new


def set_image_dpi(im,extension):
    #im = Image.open(file_path)
    # size = (1800, 1800)
    size = get_size_of_scaled_image(im)
    im_resized = im.resize(size, Image.ANTIALIAS)
    if extension =="png":
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    elif extension=="jpg":
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    elif extension=="webp":
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webp')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))  # best for OCR
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(img):
    logging.info('Removing noise and smoothening image')
    #img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image


def main_fun(imgcv,imp,extension):
    #filename='F://resumes//resumemba.jpg'
    img= process_image_for_ocr(imgcv,imp,extension)
    custom_config = r' --psm 6 -c preserve_interword_spaces=1'
    result = pytesseract.image_to_string(img,lang='eng',config=custom_config)
    result=result.replace("      ",'\n')
    return result

