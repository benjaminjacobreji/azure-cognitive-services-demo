import os
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# API key and Resource endpoint for Azure Cognitive Services : Vision (Face) API
# Setup a free account with Azure and create resource
KEY = os.getenv('FACE_RESOURCE_KEY')
ENDPOINT = os.getenv('FACE_RESOURCE_ENDPOINT')

# Authenticate the client
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Detect faces
# path to image with single face
single_face_image_path = 'images/test-image-person-group.jpg'
single_image_name = os.path.basename(single_face_image_path)

# Open Image
img = open(single_face_image_path, 'r+b')

# Azure API call
detected_faces = face_client.face.detect_with_stream(image=img, detection_model='detection_03')

# Check if the returned response has detected faces in it
# Raise exception if there is no detected face
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

# Display the detected face ID in the first single-face image.
# Face IDs are used for comparison to faces (their IDs) detected in other images.
print('Detected face ID from', single_image_name, ':')
for face in detected_faces: 
    print (face.face_id)
print()

# # Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return ((left, top), (right, bottom))

print('Drawing rectangle around face...')
img = Image.open(single_face_image_path)
draw = ImageDraw.Draw(img)

# Single Face
# face = detected_faces[0]

# Multiple Face
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')

if not os.path.exists('outputs'):
    os.makedirs('outputs')

img.save(f'outputs/quickstart-result.jpg', format='JPEG')
print(f'Output File: images/outputs/quickstart-result.jpg')