import os
from PIL import Image, ImageDraw
from azureFaceAPI import azure_detect_from_local_file, draw_rectangles_and_save, getRectangle, face_client

# Detect faces
# path to image with single face
single_face_image_path = 'images/jfk/jfk.jpg'
single_image_name = os.path.basename(single_face_image_path)

detected_faces = azure_detect_from_local_file(single_face_image_path)

# Display the detected face ID in the first single-face image.
# Face IDs are used for comparison to faces (their IDs) detected in other images.
print('Detected face ID from', single_image_name, ':')
for face in detected_faces: 
    print (face.face_id)
print()

# Save this ID for use in Find Similar
first_image_face_ID = detected_faces[0].face_id

# Open the image and initialize a 2D drawing interface
# Draw a red rectangle around the first detected face
print('Drawing rectangle around detected face...')
draw_rectangles_and_save(single_face_image_path, 'Face Recognition', detected_faces)

# Detect the faces in an image that contains multiple faces
# Each detected face gets assigned a new ID
multi_face_image_path = 'images/jfk/family.jpg'
multi_image_name = os.path.basename(multi_face_image_path)

detected_faces2 = azure_detect_from_local_file(multi_face_image_path)

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