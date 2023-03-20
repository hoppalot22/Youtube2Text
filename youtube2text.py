from pytube import YouTube
from vosk import Model, KaldiRecognizer
import sys
import time
import os
import wave
import json
import subprocess




CURR_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\downloads"

def Download(link):
    yt = YouTube(link)
    print(f"Downloading '{link}'...")
    #time.sleep(0.5)
    audio = yt.streams.filter(only_audio = True)[0]
    return audio.download(CURR_DIR)
    # try:
        # audio.download()
    # except:
        # print("An error has occurred")
    # print("Download is completed successfully")

def convert2wav(inFileName):
    print("Converting to WAV format")

    outFile = ".".join(inFileName.split(".")[0:-1])+".wav"
    command = f'ffmpeg -i "{inFileName}" -ac 1 -ar 16000 -vn "{outFile}"'
    subprocess.call(command, shell=True)
    return outFile

def file2text(inFileName):

    initTime = time.time()
    
    title = inFileName.split("\\")[-1].split(".")[0]

    outfileResults = '\\'.join(inFileName.split('\\')[0:-2]) + "\\results\\" + title +"results.json"
    outfileText = '\\'.join(inFileName.split('\\')[0:-2]) + "\\results\\" + title +"text.json"
    outfileRead = '\\'.join(inFileName.split('\\')[0:-2]) + "\\results\\" + title +"text.txt"

    wf = wave.open(inFileName, "rb")

    # initialize a str to hold results
    results = ""
    textResults = []

    # build the model and recognizer objects.
    #model = Model(r"C:\Users\Marc\Documents\AH\Code\Youtube2Text\models\vosk-model-en-us-0.22")
    model = Model(r"C:\Users\Marc\Documents\AH\Code\Youtube2Text\models\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)
    
    chunkSize = 4000
    counter = 0
    numFrames = wf.getnframes()
    chunkLength = chunkSize/wf.getframerate()
    print( chunkLength)
    
    while True:
        counter += 1
        data = wf.readframes(chunkSize)
        print(counter*chunkSize/numFrames*100)
        if (len(data) == 0):
            break
            
        recognizer.AcceptWaveform(data)
            
            
    # process "final" result
    results = recognizer.FinalResult()
    resultDict = json.loads(results)

    wordsPerLine = 14
    textResults = resultDict["text"].split(' ')
    readableResult = []
    line = ''
    for i,word in enumerate(textResults):
        line += word + " "
        if (i+1)%wordsPerLine == 0:
            readableResult.append(line + '\n')
            line = ''
    readableResult.append(line)
    
    print("Writing Results")
    
    # write results to a file
    with open(outfileResults, 'w') as output:
        output.write(results)

    # write text portion of results to a file
    with open(outfileText, 'w') as output:
        output.write(json.dumps(textResults, indent=4))
        
    with open(outfileRead, 'w') as output:
        output.writelines(readableResult)
    
    print ("Complete!")


link = sys.argv[1]
file = Download(link)
wav = convert2wav(file)
file2text(wav)




