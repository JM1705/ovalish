import json 

def read_csv(path, make_float=True):
    with open (path, "r") as f:
        rows = f.read().rstrip().split("\n")
        rows = [[item.strip() for item in row.split(",")] for row in rows]
        titles = rows[0]
        data = rows[1:]
        if make_float:
            data = [[float(item) for item in row] for row in data]        

        dict_data = []
        for row in data:
            row_dict = {}
            for i, item in enumerate(row):
                row_dict[titles[i]] = item
            dict_data.append(row_dict)

        # list of dicts with key=name and data=data
        return dict_data

def write_csv(data, path):
    with open(path, "w") as f:
        new_data = [[item for item in data[0]]]
        new_data += [[str(row[item]) for item in row] for row in data]
        csv_string = "\n".join([",".join(row) for row in new_data])
        f.write(csv_string)          

def list_csv(path):
    import os
    files = os.listdir(path)
    csvs = [file for file in files if file.endswith(".csv")]
    return csvs

def read_cache(path):
    with open(path, "r") as f:
        cache = json.loads(f.read())
    return cache
