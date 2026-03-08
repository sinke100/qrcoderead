from flask import Flask, render_template, request
import cv2 as cv 
import numpy as np
import PIL.Image as im
from pyzbar.pyzbar import decode
from io import BytesIO as b
from collections import Counter

app = Flask(__name__)
app.template_folder = '.'

def buffer(x):
    with b() as output:
        x.save(output, 'PNG')
        data = output.getvalue()
    return data

def edge_value(x):
    x = list(Counter(x).items())
    x.sort(key=lambda i: i[-1],reverse=True)
    x = x[:5]
    x = [i[0] for i in x]
    return max(x)-10
    
def simplify(fr):
    img = im.open(b(fr)).convert('L')
    size = img.size
    img = img.tobytes()
    mx = edge_value(img)
    img_b = bytes([0 if i < mx else 255 for i in img])
    img_b = im.frombytes('L',size,img_b).convert('1')
    return buffer(img_b)

def reverse(fr):
    img = im.open(b(fr)).convert('L')
    size = img.size
    img = img.tobytes()
    assert len(set(img)) == 2
    img_inv = bytes([i^255 for i in img])
    img_inv = im.frombytes('L',size,img_inv).convert('1')
    return buffer(img_inv)

def trp(data):
    data = bytes(data)
    img = im.open(b(data))
    try: qr = decode(img)[0]
    except IndexError: return
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
    file = request.files['image'].read()
    fr = simplify(file)
    data = tr(list(fr))
    if data: return data
    fr = reverse(fr)
    data = tr(list(fr))
    if data: return data
    return "Can't read",400

if __name__ == '__main__':
    app.run(host='0.0.0.0')

