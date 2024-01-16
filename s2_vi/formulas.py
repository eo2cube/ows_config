def ndvi(data):
    castdata = data.astype("float32")
    return (castdata["nir"] - castdata["red"]) / (castdata["nir"] + castdata["red"])

def ndvi_diff(data):
    datetime = data.time
    return ndvi(data) - 0.2195341375  # value applicable for combination of date and crop

def evi(data):
    castdata = data.astype("float32")
    normdata = castdata / 10000
    G = 2.5
    C1 = 6
    C2 = 7.5
    L = 1
    return G * ((normdata["nir"] - normdata["red"]) / (normdata["nir"] + C1*normdata["red"] - C2*normdata["blue"] + L))

def evi_diff(data):
    datetime = data.time
    return evi(data) - 0.157540205  # value applicable for combination of date and crop