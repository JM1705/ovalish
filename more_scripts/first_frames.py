import cv2

with open("video_files.txt") as f:
    files = f.read().rstrip().split("\n")


ppms = []
for file in [files[1]]:
# for file in files:
    print(f"{file.split("/")[-1]}")

    vc = cv2.VideoCapture(file)

    for i in range(100):
        success,img = vc.read()

    cv2.imshow("find ruler ends 20cm", img)

    cv2.waitKey(0)

    x1=int(input("left end x:"))
    y1=int(input("left end y:"))
    x2=int(input("left end x:"))
    y2=int(input("left end y:"))

    dx = x1-x2
    dy = y1-y2

    pixel_dist = (dx**2+dy**2)**0.5
    print(pixel_dist)
    pixels_per_metre = pixel_dist/0.2 # 0.2 is 20cm

    ppms.append(str(pixels_per_metre))

with open("ruler_length_data.txt", "w") as f:
    f.write("\n".join(ppms))
    

