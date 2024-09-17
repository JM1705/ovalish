import json

CACHE_DIR = "cache.json"
STRING_LENGTH = 21.8 #cm
COM_CODE_DIST = 1.2 #cm
# COM_CODE_DIST = 0 #cm

with open(CACHE_DIR, "r") as f:
    data = json.loads(f.read())

for video in data:
    data[video]["string_length"] = STRING_LENGTH/100
    data[video]["string_length_code"] = (STRING_LENGTH+COM_CODE_DIST)/100
    
with open(CACHE_DIR, "w") as f:
    f.write(json.dumps(data, indent=4))

    
