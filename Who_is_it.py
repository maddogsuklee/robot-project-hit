# Who is it file #
import cv2
import time
from recognition_module import RecognitionClass


def find_face_def():
    # init recognition class
    reco = RecognitionClass()

    # Initialize face recognition variables
    face_locations = []
    face_names = []

    # Initialize Video Capture
    videostream = cv2.VideoCapture(0)
    # Frame buffer equal to 1
    videostream.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # A known face is found flag
    known_face_found = False

    while not known_face_found:
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
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        # Calculate fps
        frame_rate_calc = (1/(time.time()-time1))
        # Add fps
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        # stop video when recognize someone known.
        if (face_locations != []) and (any(name != "Unknown" for name in face_names)):
            known_face_found = True
            
        # add comment below
        cv2.putText(frame, 'press on q to close', (30, 460), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)

        # show new Frame
        cv2.imshow('frame', frame)

        # say names
        if known_face_found:
            for name in face_names:
                if name != "Unknown":
                    reco.voice_announcement(name)

        # break when q key pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # stop video stream
    videostream.release()

    # freeze last frame
    while known_face_found:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close all cv2 windows
    cv2.destroyAllWindows()
    
    return 

