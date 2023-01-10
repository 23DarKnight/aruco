import numpy as nm
import cv2
import glob

# Dimensions of the black and white squares on the calibration checkerboard
import numpy as np

cb_width = 9                # NO of corners
cb_height = 6               # No of corners present
cb_square_size = 28         # in mm

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points like (0, 0, 0)
cb_3d_pts = np.zeros((cb_height*cb_width, 3), np.float32)
cb_3d_pts[:,:2] = np.mgrid[0:cb_width, 0:cb_height].T.reshape(-1, 2) * cb_square_size

# Arrays to store object points and image points from all the images
lst_cb_3d_pts = []                  # 3d points in real world space
lst_cb_2d_img_pts = []              # 2d points in image plane

img_lst = glob.glob('*.jpg')

for frame_name in img_lst:
    img = cv2.imread(frame_name)

    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    # If found add obj points, img points (after refining them)
    if ret == True:
        lst_cb_3d_pts.append(cb_3d_pts)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        lst_cb_2d_img_pts.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (cb_width, cb_height), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(lst_cb_3d_pts, lst_cb_2d_img_pts, gray.shape[::-1], None, None)

print("Calibration Matrix: ")
print(mtx)
print("Disortion: ", dist)


# Save calibration data in a npy file
with open('camera_cal.npy','wb') as f:
    np.save(f, mtx)
    np.save(f, dist)
