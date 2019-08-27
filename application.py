from app import app
import os

def createFolder(directory):
    print('******** Upload directory creating ...')
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print('******** ' + directory + ' Directory created successfully ...')
    except OSError:
        print ('********** Error: Creating directory' +  directory)
        

# Example
createFolder('./uploads/')
createFolder('./audio_sources/')
createFolder('./Speakers_models/')
createFolder('./test_samples/')
if __name__ == "__main__":
    #app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
    app.run(debug=True)