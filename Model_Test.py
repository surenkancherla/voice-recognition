import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from Feature_Extraction import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
import sklearn.mixture.gaussian_mixture
import math


def test_sample(path,sourceDir,destDir):
    
    """
    #Path to audio files to be tested
    source   = "test_samples/"   

    #Path where trained models are to be saved
    modelpath = "Speakers_models/"
    """

    gmm_files = [os.path.join(destDir,fname) for fname in 
              os.listdir(destDir) if fname.endswith('.gmm')]

    #Load the Gaussian  Models
    models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
              in gmm_files]
    path=path.split(".")[0] + ".wav"

    #Reading the test audio file & extracting features
    sr,audio = read(sourceDir + path)
    vector   = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 
    
    #Checking with each model one by one

    for i in range(len(models)):
        gmm    = models[i] 
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        
    winner = np.argmax(log_likelihood)

    probs = np.exp(log_likelihood) / (np.exp(log_likelihood)).sum()
    print("PROBS=",probs)
    print("*************WINNER***********=",probs[winner])
    confidence=probs[winner]
    print("\tDetected as - ", speakers[winner])
    print("LOGS=",log_likelihood)
    print("WINNER=",winner)
    print("SPEAKERS=",speakers)
    
    time.sleep(1.0)

    flag = False
    speaker = None

    if winner >= 0:
        flag = True
        speaker = speakers[winner]

    return flag, speaker, confidence

def compare_test(filenames,sourceDir,destDir):
    
    """
    #Path to audio files to be tested
    source   = "test_samples/"   

    #Path where trained models are to be saved
    modelpath = "Speakers_models/"
    """
    gmm_files=[]
    print("FILENAMES ", filenames)
    testgmmFile1=filenames[0].split(".wav")[0] + ".gmm"
    testgmmFile2=filenames[1].split(".wav")[0] + ".gmm"
    testwavFile=filenames[1]
    gmm_files.append(destDir + testgmmFile1)
    gmm_files.append(destDir + testgmmFile2)

    #Load the Gaussian  Models
    models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
              in gmm_files]
    testwavFile=testwavFile.split(".")[0] + ".wav"
    print("TEST WAV FILE ", testwavFile)

    #Reading the test audio file & extracting features
    sr,audio = read(sourceDir + testwavFile)
    """
    vector = np.asarray(())
    y2, sr2 = librosa.load("./Unknown/" + testwavFile)
    vector = librosa.feature.mfcc(y2,sr2)   
    """
    vector   = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 
    
    ##Checking with each model one by one

    for i in range(len(models)):
        gmm    = models[i] 
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        
    winner = np.argmax(log_likelihood)

    probs = np.exp(log_likelihood) / (np.exp(log_likelihood)).sum()
    confidence=probs[winner]
    print("@@@@@@ PROBS",probs)
    print("LOGS=",log_likelihood)
    
    time.sleep(1.0)

    flag = False
    speaker = None

    p1=log_likelihood[0]
    p2=log_likelihood[1]
    if(abs(p1-p2))<=3:
        compareMatch="Match Found"
        similarityprob_score=1
    else:
        compareMatch="Match Not Found"
        similarityprob_score=probs[0]

    if winner >= 0:
        flag = True
        speaker = speakers[winner]

    return flag, similarityprob_score, compareMatch