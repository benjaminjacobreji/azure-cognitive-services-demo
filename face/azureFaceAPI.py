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

def azure_detect_from_local_file(image_path, detectionModel='detection_03'):
    image_name = os.path.basename(image_path)
    image = open(image_path, 'r+b')

    detected_faces = face_client.face.detect_with_stream(image=image, detection_model=detectionModel)
    image.close()
    # Check if the returned response has detected faces in it
    # Raise exception if there is no detected face
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(image_name))
    else:
        return detected_faces

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return ((left, top), (right, bottom))

def draw_rectangles_and_save(image_path, save_folder_name, detected_faces):
    # Open the image and initialize a 2D drawing interface
    # Draw a red rectangle around the detected faces
    # Save image to specified folder
    image = Image.open(image_path)
    image_name = os.path.basename(image_path)
    draw = ImageDraw.Draw(image)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')

    img_save_folder = f'outputs/{save_folder_name}'

    if not os.path.exists(img_save_folder):
        os.makedirs(img_save_folder)

    img_save_path = f'{img_save_folder}/{image_name}'
    image.save(img_save_path, format='JPEG')
    image.close()
    print(f'Image Saved in {img_save_path}')