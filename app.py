"""
The flask application package.
"""
from flask import Flask
from pydub import AudioSegment
import os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

wsgi_app = app.wsgi_app #Registering with IIS


os.environ["PATH"]+="/Users/cb/voice-recognition/voice-recognition/ffmpeg"

AudioSegment.converter = "/Users/cb/voice-recognition/voice-recognition/ffmpeg"
AudioSegment.ffmpeg = "/Users/cb/voice-recognition/voice-recognition/ffmpeg/ffmpeg"
AudioSegment.ffprobe ="/Users/cb/voice-recognition/voice-recognition/ffmpeg/ffprobe"

#import views
import Speaker_Enrollment
import Speaker_Authentication