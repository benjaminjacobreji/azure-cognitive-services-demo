import os
from azureFaceAPI import azure_detect_from_local_file, draw_rectangles_and_save

# Detect faces
# path to image with single face
multiple_faces_image_path = 'images/test-image-person-group.jpg'
multiple_image_name = os.path.basename(multiple_faces_image_path)

detected_faces = azure_detect_from_local_file(multiple_faces_image_path)

# Display the detected face ID in the first single-face image.
# Face IDs are used for comparison to faces (their IDs) detected in other images.
print('Detected face ID from', multiple_image_name, ':')
for face in detected_faces: 
    print (face.face_id)
print()

print('Drawing rectangle around face...')
draw_rectangles_and_save(multiple_faces_image_path, 'Multiple Face Detection', detected_faces)