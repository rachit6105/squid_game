import cv2 as cv
from cv2 import aruco
import numpy as np
"""
Camera Matrix (Intrinsic Parameters):
 [[953.20908743   0.         277.93372861]
 [  0.         954.43512104 278.42310266]
 [  0.           0.           1.        ]]
Distortion Coefficients:
 [[-1.12100695e+00  1.29525314e+01 -1.27296008e-02  1.93187973e-02
  -5.15823610e+01]]
"""

cam_mat = np.array([[953.20908743, 0, 277.93372861], [0, 954.43512104, 278.42310266], [0, 0, 1]])
dist_coef = np.array([-1.12100695, 1.29525314, -1.27296008, 1.93187973, -5.15823610])
MARKER_SIZE = 4  
marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create()
cap = cv.VideoCapture(0) #give the server id shown in IP webcam App
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            # calculate the distance
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )
            # for pose of the marker
            # point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            print(ids, "  ", corners)
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()