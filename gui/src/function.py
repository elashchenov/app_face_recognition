import cv2
import os
import base64
import time
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np

work_path = os.path.join("/Users/lashchenov/university/ТРКПО Маслаков/app_access_with_Face_Recognition/gui", 'src')

def add_photo(pbar):
    face_cascade = cv2.CascadeClassifier(os.path.join(work_path, 'haarcascade_frontalface_default.xml'))
    cam = cv2.VideoCapture(get_video_stream())
    cv2.namedWindow("Save New Face")
    time.sleep(2)

    img_counter = 0

    i, j = 0, 0

    num = 200
    list_binary_images_train = []
    list_binary_images_test = []
    while img_counter < num:
        ret, frame = cam.read()
        cv2.imshow("Save New Face", frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.2, 5)

        if not ret:
            break
        k = cv2.waitKey(1)
        for x, y, w, h in face:

            # Get face in grayscale
            roi_gray = gray[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), 1)
            gray_face = cv2.resize(roi_gray, (128, 128))

            # Capture only 20% of the face
            # if i == 5:
            img_bytes = cv2.imencode('.png', gray_face)[1].tostring()
                # Split data in train and test set to be 80%/20%
            # cv2.imwrite(os.path.join(work_path,'images', 'face.png'), gray_face)
            # with open(os.path.join(work_path,'images', 'face.png'), 'rb') as f:
            #     img_bytes = f.read()
            if img_counter % 5 == 0:
                list_binary_images_test.append(base64.b64encode(bytes(str(img_bytes),"utf-8")).decode('ascii'))
            else:
                list_binary_images_train.append(base64.b64encode(bytes(str(img_bytes),"utf-8")).decode('ascii'))

            # os.system("cls")
            # time.sleep(0.1)
            pbar.setValue(100*(img_counter+1)//num)
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    
    return list_binary_images_train, list_binary_images_test

def openResource(id_user):
    
    # train the model on those images
    classifier = os.path.join(work_path,"haarcascade_frontalface_default.xml")
    model = os.path.join(work_path,"models",id_user,"model_face.h5")

    def get_legend(class_arg):
        label_list = ['sergei']
        # get label from prediction
        label = label_list[class_arg]
        # create color from each label
        coef = float(class_arg + 1)
        color = coef * np.asarray((20,30,50))
        return color, label
    
    def process_face(roi_gray):
        # resize input model size
        roi_gray = cv2.resize(roi_gray, (128, 128))
        roi_gray = roi_gray.astype("float") / 255.0
        roi_gray = img_to_array(roi_gray)
        roi_gray = np.expand_dims(roi_gray, axis=0)

        return roi_gray
    
    face_cascade = cv2.CascadeClassifier(classifier)
    # Keras model was trained using the iPython Notebook

    model = load_model(model)

    """
    Open the webcam recognize the face.
    If face recognized print Access Granted.
    Else if face not recognized after 10 seconds Quit and Print
    Access not granted
    """
    # The program will quit when clicking ESC
    cam = cv2.VideoCapture(get_video_stream())
    cv2.namedWindow("Recognizing Face...")

    # clear Terminal
    # os.system('cls')
    time.sleep(2)
    img_counter = 0
    #prediction = 0

    t_end = time.time() + 10
    # Run this loop for 10 seconds
    access = False
    while time.time() < t_end and access != True:
        ret, frame = cam.read()
        cv2.imshow("Testing existing Face", frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not ret:
            break
        k = cv2.waitKey(1)

        threshold = 0.55
        # Get faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_face = gray[y:y + h, x:x + w]
            roi_face = process_face(roi_face)
            prediction = model.predict(roi_face)
            print(prediction[0][0])
            
            # Get label and color from prediction
            color, label = get_legend(np.argmax(prediction))

            cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            if(prediction[0][0] >= threshold):
                print(prediction[0][0])
                cam.release()
                cv2.destroyAllWindows()
                return True
        
    cam.release()
    cv2.destroyAllWindows()  
    if (time.time() > t_end):
        return False


def get_video_stream():
    return 0
    

