import cv2
import numpy as np

# Define chessboard size
chessboard_size = (5,4)

# Prepare object points (3D coordinates of the chessboard corners in real-world space)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []  # 3D points in real-world space
imgpoints = []  # 2D points in image plane

# Open webcam
cap = cv2.VideoCapture(0)

frame_count = 0
while frame_count < 20:  # Collect 20 valid chessboard images
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        print(f"Frame {frame_count} captured.")

        # Draw and display the corners
        cv2.drawChessboardCorners(frame, chessboard_size, corners, ret)
        frame_count += 1

    cv2.imshow('Calibration', frame)

    # Press 'q' to exit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Perform calibration if enough images are collected
if len(objpoints) > 10:
    ret, camera_matrix, distortion_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    print("Camera Matrix (Intrinsic Parameters):\n", camera_matrix)
    print("Distortion Coefficients:\n", distortion_coeffs)
else:
    print("Not enough valid frames captured for calibration.")
