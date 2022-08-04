import cv2
import time
import numpy as np
import pytesseract
from time import sleep
import imutils
from pyModbusTCP.client import ModbusClient

d = ModbusClient(host="192.168.0.10", port=502,
                 unit_id=1, auto_open=True, auto_close=True)

indexCAM = 1

def initCamera():
    webcam = cv2.VideoCapture(indexCAM, cv2.CAP_DSHOW)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 920)
    # webcam.set(cv2.CAP_PROP_AUTOFOCUS, 2)
    webcam.set(cv2.CAP_PROP_FOCUS, 40)
    webcam.set(cv2.CAP_PROP_ZOOM, 300.0)

    if not webcam.isOpened():
        raise Exception("Camera not found")
    return webcam

def detect(webcam):
    _, frame = webcam.read()    
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    _, bin = cv2.threshold(gray, 205, 255, cv2.THRESH_TOZERO)
    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    contornos, hier = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro > 150:
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(aprox) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+alt, y+lar), (0, 255, 0), 4)
                roi = frame[y:y + lar, x:x + alt]
            
                cinza = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                _, tresh = cv2.threshold(cinza, 240, 255, cv2.THRESH_TOZERO)
                cv2.imwrite('detect.jpg', tresh)
                pytesseract.pytesseract.tesseract_cmd = R"C:\Users\bc1g7841\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
                dados = pytesseract.image_to_string((tresh), output_type=pytesseract.Output.DICT)
                text = "{}".format(dados)
                if ('Character Detection') in text:
                    print(dados,"Aprovado")
                    d.write_single_register(200, 2)

    cv2.imshow('draw', frame)
    cv2.waitKey(1)
