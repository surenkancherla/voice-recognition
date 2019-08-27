import subprocess
import os
import glob, sys
from subprocess import Popen, PIPE
from flask import Flask
"""
from pydub import AudioSegment

from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = './ffmpeg/ffmpeg'
#AudioSegment.ffmpeg = "/Users/cb/ffmpeg"
#print("************** ",AudioSegment.converter)
#AudioSegment.converter = which("ffmpeg")
#print("ABC   ",AudioSegment.converter)
#print("****** " ,os.environ)
subprocess.call([AudioSegment.converter, '-i', 'aryan.mp3', 'output.wav'])
import subprocess
#retcode = subprocess.call(['sox', "Aryan.mp3", '--rate 16k', '--bits 16', '--channels 1', "Aryan.wav"])

"""


def getVideoFilesFromFolder(dirPath):
    types = (dirPath+os.sep+'*.avi', dirPath+os.sep+'*.mkv', dirPath+os.sep+'*.mp4', dirPath, dirPath+os.sep+'*.flac', dirPath+os.sep+'*.ogg') # the tuple of file types
    print(dirPath)
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    return files_grabbed

def main(samplingRate,channels):
    files = getVideoFilesFromFolder("./aryan.mp3")
    """samplingRate = int(argv[2])
    channels = int(argv[3])
    """
    for f in files:
        wavPath = 'avconv -y -i  ' + '\"' + f + '\"' + ' -ar ' + str(samplingRate) + ' -ac ' + str(channels) + ' ' + '\"' + os.path.splitext(f)[0] + '\"' + '.wav' 
        os.system(wavPath)



@app.route('/start')
def fun():
    main(8000,1)
    return "Success"
            
#if __name__ == '__main__':
    #main(sys.argv)



#mp3 to wav conversion using ffmpeg 
mp3toWav(filename, replace_filename, "./audio_sources", "./uploads")

mp3toWav(filename, filename.split(".mp3")[0] + ".wav", "./test_samples", "./test_samples")

def mp3toWav(fname, replace_filename, sourceDir, destDir):
    subprocess.call([AudioSegment.converter, '-i', sourceDir + '/' + fname, destDir + '/' +replace_filename])
AudioSegment.from_mp3(sourceDir + "/" + fname).export(destDir + "/" + replace_filename, format="wav")




