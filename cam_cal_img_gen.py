import numpy as nm
import cv2, time

cv2.namedWindow("Drone 1")
cv2.moveWindow("Drone 1", 159, -25)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 40)

prev_frame_time = time.time()

cal_img_cnt = 0
frame_cnt = 0

while True:
    ret, frame = cap.read()

    frame_cnt += 1

    if frame_cnt == 30:
        cv2.imwrite("cal_img_"+str(cal_img_cnt)+".jpg", frame)
        cal_img_cnt += 1
        frame_cnt = 0


    new_frame_time = time.time()

    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, "FPS: "+(str(int(fps))), (10, 40), cv2.FONT_HERSHEY_PLAIN, 3, (100, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Drone 1", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

cap.release()

cv2.destroyAllWindows()