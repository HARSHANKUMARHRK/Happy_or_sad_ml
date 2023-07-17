from flask import Flask, render_template,Response, request,session,redirect,url_for
import os
import cv2
import tensorflow as tf
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = "abc" 
@app.route('/',methods=['GET','POST'])



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

@app.route('/predict')

def predict_output():
    img_filename = session.get('uploaded_image')
    imgPath='uploads/'+img_filename
    from keras.models import load_model
    model =load_model("models/imageclassifier.h5")
    img = cv2.imread(imgPath)
    resize = tf.image.resize(img, (256,256))
    out = model.predict(np.expand_dims(resize/255, 0))
    if(out<0.5):
        pred="Happy"
    else:
        pred="sad"

    return render_template("result.html",out=pred)

    
    

if __name__ == '__main__':
    app.run(debug=True)
