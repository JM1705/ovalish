import file_ops
import json


ANALYSED_DIR = "analysed/"
ECC_MAX = 0.4
ECC_MIN_LEN = 20
DT_MAX = 40
SKIP_AFTER_ERROR = 200


def main_process(file):
    data = file_ops.read_csv(ANALYSED_DIR+file)

    good_parts = [[]]
    last_false = 100000000
    for i, row in enumerate(data):
        ecc = row["eccentricity"]
        dt = row["delta time (ms)"]
        if ecc < ECC_MAX and dt < DT_MAX:
            if last_false == SKIP_AFTER_ERROR:
                good_parts.append([])
            if last_false >= SKIP_AFTER_ERROR:
                good_parts[-1].append(row)
            last_false += 1
        else:
            last_false = 0

    # print(json.dumps(good_parts, indent=4))

    for i, part in enumerate(good_parts):
        for j, row in enumerate(part):
            good_parts[i][j]["file"] = file
            good_parts[i][j]["video segment"] = i

    long_good_rows = []
    for i, part in enumerate(good_parts):
        if len(part) >= ECC_MIN_LEN:
            long_good_rows.append(part)


    return long_good_rows
    


def main():
    # files = file_ops.list_csv(ANALYSED_DIR)
    files = [
        "VID_20240909_124830.mp4.csv",
        "VID_20240906_130408.mp4.csv",
        "VID_20240906_124910.mp4.csv",
        "VID_20240906_131255.mp4.csv"
    ]
    all_data = []
    for file in files:
        all_data += main_process(file)

    for i, part in enumerate(all_data):
        for j, row in enumerate(part):
            all_data[i][j]["trial"] = i+1

    final_data = []

    for part in all_data:
        for row in part:
            final_data.append(row)

    file_ops.write_csv(final_data, "final.csv")

main()

    
