VEL_COMPARE_DIST = 6 # frames
# PIXELS_PER_METER = 1570
STRING_LENGTH = 21.8/100 # m

with open("data_files.txt", "r") as f:
    files = f.read().rstrip().split("\n")

with open("ruler_length_data.txt", "r") as f:
    ppms = f.read().rstrip().split("\n")
    ppms = [float(ppm) for ppm in ppms]

for n, file in enumerate(files):
    print(file)
    with open(file, "r") as f:
        rows= f.read().rstrip().split("\n")

    rows = [item.split(",") for item in rows]

    filename = file.split("/")[-1]

    titles = rows[0] + ["ti-t(i-5) (ms)","pixels/meter", "string length (m)", "radius (m)","xi-x(i-5) (pixels)", "yi-y(i-5) (pixels)", "speed (m/s)", "experimental g (N/kg)"]
    data_rows = rows[1:]

    new_data_rows = []

    for k, item in enumerate(data_rows):
        item = item + [0,0,0,0,0,0,0,0]
        if k > VEL_COMPARE_DIST/2 and k < len(data_rows) - VEL_COMPARE_DIST/2 -1:
            # d_x = float(item[2]) - float(data_rows[k-VEL_COMPARE_DIST][2])
            # print(data_rows[0])
            # exit()
            # print(round(k+VEL_COMPARE_DIST/2))
            # print(k-VEL_COMPARE_DIST/2)
            # exit()
            d_x = float(data_rows[round(k+VEL_COMPARE_DIST/2)][2]) - float(data_rows[round(k-VEL_COMPARE_DIST/2)][2])
            # d_y = float(item[3]) - float(data_rows[k-VEL_COMPARE_DIST][3])
            d_y = float(data_rows[round(k+VEL_COMPARE_DIST/2)][3]) - float(data_rows[round(k-VEL_COMPARE_DIST/2)][3])
            d_pos = (d_x**2 + d_y**2)**0.5
            d_t = float(data_rows[round(k+VEL_COMPARE_DIST/2)][1]) - float(data_rows[round(k-VEL_COMPARE_DIST/2)][1])
            radius_pixels = ((float(item[2]) - float(item[5]))**2 + (float(item[3]) - float(item[6]))**2)**0.5

            radius = radius_pixels/ppms[n]
            item[-8] = d_t
            item[-7] = ppms[n]
            item[-6] = STRING_LENGTH
            item[-5] = radius
            item[-4] = d_x
            item[-3] = d_y
            speed = d_pos/(ppms[n]*d_t/1000)
            item[-2] = speed
            if not speed == 0:
                h2 = STRING_LENGTH**2 - radius**2 # Height squared
                if h2 > 0:
                    g = (speed**2)*(h2**0.5)/radius**2
                    item[-1] = g

        new_data_rows.append(item)

    all_data = [titles] + new_data_rows

    csv_rows = []
    for i, row in enumerate(all_data):
        csv_rows.append(",".join([str(item) for item in row]))

    csv = "\n".join(csv_rows)

    with open(f"analyzed/{filename}", "w") as f:
        f.write(csv)




        
    
