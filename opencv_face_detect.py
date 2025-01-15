
#!/usr/bin/python3

import cv2
import time

from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

face_detector = cv2.CascadeClassifier("/home/kiet/FACE-TRACKING-SYSTEM/Face_Tracking_System(PYTHON CODE)/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))

picam2.start()

start_time = time.time()
frame_count = 0

total_frames = 0
correct_predictions = 0

ground_truth_present = True

picam2.set_controls({"FrameDurationLimits": (40000, 40000)})

while True:
    im = picam2.capture_array()
    frame_count +=1

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

#print("Number of Faces detected: ", len(dafFace))
    #teks = "Number of Faces Detected = " + str(len(faces))
    total_frames += 1
    if(len(faces) > 0) == ground_truth_present:
        correct_predictions += 1
        
    accuracy = (correct_predictions / total_frames * 100) if total_frames > 0 else 0 


    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im, f"Accuracy: {accuracy:.2f}%", (0, 30), font, 1, (255, 0, 0), 1)

    cv2.imshow("Results", im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        buttonispressed = True
        break
    if time.time() - start_time > 2:
        fps = frame_count / (time.time() - start_time)
        print(f"Current FPS: {fps:.2f}")
        start_time = time.time()
        frame_count = 0
