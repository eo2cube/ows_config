from ows_refactored.s2_vi.utils import get_crop_stats

def ndvi(data):
    castdata = data.astype("float32")
    return (castdata["nir"] - castdata["red"]) / (castdata["nir"] + castdata["red"])

def ndvi_diff(data, croptype):
    mean, _ = get_crop_stats(data, croptype, 'con', 'ndvi')
    return ndvi(data) - mean

def ndvi_diff_norm(data, croptype):
    _, std = get_crop_stats(data, croptype, 'con', 'ndvi')
    return ndvi_diff(data, croptype) / std

def evi(data):
    castdata = data.astype("float32")
    normdata = castdata / 10000
    G = 2.5
    C1 = 6
    C2 = 7.5
    L = 1
    return G * ((normdata["nir"] - normdata["red"]) / (normdata["nir"] + C1*normdata["red"] - C2*normdata["blue"] + L))

def evi_diff(data, croptype):
    mean, _ = get_crop_stats(data, croptype, 'con', 'evi')
    return evi(data) - mean

def evi_diff_norm(data, croptype):
    _, std = get_crop_stats(data, croptype, 'con', 'evi')
    return evi_diff(data, croptype) / std
