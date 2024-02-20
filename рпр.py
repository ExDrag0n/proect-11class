import cv2
import pytesseract
from pytesseract import Output
from scipy import ndimage

debug = True

tes_v3 = r'C:\Program Files (x86)\Tesseract-OCR-3\tesseract.exe'


def tesseract_init(tes_version=tes_v3):
    pytesseract.pytesseract.tesseract_cmd = tes_version
    #print(tes_version)


def preprocess_image(img):
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.medianBlur(processed_img, 1)
    processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)
    #cv2.imwrite('processed_img.png', processed_img)
    return processed_img


def last_chance(img):
    processed_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    processed_img = cv2.bitwise_not(processed_img)
    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.medianBlur(processed_img, 1)
    processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)
    return processed_img


def rectify_image_rotation(img):
    tesseract_init(tes_version=tes_v3)
    success = False

    try:
        rectified_image = preprocess_image(img)
        osd = pytesseract.image_to_osd(rectified_image, output_type=Output.DICT)
        success = True

    except pytesseract.pytesseract.TesseractError:

        try:
            rectified_image = last_chance(img)
            osd = pytesseract.image_to_osd(rectified_image, output_type=Output.DICT)
            success = True

        except pytesseract.pytesseract.TesseractError:
            return img, success

    angle = -osd['rotate']

    if debug:
        print('Повернуто на', angle, 'градусов')

    rectified_img = ndimage.rotate(rectified_image, angle)
    return rectified_img, success