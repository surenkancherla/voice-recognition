import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from Feature_Extraction import extract_features
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

#path to training data
source   = "test_samples/"   

#path where training speakers will be saved i.e GMM files
modelpath = "test_samples/train_samples/"

gmm_files = [os.path.join(modelpath,fname) for fname in 
              os.listdir(modelpath) if fname.endswith('.gmm')]

#Load the Gaussian gender Models
models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
              in gmm_files]

error = 0
total_sample = 0.0

test_file = "test-files-list.txt"        
file_paths = open(test_file,'r')

# Read the test directory and get the list of test audio files 
for path in file_paths:   

    total_sample += 1.0
    path = path.strip()   
    print("Current Speaker audio file : ", path)
    sr,audio = read(source + path)
    vector   = extract_features(audio,sr)

    log_likelihood = np.zeros(len(models)) 

    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()

    winner = np.argmax(log_likelihood)
    print("\tIdentified as - ", speakers[winner])

    checker_name = path.split(".")[0]
    if speakers[winner] != checker_name:
        error += 1
        time.sleep(1.0)

print(error, total_sample)
accuracy = ((total_sample - error) / total_sample) * 100

print("The Accuracy Percentage for the current testing performance with MFCC + GMM is : ", accuracy, "%")


print(" ************ Successfully completed!!!. **************** ")
