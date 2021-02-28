import os
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv() #loads the .env (environment) variables into the python file

# "done" is a boolean to keep track of the stop event of a callback being triggered to stop continuous recognition , inititated to false
done = False

# an array to store the final output from the recognition
output = []

def stop_cb(evt):
    """Callback to stop continuous recognition upon receiving an event `evt`"""
    speech_recognizer.stop_continuous_recognition()
    global done
    done = True

# Create an instance of a speech config with the provided subscription
# key and service region. Then create an audio configuration to load
# the audio from a file rather than from microphone

# A recognizer is then created with the given settings.

speech_key, service_region = os.getenv('SPEECH_RESOURCE_KEY'), "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# The name of the file is stored in a variable

filename=input("Enter the path to an audio file (.wav) : ")

# This if statement just checks if the first character of our input is
# either a ' or a " implying the input file is of format "file.wav" or
# 'file.wav' in which case we remove the enclosing quotes

if(filename[0] in ["'","\""]):
    filename=filename[1:-1]

audio_input = speechsdk.AudioConfig(filename=filename)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

print()

def outputCalled(evt):
    print('{}'.format(evt.result.text))
    print()
    output.append(evt.result.text+ "\n")


# This callback provides the actual transcription.

speech_recognizer.recognized.connect(lambda evt: outputCalled(evt))

# Stop continuous recognition on either session stopped or canceled
# events.

speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start continuous speech recognition, and then perform
# recognition. For long-running recognition we use
# start_continuous_recognition().

speech_recognizer.start_continuous_recognition()

# this loop checks every half a second if the recognition is complete
while not done:
    time.sleep(.5)

print("Do you wish to save the output in a file [Y/N] : ")
choice = input()

if(choice in ['y','Y']):
    name = input("Enter the name of the output file : ")
    out = open(f'./Output/{name}.txt', 'w')
    for sentence in output:
        out.write(sentence + "\n")
    out.close()