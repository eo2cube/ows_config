def ndvi(data):
    castdata = data.astype("float32")
    return (castdata["nir"] - castdata["red"]) / (castdata["nir"] + castdata["red"])

def ndvi_diff(data):
    datetime = data.time
    return ndvi(data) - 0.2195341375  # value applicable for combination of date and crop

def evi(data):
    castdata = data.astype("float32")
    G = 2.5
    C1 = 6
    C2 = 7.5
    L = 1
    return G * ((castdata["nir"] - castdata["red"]) / (castdata["nir"] + C1*castdata["red"] - C2*castdata["blue"] + L))

def evi_diff(data):
    datetime = data.time
    return evi(data) - 0.157540205  # value applicable for combination of date and crop