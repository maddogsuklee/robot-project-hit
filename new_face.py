import cv2
import time
from recognition_module import RecognitionClass


def add_face(new_name):
    # init recognition class
    reco = RecognitionClass()

    if reco.is_known_name(new_name):
        return "name in used - Choose a different name"

    # Initialize face recognition variables
    face_locations = []
    face_names = []
    # Initialize Video Capture
    videostream = cv2.VideoCapture(0)
    
    # Frame buffer equal to 1
    videostream.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # A unknown face counter is found flag
    frame_counter = 0
    frame_counter_limit = 1

    while frame_counter < frame_counter_limit:
        time1 = time.time()
        # Grab frame from video stream
        ret, frame = videostream.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # find all faces and check if they match to known faces.
        face_locations, face_names = reco.find_faces_and_match(rgb_small_frame)

        # Scale back up faces and draw box around them
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # save new face 
            if name == "Unknown":
                cv2.imwrite('temp_img/temp.jpg', frame[top-10:bottom+10, left-10:right+10])
                frame_counter += 1 

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            
        # Calculate fps
        frame_rate_calc = (1/(time.time()-time1))
        # Add fps
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        # add comment below
        cv2.putText(frame, 'press on q to close', (30, 460), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)

        # show new Frame
        cv2.imshow('frame', frame)

        # break when q key pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # stop video stream
    videostream.release()

    # close all cv2 windows
    cv2.destroyAllWindows()

    # show added face and save image. also call is name. 
    if new_name != "" and frame_counter >= frame_counter_limit:

        img = cv2.imread("temp_img/temp.jpg")
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        # Convert the image to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if not reco.is_face_encoded(rgb_small_frame):
            return "bad image"

        reco.add_face_and_voice(new_name)
        img = cv2.imread("/home/pi/My_robot/face_and_voice/"+new_name+".jpg")
        
        cv2.imshow(new_name, img)
        reco.voice_announcement(new_name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return "face added"

    return ""



