def read_image(img):
    img, success = rectify_image_rotation(img)
    if success:
        tesseract_init(tes_version=tes_v3)
        text = pytesseract.image_to_string(img, lang='rus+eng')

        return text
    else:
        return 'не удалось прочесть текст'