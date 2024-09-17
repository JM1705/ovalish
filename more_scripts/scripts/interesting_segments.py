import csv
import json
import file_ops

ECC_MAX = 0.25
ECC_MIN_LEN = 30
ECC_MAX_LEN = 120

ANALYSED_DIR = "analysed/"

files = file_ops.list_csv(ANALYSED_DIR)

main_title = []
main_data = []

for file in files:
    print(file)
    with open(file, "r") as f:
        rows= f.read().rstrip().split("\n")

    filename = file.split("/")[-1]
    
    rows = [[item.strip() for item in row.split(",")] for row in rows]

    title = rows[0]
    rest = [[float(item) for item in row] for row in rows[1:]]

    good_parts = []
    good_rn = False
    for i in rest:
        ecc = i[4]
        if ecc < ECC_MAX:
            if not good_rn:
                good_parts.append([])

            good_parts[-1].append(i)
            good_rn = True
        else:
            good_rn = False

    long_good_parts = []
    for i, part in enumerate(good_parts):
        if len(part) >= ECC_MIN_LEN:
            long_good_parts.append([[filename,"",""]+item for item in part])

    for i, part in enumerate(long_good_parts):
        if len(part) > ECC_MAX_LEN:
            long_good_parts[i] = long_good_parts[i][:ECC_MAX_LEN]
        for j, item in enumerate(long_good_parts[i]):
            long_good_parts[i][j][1] = i

    final_items = []
    for part in long_good_parts:
        for item in part:
            final_items.append(item)
            

    # print(json.dumps(final_items, indent=4))
    print(f"{len(final_items)} frames found in {filename}")

    new_titles = ["File", "Segment number", "trial"]+title
    if main_data == []:
        main_title = new_titles

    main_data += final_items

# print(json.dumps(main_data, indent=4))

current_trial = 0
current_file = ""
current_segment = 0
for i, item in enumerate(main_data):
    if not current_file == item[0] or not current_segment == item[1]:
        current_trial += 1
    main_data[i][2] = current_trial

    current_file = item[0]
    current_segment = item[1]

main_data = [main_title]+main_data
    

csv_rows = []
for i, row in enumerate(main_data):
    csv_rows.append(",".join([str(item) for item in row]))

csv = "\n".join(csv_rows)

with open("master_summary.csv", "w") as f:
    f.write(csv)
    
