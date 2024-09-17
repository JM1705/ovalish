import json

ROOT_DIR = ""
DATA_DIR = "data/"

with open(f"{ROOT_DIR}video_files.txt", "r") as f:
    files = f.read().rstrip().split("\n")

with open(f"{ROOT_DIR}ruler_length_data.txt", "r") as f:
    lengths = f.read().rstrip().split("\n")

main = {}
for i, file in enumerate(files):
    main[f"{file.split("/")[-1]}"] = {"20cm_length":float(lengths[i])}

with open(f"{ROOT_DIR}cache.json", "w") as f:
    f.write(json.dumps(main, indent=4))


    
