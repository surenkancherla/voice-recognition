import os
import pickle as cPickle
import numpy as np
from Audiosplit import getWavfile,convertTowav
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from Feature_Extraction import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
import sklearn.mixture.gaussian_mixture
from flask import Flask,redirect,url_for,jsonify,flash,request
from werkzeug import secure_filename
from Model_Test import test_sample
from app import app

#app=Flask(__name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'mp4'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/authentication-upload', methods=['GET', 'POST'])
def upload_testfile():
    sourceDir  = "test_samples/"   
    destDir = "Speakers_models/"
    UPLOAD_FOLDER = './test_samples/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename.endswith(".mp3"):
                file.save(os.path.join('test_samples',secure_filename(file.filename)))
                replace_filename=filename.split(".")[0] + ".wav"
                getWavfile(8000,1,filename,replace_filename,"./test_samples/","./test_samples/")
            else:
                file.save(os.path.join('test_samples',secure_filename(file.filename)))

            flag, _speakerMatch, _confidence = test_sample(filename,sourceDir,destDir)
            
            responseJson = {}
            _speakerName = ""
            _guid = ""
            confidenceThreshold = 0.75

            htmlStr = ""

            if(_speakerMatch != ""):
                filenNameArr = _speakerMatch.split("-") #get the name of the speaker
                _speakerName = filenNameArr[0]
                _guid = filenNameArr[1]

            if(_confidence > confidenceThreshold):
                responseJson = jsonify(
                            status = 200,
                            message = "Match found",
                            name = _speakerName,
                            guid = _guid,
                            confidence = _confidence
                        )
            elif(_confidence < confidenceThreshold):
                responseJson = jsonify(
                            status = 200,
                            message = "Match not found",
                            guid = _guid,
                            speaker = _speakerName,
                            confidence = _confidence
                        )
                
            else: 
                responseJson = jsonify(
                            status = 500,
                            message = "Internal server error"
                        )

        return responseJson
    return '''
<!doctype html>
<title>Upload test File</title>
<h1>Upload Test File</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
<input type=submit value=Test>
</form>
'''
    

"""if __name__ == "__main__":
    app.run(debug=True)"""