# Azure Cognitive Services Demo

Simple demo files for Azure Cognitive Services. More might be added later.

## Credits

Benjamin Jacob Reji ([benjaminjacobreji](https://github.com/benjaminjacobreji))  
Gaurav Gosain ([Gaurav-Gosain](https://github.com/Gaurav-Gosain))  

[Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/) by [Microsoft](https://www.microsoft.com/)
## Usage Guide

1. Make an account at [Microsoft Azure Cloud](https://portal.azure.com/)
2. Create [Face Resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesFace) or [Speech Resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) (Click to get direct links)
3. [Fork this repository](https://github.com/benjaminjacobreji/azure-cognitive-services-demo/fork)
4. Clone repository: ```git clone https://github.com/<your-github-username>/azure-cognitive-services-demo.git```
5. Change directory: ```cd azure-cognitive-services-demo```
6. Make sure ```Python<=3.8*``` as later versions is not supported by Azure packages yet.
7. Install Azure Python packages
   1. ```pip install --upgrade azure-cognitiveservices-vision-face```
   2. ```pip install --upgrade azure-cognitiveservices-speech```
8. Set Enoviroment Variables
   1. Face
      1. FACE_RESOURCE_KEY="key generated in Azure Portal under Face Resource"
      2. FACE_RESOURCE_ENDPOINT="endpoint specified in Azure Portal"
   2. Speech
      1. SPEECH_RESOURCE_KEY="key generated in Azure Portal under Speech Resource"
9. To run Azure Cognitive Services Face API demos
   1. Change to face directory: ```cd face```
   2. Run quickstart example: ```python 00-quickstart.py```
   3. Run face recognition example: ```python 01-face-recognition.py```
10. To run Azure Cognitive Services Face API demos
    1. Change to speech directory: ```cd speech``` or ```cd ../speech```
    2. Run quickstart example: ```python 00-quickstart.py```
    3. Run sppech-to-text example: ```python 01-speech-to-text-from-file.py```
    4. Run text-to-speech example: ```python 02-text-to-speech.py```
