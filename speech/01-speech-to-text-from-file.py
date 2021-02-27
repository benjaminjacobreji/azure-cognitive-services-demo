import os
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

done = False

output = []

def stop_cb(evt):
    """Callback to stop continuous recognition upon receiving an event `evt`"""
    speech_recognizer.stop_continuous_recognition()
    global done
    done = True

# Create an instance of a speech config with the provided subscription
# key and service region. Then create an audio configuration to load
# the audio from file rather than from microphone

# A recognizer is then created with the given settings.

speech_key, service_region = os.getenv('SPEECH_RESOURCE_KEY'), "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

filename=input("Enter the path to an audio file(.wav) : ")

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
    print("Enter the name of the output file : ")
    name = input()
    out = open(f'./Output/{name}.txt', 'w')
    for sentence in output:
        out.write(sentence + "\n")
    out.close()