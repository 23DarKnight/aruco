import numpy as np
import cv2
import cv2.aruco as aruco

with open('camera_cal.npy', 'rb') as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
marker_size = 100

cap = cv2.VideoCapture(0)

cam_width = 640
cam_height = 480
cam_fps = 40

cap.set(2, cam_width)
cap.set(4, cam_height)
cap.set(5, cam_fps)


while True:
    ret, frame = cap.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Finding all the aruco markers in the images
    corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners)            # Draw a box around all the detected markers

        # Get pos of all single markers
        rvec_lst_all, tvec_lst_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

        rvec = rvec_lst_all[0][0]
        tvec = tvec_lst_all[0][0]

        # aruco.drawFrameAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 100)

        tvec_str = "x=%4.0f y=%4.0f z=%4.0f"%(tvec[0], tvec[1], tvec[2])
        cv2.putText(frame, tvec_str, (20, 460), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2, cv2.LINE_AA)


    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):break

cap.realease()
cap.destroyAllWindows()