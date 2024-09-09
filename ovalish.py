import cv2
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import json

with open("video_location", "r") as f:
    videoloc = f.read()
crop_width = 1080
remember = 200

# vc = cv2.VideoCapture(0)
vc = cv2.VideoCapture(videoloc)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

class position_log:
    def __init__(self, max_len=10000):
        self.max = max_len
        self.pos_log = []

    def add_pos(self, pos):
        self.pos_log.append(pos)
        if len(self.pos_log) > self.max:
            self.pos_log.pop(0)

    def get_pos_history(self, count):
        if len(self.pos_log) > count:
            return self.pos_log[-count+1:]
        return self.pos_log

pos_log = position_log()

def crop_square_centre(img, width):
    assert width <= img.shape[0]
    assert width <= img.shape[1]
    
    centre = (img.shape[0]/2, img.shape[1]/2)
    bounds = [centre[0]-width/2, centre[0]+width/2, centre[1]-width/2, centre[1]+width/2]
    for i, coord in enumerate(bounds):
        bounds[i] = round(coord)
    cropped = img[bounds[0]:bounds[1], bounds[2]:bounds[3]]
    return cropped

def aruco_centre_coord(corners):
    if len(corners) > 1:
        print("more than one corner detected, choosing first one")
    corner = corners[0]
    centre = (corner[0][0]+corner[0][2])/2
    centre = (round(centre[0]), round(centre[1]))
    return centre

def draw_path_line(imgin, pos_log, length):
    log = pos_log.get_pos_history(length)
    for i in range(len(log)-1):
        intp = (len(log)-2-i)/(len(log)-1)
        pos1 = log[i]
        pos2 = log[i+1]
        imgin = cv2.line(imgin, pos1, pos2, (255,255*intp,255*intp), 2)
    return imgin

def draw_ellipse_box(imgin, pos_log, length):
    log = pos_log.get_pos_history(length)
    eccentricity = 1
    if len(log) >= 5:
        ellipse_data = cv2.fitEllipse(np.array(log))
        centre = (round(ellipse_data[0][0]), round(ellipse_data[0][1]))
        axes = (round(ellipse_data[1][0]/2), round(ellipse_data[1][1]/2))
        cv2.ellipse(imgin, centre, axes, ellipse_data[2], 0, 360, (0, 255, 0), 2)

        eccentricity = ellipse_eccentricity(ellipse_data)
        return imgin, eccentricity, (ellipse_data[0][0], ellipse_data[0][1]), (ellipse_data[1][0], ellipse_data[1][1]), ellipse_data[2]
    return imgin, eccentricity, (0,0),(0,0),0

def ellipse_eccentricity(ellipse_data):
    axes = ellipse_data[1]
    semi_major = max(axes)/2
    semi_minor = min(axes)/2
    if not semi_major == 0: 
        eccentricity = (1 - (semi_minor/semi_major)**2)**0.5
        return eccentricity
    return 1

def half_scale(img):
    new_img = []
    for i, row in enumerate(img):
        new_row = []
        for j, pixel in enumerate(row):
            if j%2==0:
                new_row.append(pixel)
        if i%2==0:
            new_img.append(np.array(new_row))
    return np.array(new_img)


def aruco_loop_process():
    success, img = vc.read()
    if success:
        processing = crop_square_centre(img, crop_width)
        
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(processing, aruco_dict)
        if len(corners) > 0:
            centre = aruco_centre_coord(corners)
            pos_log.add_pos(centre)
            processing = cv2.circle(processing, (round(centre[0]), round(centre[1])), 10, (255,255,0),2)

        processing = draw_path_line(processing, pos_log, remember)

        processing, eccentricity, ellipse_centre, ellipse_axes, ellipse_rotation = draw_ellipse_box(processing, pos_log, remember)
        processing = cv2.putText(processing, f"Eccentricity: {round(eccentricity, 4)}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        res = (round(processing.shape[0]/2), round(processing.shape[1]/2))

        img_view = cv2.resize(processing, res, interpolation = cv2.INTER_NEAREST)

        cv2.imshow("ovalish_track output", img_view)

        t = vc.get(cv2.CAP_PROP_POS_MSEC)
        frame = vc.get(cv2.CAP_PROP_POS_FRAMES)

        if len(corners) > 0:
            frame_stats = [
                round(frame),
                t,
                centre[0],
                centre[1],
                eccentricity,
                ellipse_centre[0],
                ellipse_centre[1],
                ellipse_axes[0],
                ellipse_axes[1],
                ellipse_rotation
            ]
            log.append(frame_stats)
        print(f"time: {t/1000}", end="\r")
    return success

log = [
    [                
        "frame",
        "time (ms)",
        "x (pixels)",
        "y (pixels)",
        "eccentricity",
        "ellipse centre x (pixels)",
        "ellipse centre y (pixels)",
        "ellipse major axis",
        "ellipse minor axis",
        "ellipse rotation"
    ]
]

iter = 0
while True:
    if not aruco_loop_process():
        break
    iter+=1
    cv2.waitKey(10)

print("\ndone")

with open("data/data.csv", "w") as f:
    csv = "\n".join([",".join([str(item) for item in row]) for row in log])
    f.write(csv)
    

