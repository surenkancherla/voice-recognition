import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from app import app
"""
# Initialize the Flask application
#app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'Unknown/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['mp3', 'wav', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index-multiple.html')


# Route that will process the file upload
@app.route('/compare', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload-multiple.html', filenames=filenames)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )

similarityprob_score=2.98439642e-05
#similarityprob_score = float("{0:.2f}".format(similarityprob_score))
#format(similarityprob_score, '.2f')
print("&&&&&&",similarityprob_score)
print(format(similarityprob_score, '.8f'))

#Duration of a wav file
import wave
import contextlib
fname = '/Users/cb/Desktop/Compare clips/Aryan_15a.wav'
with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
chunk_duration=duration/15
print(duration)
print(int(chunk_duration))

"""

import requests

print('Beginning file download with requests')

url = 'http://127.0.0.1:5000/audiofile/AryanKandimalla-1da9d98c90c311e9a0103c15c2d936f0.wav'  
filename = url[url.rfind("/")+1:]
r = requests.get(url)

with open('/Users/cb/voice-recognition/voice-recognition/' + filename, 'wb') as f:  
    f.write(r.content)
print("@@@@@",filename)
# Retrieve HTTP meta-data
print(r.status_code)  
print(r.headers['content-type'])  
print(r.encoding)  
