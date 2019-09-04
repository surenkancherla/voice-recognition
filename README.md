# Speaker Registration and Verification

	A Python based Web & REST API built on Flask web framework. 

	OBJECTIVES: 
	Speaker registration is used for recognizing or identifying from persons individual sound by machine learning. 

# Requirements
	Python 3.7+

# Pre-requisites
	This application requires an FFMPEG MP3 to WAV file conversion to be installed at system level if you are planning to support MP3 audio files.

# Audio file speficiations 
	Step 2: 16000 kHz 
	Step 3: Mono type
	To record from your computer use # Audacity tool with above specifications. From mobile and tabs by default MP3 audio clip will be generated.

# Switch to virtual environment

	Step 1: python3 -m venv env
	Step 2: source env/bin/activate
	Step 3: run pip install -r requirements.txt

# How to run the app
	Step4: flask run app.py

# Speaker Registration

	Navigate to http://host-name:port/upload path to upload wav audio file.
	
	Step 1: Choose .wav file at present minimum 45 seconds of audio clip is required to get good accuracy.
	Step 2: Enter any unique in the user name input field
	Step 3: Click on Upload

# Speaker Verification

	Navigate to http://host-name:port/authentication-upload path to test.
	Step 1: Choose .wav file at present minimum 15 seconds of audio clip </br>is required to get good accuracy.
	Step 2: Click on Test button


# Reference Papers

# MFCC
--------
http://www.mecs-press.org/ijmecs/ijmecs-v10-n11/IJMECS-V10-N11-3.pdf

https://saiconference.com/Downloads/FTC2017/Proceedings/108_Paper_151-Text_Dependent_Voice_Recognition_System.pdf 

https://www.researchgate.net/publication/50282047_SPEAKER_RECOGNITION_USING_GMM

http://mirlab.org/jang/books/audioSignalProcessing/speakerRecogIntro.asp?title=13-1%20Speaker%20Recognition

http://users.rowan.edu/~ravi/journal/jour_2002_03.pdf

https://www.researchgate.net/publication/258650613_Spoken_Digits_Recognition_using_Weighted_MFCC_and_Improved_Features_for_Dynamic_Time_Warping

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.701.6802&rep=rep1&type=pdf

https://nlp.stanford.edu/courses/lsa352/lsa352.lec6.ppt

http://mirlab.org/jang/books/audioSignalProcessing/speechFeatureMfcc.asp?title=12-2%20MFCC

https://www.researchgate.net/publication/248392078_Convolutive_ICA-Based_Forensic_Speaker_Identification_Using_Mel_Frequency_Cepstral_Coefficients_and_Gaussian_Mixture_Models

# GMM
https://pdfs.semanticscholar.org/8aa5/a355653291bbdad7272d57dbaa7f452668c1.pdf
https://towardsdatascience.com/clustering-based-unsupervised-learning-8d705298ae51
https://towardsdatascience.com/gaussian-mixture-models-explained-6986aaf5a95
https://www.quora.com/What-is-the-difference-between-K-means-and-the-mixture-model-of-Gaussian
https://stephens999.github.io/fiveMinuteStats/intro_to_em.html
https://towardsdatascience.com/gaussian-mixture-models-d13a5e915c8e
https://link.springer.com/article/10.1186/s13634-017-0515-7 - formulas


# Log likelihood
https://towardsdatascience.com/probability-concepts-explained-maximum-likelihood-estimation-c7b4342fdbb1

https://www.hindawi.com/journals/misy/2017/6986391/





