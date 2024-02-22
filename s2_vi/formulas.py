from ows_refactored.s2_vi.constants import ndvi_means, ndvi_stds
from ows_refactored.s2_vi.constants import evi_means, evi_stds

def ndvi(data):
    castdata = data.astype("float32")
    return (castdata["nir"] - castdata["red"]) / (castdata["nir"] + castdata["red"])

def ndvi_diff(data, croptype):
    mm_dd = data.time.values[0].astype(str)[5:10]
    return ndvi(data) - ndvi_means[croptype][mm_dd]  # value applicable for combination of date and crop

def ndvi_diff_norm(data, croptype):
    mm_dd = data.time.values[0].astype(str)[5:10]
    return ndvi_diff(data, croptype) / ndvi_stds[croptype][mm_dd]  # value applicable for combination of date and crop

def evi(data):
    castdata = data.astype("float32")
    normdata = castdata / 10000
    G = 2.5
    C1 = 6
    C2 = 7.5
    L = 1
    return G * ((normdata["nir"] - normdata["red"]) / (normdata["nir"] + C1*normdata["red"] - C2*normdata["blue"] + L))

def evi_diff(data, croptype):
    mm_dd = data.time.values[0].astype(str)[5:10]
    return evi(data) - evi_means[croptype][mm_dd]  # value applicable for combination of date and crop

def evi_diff_norm(data, croptype):
    mm_dd = data.time.values[0].astype(str)[5:10]
    return evi_diff(data, croptype) / evi_stds[croptype][mm_dd]  # value applicable for combination of date and crop
