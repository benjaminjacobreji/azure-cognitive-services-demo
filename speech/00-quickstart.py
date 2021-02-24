import os
import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = os.getenv('SPEECH_RESOURCE_KEY'), "southeastasia"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, )

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# https://docs.microsoft.com/en-us/answers/questions/285441/speech-cognitive-services-authentication-error-401.html
# If you face an error, there is something wrong with Azure, follow the above for updates

print("Speak into your microphone")
result = speech_recognizer.recognize_once_async().get()
# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
