import file_ops

data = file_ops.read_csv("final.csv", make_float=False)

segments = []

current_trial = ""
for i, row in enumerate(data):
    trial = row["trial"]
    if not trial == current_trial:
        current_trial = trial
        segments.append(i)
segments.append(len(data)-1)

data_out = []

for i in range(len(segments)-1):
    start = segments[i]
    end = segments[i+1]
    slice = data[start:end]

    slice_gx = [float(row["graph_x"]) for row in slice]
    slice_gy = [float(row["graph_y"]) for row in slice]

    gx_avg = sum(slice_gx)/len(slice_gx)
    gy_avg = sum(slice_gy)/len(slice_gy)

    gx_min = abs(min(slice_gx)-gx_avg)
    gy_min = abs(min(slice_gy)-gy_avg)

    gx_max = abs(max(slice_gx)-gx_avg)
    gy_max = abs(max(slice_gy)-gy_avg)

    gx_rr = (gx_max-gx_min)/gx_avg
    gy_rr = (gy_max-gy_min)/gy_avg
    
    data_out.append({
                        "graph x avg": gx_avg,
                        "graph y avg": gy_avg,
                        "graph x min": gx_min,
                        "graph y min": gy_min,
                        "graph x max": gx_max,
                        "graph y max": gy_max,
                        "graph x rr": gx_rr,
                        "graph y rr": gy_rr
                    })    

file_ops.write_csv(data_out,"trial_ends.csv")

