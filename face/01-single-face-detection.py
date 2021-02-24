import os
from PIL import Image, ImageDraw
from azureFaceAPI import azure_detect_from_local_file, getRectangle

# path to image with single face
single_face_image_path = 'images/test-image-person-group.jpg'
single_image_name = os.path.basename(single_face_image_path)

detected_faces = azure_detect_from_local_file(image_path=single_face_image_path)

# Display the detected face ID in the first single-face image.
# Face IDs are used for comparison to faces (their IDs) detected in other images.
print('Detected face ID from', single_image_name, ':')
for face in detected_faces: 
    print (face.face_id)
print()

# Open the image and initialize a 2D drawing interface
# Draw a red rectangle around the first detected face
print('Drawing rectangle around face...')
img = Image.open(single_face_image_path)
draw = ImageDraw.Draw(img)
face = detected_faces[0]
draw.rectangle(getRectangle(face), outline='red')

img_save_folder = f'outputs/Single Face Detection'
img_save_path = f'{img_save_folder}/{single_image_name}'

if not os.path.exists(img_save_folder):
    os.makedirs(img_save_folder)

img.save(img_save_path, format='JPEG')
print(img_save_path)