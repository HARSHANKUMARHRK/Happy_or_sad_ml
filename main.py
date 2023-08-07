from flask import Flask, render_template, Response, request, session, redirect, url_for
import os
import cv2
from keras.models import load_model
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = "abc"

@app.route('/', methods=['GET', 'POST'])
def get_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image part in the request."

        file = request.files['image']

        if file.filename == '':
            return "No selected file."

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            session['uploaded_image'] = file.filename
            return redirect(url_for('predict_output'))
        else:
            return "File type not allowed."

    return render_template('index.html')

def allowed_file(filename):
    allowed_extention = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extention

def load_vgg16_model():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
    return base_model

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@app.route('/predict')
def predict_output():
    img_filename = session.get('uploaded_image')
    img_path = 'uploads/' + img_filename

    base_model = load_vgg16_model()
    model = load_model("models/imageclassifier.h5")

    img_array = preprocess_image(img_path)
    features = base_model.predict(img_array)
    out = model.predict(features)

    if out < 0.5:
        pred = "Happy"
    else:
        pred = "Sad"

    return render_template("result.html", out=pred)

if __name__ == '__main__':
    app.run(debug=True)
