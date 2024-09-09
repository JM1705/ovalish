import cv2
import numpy as np

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
tag = np.zeros((256, 256, 1), dtype="uint8")
cv2.aruco.generateImageMarker(arucoDict, 0, 256, tag, 1)
cv2.imwrite("marker.png", tag)
