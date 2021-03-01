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
single_face_image_path = 'images/jfk/jfk.jpg'
single_image_name = os.path.basename(single_face_image_path)

# Open Image
image = open(single_face_image_path, 'r+b')

# Azure Cognitive Service Face API Function
detected_faces = face_client.face.detect_with_stream(image=image, detection_model='detection_03')

# Always close opened files
image.close()

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

# Save this ID for use in Find Similar
first_image_face_ID = detected_faces[0].face_id

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return ((left, top), (right, bottom))

# Open the image and initialize a 2D drawing interface
# Draw a red rectangle around the first detected face
# Save image to specified folder
print('Drawing rectangle around detected face...')
image = Image.open(single_face_image_path)
draw = ImageDraw.Draw(image)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')

img_save_folder = f'outputs/Face Recognition'

if not os.path.exists(img_save_folder):
    os.makedirs(img_save_folder)

img_save_path = f'{img_save_folder}/{single_image_name}'
image.save(img_save_path, format='JPEG')
image.close()
print(f'Image Saved in {img_save_path}')
print()


# Face Identification

# Detect the faces in an image that contains multiple faces
# Each detected face gets assigned a new ID
multi_face_image_path = 'images/jfk/family.jpg'
multi_image_name = os.path.basename(multi_face_image_path)

image = open(multi_face_image_path, 'r+b')

detected_faces2 = face_client.face.detect_with_stream(image=image, detection_model='detection_03')
image.close()
# Check if the returned response has detected faces in it
# Raise exception if there is no detected face
if not detected_faces:
    raise Exception('No face detected from image {}'.format(multi_image_name))

# Search through faces detected in group image for the single face from first image.
# First, create a list of the face IDs found in the second image.
second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))

# Next, find similar face IDs like the one detected in the first image.
similar_faces = face_client.face.find_similar(face_id=first_image_face_ID, face_ids=second_image_face_IDs)
if not similar_faces:
    print('No similar faces found in', multi_image_name, '.')

# Print the details of the similar faces detected
else:
    print('Similar faces found in', multi_image_name + ':')
    for face in similar_faces:
        first_image_face_ID = face.face_id
        # The similar face IDs of the single face image and the group image do not need to match, 
        # they are only used for identification purposes in each image.
        # The similar faces are matched using the Cognitive Services algorithm in find_similar().
        face_info = next(x for x in detected_faces2 if x.face_id == first_image_face_ID)
        if face_info:
            image = Image.open(multi_face_image_path)
            image_name = os.path.basename(multi_face_image_path)
            draw = ImageDraw.Draw(image)
            for face in detected_faces:
                draw.rectangle(getRectangle(face_info), outline='green', width=2)

            img_save_folder = f'outputs/Face Recognition'

            if not os.path.exists(img_save_folder):
                os.makedirs(img_save_folder)

            img_save_path = f'{img_save_folder}/{image_name}'
            image.save(img_save_path, format='JPEG')
            image.close()
            print(f'Image Saved in {img_save_path}')