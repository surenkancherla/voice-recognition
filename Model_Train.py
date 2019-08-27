import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from sklearn import mixture
from Feature_Extraction import extract_features
import warnings   
import wave,struct      
warnings.filterwarnings("ignore")


def model_train(rfname,sourceDir,destDir,):
    """source   = "./Unknown/"   
    dest = "./Unknown/"
    """
    audiosegment_splitcounter = 15
    count = 1
    features = np.asarray(())
    for i in range(0, audiosegment_splitcounter-1):
        _fileNameArr = rfname.split(".")
        tempFileName = _fileNameArr[0] + "_" + str(i) +"."+ _fileNameArr[1]
        if tempFileName in os.listdir(sourceDir):
            # Read the audio
            sample_rate,audio = read(sourceDir + tempFileName)
            count = count + 1
            # Extract 40 dimensional MFCC & delta MFCC features
            vector   = extract_features(audio,sample_rate)
            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
        # When features of 15 files of speaker are generated, then train the model   
    if count == audiosegment_splitcounter:    
        gmm = GaussianMixture(n_components = 16, covariance_type='diag',n_init = 3)
        gmm.fit(features)
        # Dumping the trained gaussian model
        picklefile = rfname.split(".")[0] + ".gmm"
        cPickle.dump(gmm,open(destDir + picklefile,'wb'))
        print ('Modeling completed for speaker:',picklefile," with data point = ",features.shape  )  
        features = np.asarray(())
        count = 0
    return "Modelling completed"

