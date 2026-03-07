from flask import Flask, render_template, request
import cv2 as cv 
import numpy as np
import PIL.Image as im
from pyzbar.pyzbar import decode
from io import BytesIO as b

app = Flask(__name__)
app.template_folder = '.'

def trp(data):
    data = bytes(data)
    img = im.open(b(data))
    qr = decode(img)[0]
    return qr.data.decode()
    
def tr(data):
    array = np.array(data,np.uint8)
    img = cv.imdecode(array, cv.IMREAD_UNCHANGED)
    qr = cv.QRCodeDetector()
    value = qr.detectAndDecode(img)[0]
    if value: return value
    value = trp(data)
    if value: return value

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['image']
    data = tr(list(file.read()))
    if data: return data
    else: return "Can't read",400

if __name__ == '__main__':
    app.run(host='0.0.0.0')

