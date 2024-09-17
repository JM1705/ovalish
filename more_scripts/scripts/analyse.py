import file_ops
import json


DATA_DIR = "data/"
ANALYSED_DIR = "analysed/"
CACHE_DIR = "cache.json"
VEL_COMPARE_DIST = 2 # +-frames


def add_delta_measurements(data):
    assert(len(data) > VEL_COMPARE_DIST*2+1)
    for i in range(len(data)):
        if VEL_COMPARE_DIST<=i<len(data)-VEL_COMPARE_DIST:
            i_low = i-VEL_COMPARE_DIST
            i_high = i+VEL_COMPARE_DIST

            d_t = data[i_high]["time (ms)"] - data[i_low]["time (ms)"]
            d_x = data[i_high]["x (pixels)"] - data[i_low]["x (pixels)"]
            d_y = data[i_high]["y (pixels)"] - data[i_low]["y (pixels)"]

            data[i]["delta time (ms)"] = d_t
            data[i]["delta x (pixels)"] = d_x
            data[i]["delta y (pixels)"] = d_y
        else:
            data[i]["delta time (ms)"] = 0
            data[i]["delta x (pixels)"] = 0
            data[i]["delta y (pixels)"] = 0
    return data


def add_ppms(data, filename):
    cache = file_ops.read_cache(CACHE_DIR)
    for i, row in enumerate(data):
        assert filename in cache
        data[i]["20cm ruler length (pixels)"] = cache[filename]["pixels_per_meter"]/5
        data[i]["pixels/meter"] = cache[filename]["pixels_per_meter"]
    return data


def add_radius(data):
    assert "pixels/meter" in data[0]
    cache = file_ops.read_cache(CACHE_DIR)
    for i, row in enumerate(data):
        x_disp = row["ellipse centre x (pixels)"] -row["x (pixels)"]
        y_disp = row["ellipse centre y (pixels)"] -row["y (pixels)"]
        radius_pixels = (x_disp**2 + y_disp**2)**0.5
        radius = radius_pixels/row["pixels/meter"]
        data[i]["x displacement (m)"] = -x_disp/row["pixels/meter"]
        data[i]["y displacement (m)"] = -y_disp/row["pixels/meter"]
        data[i]["code movement radius (m)"] = radius
    return data


def add_velocity(data):
    assert "pixels/meter" in data[0]
    for i, row in enumerate(data):
        d_x = row["delta x (pixels)"]
        d_y = row["delta y (pixels)"]
        d_t = row["delta time (ms)"]
        ppm = row["pixels/meter"]

        assert not ppm == 0
        dist_m = ((d_x**2 + d_y**2)**0.5)/ppm
        if not d_t == 0:
            speed = dist_m/(d_t/1000)
        else:
            speed = 0

        data[i]["speed (m/s)"] = speed
    return data


def add_string_length(data, filename):
    cache = file_ops.read_cache(CACHE_DIR)
    for i, row in enumerate(data):
        data[i]["string length (m)"] = cache[filename]["string_length"]
        data[i]["pivot to code length (m)"] = cache[filename]["string_length_code"]
        data[i]["mass to code length (m)"] = cache[filename]["string_length_code"] - cache[filename]["string_length"]
    return data


def add_end_length_radius(data): # for calculating the CoM radius from the measured code radius, code dist from pivot and string length
    for i, row in enumerate(data):
        r_c = row["code movement radius (m)"]
        l_s = row["string length (m)"]
        l_c = row["pivot to code length (m)"]
        if not l_c == 0:
            r_s = (r_c*l_s)/l_c
        else:
            r_s = 0

        data[i]["com movement radius (m)"] = r_s
    return data


def add_x_y_for_g(data, filename):
    cache = file_ops.read_cache(CACHE_DIR)
    assert "speed (m/s)" in data[0]
    for i, row in enumerate(data):
        v = row["speed (m/s)"]
        l = row["string length (m)"]
        r = row["com movement radius (m)"]

        if not v==0 and not r==0 and l**2 > r**2:
            # data[i]["graph_x"] = 1/(v**2)
            # data[i]["graph_y"] = ((l**2-r**2)**0.5)/r**2
            data[i]["graph_x"] = 1/(((l**2-r**2)**0.5)/r**2)
            data[i]["graph_y"] = (v**2)
        else:
            data[i]["graph_x"] = 0
            data[i]["graph_y"] = 0
    return data


def data_process(file):
    print(f"analysing {file}")
    filename = file.split(".csv")[0]
    data = file_ops.read_csv(DATA_DIR+file)
    data = add_string_length(data, filename)
    data = add_delta_measurements(data)
    data = add_ppms(data, filename)
    data = add_radius(data)
    data = add_end_length_radius(data)
    data = add_velocity(data)
    data = add_x_y_for_g(data, filename)
    file_ops.write_csv(data, ANALYSED_DIR+file)


def main():
    files = file_ops.list_csv(DATA_DIR)
    for file in files:
        data_process(file)


main()
