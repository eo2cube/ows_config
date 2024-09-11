import json
from shapely.geometry import shape, Point
import xarray as xr
import numpy as np

def get_landscape(data):
    # for simplicity: use coordinate of point in the center of the bbox
    if data.crs == 'EPSG:4326':
        lon = data.longitude.values if data.longitude.size == 1 else data.longitude.values[data.longitude.size // 2]
        lat = data.latitude.values if data.latitude.size  == 1 else data.latitude.values[data.latitude.size // 2]
        centerpoint = Point(lon, lat)
    elif data.crs == 'EPSG:3857':
        x = data.x.values if data.x.size == 1 else data.x.values[data.x.size // 2]
        y = data.y.values if data.y.size == 1 else data.y.values[data.y.size // 2]
        centerpoint = Point(x, y)
    else:
        raise Exception("Only requests in EPSG:4326 or 3857 are supported.")
    # load polygons and check each whether it contains the point
    with open('/home/datacube/ows_refactored/s2_vi/DLR_crop_statistics/Naturraum_EPSG' + data.crs[5:9] + '.geojson') as geojsonfile:
        geojson = json.load(geojsonfile)
    for feature in geojson['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(centerpoint):
            return feature['properties']['ZUS']
    raise Exception("Center point of bbox must be within a Naturraum polygon - try zooming in more or panning to a different location.")

def get_crop_stats(data, croptype, treatment, index):
    stats = xr.load_dataset('/home/datacube/ows_refactored/s2_vi/DLR_crop_statistics/crop_statistics.nc')
    landscape = get_landscape(data)
    timeline = stats.sel(landscape=landscape, crop=croptype, treatment=treatment, index=index)
    # GetMap provides an array, GetFeatureInfo not -> handle like in `get_landscape` above
    date = data.time.values if data.time.size == 1 else data.time.values[0]
    # if the requested date is newer than the newest date in the reference dataset, subtract one year until the reference period has been reached
    # this needs to be done to keep the season correct, otherwise `method = nearest` might snap e.g. 2024-05-02 to 2023-10-31, producing very wrong results
    while date > stats.date.max().values:   # use `.values`, not `.item()`, because the latter would convert the value to a float
        date -= np.timedelta64(365, 'D')    # for some reason `(1, 'Y')` doesn't work, so we have to do 365 days instead, which should be good enough even if there is a leap year
    # the same with dates that are before the reference period
    while date < stats.date.min().values:
        date += np.timedelta64(365, 'D')
    # find closest data point in reference timeseries and return it
    day = timeline.sel({'date': date}, method = "nearest")
    return day.means.item(), day.stds.item()
