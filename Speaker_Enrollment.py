import os,shutil
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from sklearn import mixture
from Feature_Extraction import extract_features
import warnings         
warnings.filterwarnings("ignore")
from flask import Flask,redirect,url_for,jsonify,flash,request,render_template,send_from_directory
from werkzeug import secure_filename
from Model_Train import model_train
from Model_Test import test_sample, compare_test
from Audiosplit import audio_split,convertTowav,getWavfile,convertURLToFile
from app import app
import wave, struct
import uuid
import json
import subprocess
import glob, sys
from subprocess import Popen, PIPE
import time
import Url_Module as urlModule

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'mp4'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def start():
    return "Welcome"

@app.route('/readme', methods=['GET'])
def document():
    return render_template('readme.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    UPLOAD_FOLDER = './audio_sources/'
    #app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    sourceDir   = "./uploads/"   
    destDir = "./Speakers_models/"
    wavSourceDir = "./audio_sources/"
    chunk_length_ms = 3000
    if request.method == 'POST':
        file = request.files['file']
        personname = request.form['personname']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            guid = str(uuid.uuid1()).replace("-", "")
            replace_filename = str(personname).replace(" ", "") + '-' + str(guid) + '.wav'
            isMP3 = False
            print("@@@@@@@@",replace_filename)

            if filename.endswith(".mp3"):
                isMP3 = True
                file.save(os.path.join('audio_sources',secure_filename(file.filename)))
                #Convert mp3 to wav and save to audio_sources with appended guid 
                getWavfile(8000,1,filename,replace_filename,"./audio_sources/","./audio_sources/")

            else:
                file.save(os.path.join('audio_sources',secure_filename(file.filename)))
                #Save the uploaded wav file to audio_sources with appended guid
                os.rename('./audio_sources/' + filename, './audio_sources/' + replace_filename)            

            #rename file name
            #os.rename('./audio_sources/' + filename, './audio_sources/' + replace_filename)            
            audio_split(replace_filename, isMP3, wavSourceDir,chunk_length_ms)
            training_result = model_train(replace_filename,sourceDir,destDir)
            responseJson = {}
            appurl = request.url.split("/upload")

            if training_result == "Modelling completed":
                responseJson = jsonify(
                            status = 200,
                            message = "Enrollment Successful",
                            guid = str(guid),
                            name = personname,
                            link =  appurl[0] + "/audiofile/" + replace_filename
                        )
            else: 
                responseJson = jsonify(
                            status = 500,
                            message = "Enrollment Failed",
                            guid = str(guid),
                            name = personname
                        )
            return responseJson

    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
Person Name: <input type=text name=personname value="john david">
<input type=submit value=Upload>
</form>
'''

@app.route('/logindelete')
def index():
   return render_template('delete.html')

#To automatically delete the files when app gets heavy
@app.route('/handle_delete',methods = ['POST', 'GET'])
def handle_delete():
    inputFolder = request.form['inputFolder']
    if inputFolder=="all":
        folder_paths=['./uploads','./audio_sources','./test_samples', './Unknown']
        for folder in folder_paths:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if the_file.endswith(".wav") or the_file.endswith(".mp3"):
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                except Exception as e:
                    print(e)

    else:
        inputFolder = "./" + request.form['inputFolder']
        for the_file in os.listdir(inputFolder):
            file_path = os.path.join(inputFolder, the_file)
            try:
                if the_file.endswith(".wav") or the_file.endswith(".gmm") or the_file.endswith(".mp3"):
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            except Exception as e:
                print(e)
    return("***Deleted files***")

@app.route('/delete', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('delete_login.html', error=error)


#To query the list of enrolled speakers' gmm files
@app.route('/queryenrolledfiles', methods=['GET'])
def queryaudiofiles():
    error = None
    filesArr = []

    folder_paths=['./Speakers_models']
    for folder in folder_paths:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if the_file.endswith(".gmm"):
                    if os.path.isfile(file_path):
                        fileNameArr = the_file.split(".gmm")[0].split("-")
                        appurl = request.url.split("/queryenrolledfiles") 
                        link = appurl[0] + "/audiofile/" + fileNameArr[0] + "-" + fileNameArr[1] + ".wav"
                        filesArr.append({ "name": fileNameArr[0], "guid": fileNameArr[1], "link" : link })
            except Exception as e:
                print(e)
    print(filesArr)
    if(len(filesArr) > 0 ):
        responseJson = jsonify(data = filesArr)
    else:
        responseJson = jsonify(data =  [])

    return responseJson

#Download the desirable wav file
@app.route('/audiofile/<path:fname>',methods=['GET','POST'])
def get_file(fname):
    return send_from_directory(directory = "./audio_sources", filename = fname)

#To compare two audio files 
@app.route('/filecompare', methods=['GET', 'POST'])
def compare_files():
    
    print("url address: *** ", urlModule.getUrl(request))
    print("***** filecompare reached")
    start = time.clock()
    UPLOAD_FOLDER = './Unknown/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    sourceDir   = "./Unknown/"   
    destDir = "./Unknown/"
    trainSourceDir="./uploads/"
    chunk_length_ms = 1000

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                guid = str(uuid.uuid1()).replace("-", "")
                replace_filename = str(filename.split(".wav")[0]).replace(" ", "") + '-' + str(guid) + '.wav'
                isMP3 = False

                if filename.endswith(".mp3"):
                    isMP3 = True
                    file.save(os.path.join('Unknown',secure_filename(file.filename)))
                    filenames.append(replace_filename)
                    #Convert mp3 to wav and save to audio_sources with appended guid 
                    getWavfile(8000,1,filename,replace_filename,"./Unknown/","./Unknown/")

                else:
                    file.save(os.path.join('Unknown',secure_filename(file.filename)))
                    filenames.append(replace_filename)
                    #Save the uploaded wav file to audio_sources with appended guid
                    os.rename('./Unknown/' + filename, './Unknown/' + replace_filename)            

                #rename file name
                #os.rename('./audio_sources/' + filename, './audio_sources/' + replace_filename)            
        print("*******",filenames)

        model_train_starttime = time.clock()

        audio_split(filenames[0], isMP3 , sourceDir, chunk_length_ms)
        training_result = model_train(filenames[0],trainSourceDir,destDir)
        audio_split(filenames[1], isMP3 , sourceDir, chunk_length_ms)
        training_result = model_train(filenames[1],trainSourceDir,destDir)

        model_train_endtime = time.clock() - model_train_starttime
        print("$$$$$$$$$$$$$ Compare two .wav files model training completed in {0:.0f}ms".format(model_train_endtime))
        
        responseJson = {}
        appurl = request.url.split("/compare")

        if training_result == "Modelling completed":
            print("*********",filenames[1])
            compare_test_starttime = time.clock()

            flag, _similarityProbScore, _compareMatch = compare_test(filenames,sourceDir,destDir)
            responseJson = {}
            confidenceThreshold = 0.75
            compare_test_endtime = time.clock() - compare_test_starttime
            print("$$$$$$$$$$$$ Compare two .wav files compare_test completed in {0:.0f}ms".format(compare_test_endtime))

            if(_similarityProbScore == 1):
                responseJson = jsonify(
                                status = 200,
                                message = _compareMatch
                            )

            else:
                responseJson = jsonify(
                                status = 200,
                                message = _compareMatch,
                                similarityProbScore =format(_similarityProbScore, '.8f')
                            )
            request_time = time.clock() - start
            print("$$$$$$$$$$$$$$$ Compare two .wav files request completed in {0:.0f}ms".format(request_time))
        return responseJson
    return '''
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
              rel="stylesheet">
      </head>
      <body>
        <div class="container">
          <hr/>
          <div>
          <h3>Upload files to compare</h3>
          <form action="" method="post" enctype="multipart/form-data">
            <input type="file" multiple="" name="file[]" /><br />
            <input type="submit" value="Upload" >
          </form>
          </div>
        </div>
      </body>
    </html>
    '''

@app.route('/urlcompare', methods=['GET', 'POST'])
def compare_urls():
    UPLOAD_FOLDER = './Unknown/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    sourceDir   = "./Unknown/"   
    destDir = "./Unknown/"
    trainSourceDir="./uploads/"
    chunk_length_ms = 1000
    if request.method == 'POST':

        uploaded_files=[]
        urlnames = []

        urlnames.append(request.form['filelink1'])
        convertedFileName = convertURLToFile(urlnames[0])
        uploaded_files.append(convertedFileName)

        urlnames.append(request.form['filelink2'])
        convertedFileName = convertURLToFile(urlnames[1])
        uploaded_files.append(convertedFileName)

        for filename in uploaded_files:
            isMP3 = False
            if filename.endswith(".mp3"):
                isMP3 = True
                #file.save(os.path.join('Unknown',secure_filename(file.filename)))
                #filenames.append(replace_filename)
                #Convert mp3 to wav and save to audio_sources with appended guid 
                getWavfile(8000,1,filename,replace_filename,"./Unknown/","./Unknown/")     

        audio_split(uploaded_files[0], isMP3 , sourceDir, chunk_length_ms)
        training_result = model_train(uploaded_files[0],trainSourceDir,destDir)
        audio_split(uploaded_files[1], isMP3 , sourceDir, chunk_length_ms)
        training_result = model_train(uploaded_files[1],trainSourceDir,destDir)
        responseJson = {}
        appurl = request.url.split("/compare")

        if training_result == "Modelling completed":
            print("*********",uploaded_files[1])
            flag, _similarityProbScore, _compareMatch = compare_test(uploaded_files,sourceDir,destDir)
            responseJson = {}
            confidenceThreshold = 0.75

            if(_similarityProbScore == 1):
                responseJson = jsonify(
                                status = 200,
                                message = _compareMatch
                            )

            else:
                responseJson = jsonify(
                                status = 200,
                                message = _compareMatch,
                                similarityProbScore =format(_similarityProbScore, '.8f')

                            )
            
            return responseJson
    return '''
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
              rel="stylesheet">
      </head>
      <body>
        <div class="container">
          <hr/>
          <div>
          <h3>Enter URLs to Compare</h3><br/>
          <form action="" method="post" enctype="multipart/form-data">
            <p>URL 1: <input type="text" name="filelink1"><br/><br /></p>
            <p>URL 2: <input type="text" name="filelink2"><br/><br /></p>
            <input type="submit" value="Upload" >
          </form>
          </div>
        </div>
      </body>
    </html>
    '''

@app.route('/mixedcompare', methods=['GET', 'POST'])
def compare_mixed():
    UPLOAD_FOLDER = './Unknown/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    sourceDir   = "./Unknown/"   
    destDir = "./Unknown/"
    trainSourceDir="./uploads/"
    chunk_length_ms = 1000
    if request.method == 'POST':

        uploaded_files = []
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            guid = str(uuid.uuid1()).replace("-", "")
            replace_filename = str(filename.split(".wav")[0]).replace(" ", "") + '-' + str(guid) + '.wav'
            isMP3 = False
            print("@@@@@@@@",replace_filename)

            if filename.endswith(".mp3"):
                isMP3 = True
                file.save(os.path.join('Unknown',secure_filename(file.filename)))
                uploaded_files.append(replace_filename)
                #Convert mp3 to wav and save to audio_sources with appended guid 
                getWavfile(8000,1,filename,replace_filename,"./Unknown/","./Unknown/")

            else:
                file.save(os.path.join('Unknown',secure_filename(file.filename)))
                uploaded_files.append(replace_filename)
                #Save the uploaded wav file to audio_sources with appended guid
                os.rename('./Unknown/' + filename, './Unknown/' + replace_filename)

        urlname = request.form['filelink']
        convertedFileName = convertURLToFile(urlname)
        uploaded_files.append(convertedFileName)

        for filename in uploaded_files:
            isMP3 = False
            if filename.endswith(".mp3"):
                isMP3 = True
                #file.save(os.path.join('Unknown',secure_filename(file.filename)))
                #filenames.append(replace_filename)
                #Convert mp3 to wav and save to audio_sources with appended guid 
                getWavfile(8000,1,filename,replace_filename,"./Unknown/","./Unknown/")

        audio_split(uploaded_files[0], isMP3 , sourceDir, chunk_length_ms)
        training_result = model_train(uploaded_files[0],trainSourceDir,destDir)
        audio_split(uploaded_files[1], isMP3 , sourceDir, chunk_length_ms)
        training_result = model_train(uploaded_files[1],trainSourceDir,destDir)
        responseJson = {}
        appurl = request.url.split("/compare")

        if training_result == "Modelling completed":
            print("*********",uploaded_files[1])
            flag, _similarityProbScore, _compareMatch = compare_test(uploaded_files,sourceDir,destDir)
            responseJson = {}
            confidenceThreshold = 0.75

            if(_similarityProbScore == 1):
                responseJson = jsonify(
                                status = 200,
                                message = _compareMatch
                            )

            else:
                responseJson = jsonify(
                                status = 200,
                                message = _compareMatch,
                                similarityProbScore =format(_similarityProbScore, '.8f')

                            )
            
            return responseJson
    return '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
          rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <hr/>
      <div>
      <h3>Enter URL and Upload a file to Compare</h3><br/>
      <form action="" method="post" enctype="multipart/form-data">
        <p>URL : <input type="text" name="filelink"><br/></p>
        <p><input type=file name=file><br />
        <input type="submit" value="Upload" >
      </form>
      </div>
    </div>
  </body>
</html>
'''

@app.route('/compare', methods=['GET', 'POST'])
def compare_mode():
    return render_template('compare.html')

@app.route('/handle_compare', methods=['GET', 'POST'])
def handle_compare():
    compareMode = request.form['compareMode']
    if compareMode=="File Mode":
        return redirect('/filecompare')
    elif compareMode=="URL Mode":
        return redirect('/urlcompare')
    else:
        return redirect('/mixedcompare')
    return "Error: Choose the right mode"
    

#if __name__ == "__main__":
#app.run(debug=True)