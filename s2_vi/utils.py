import json
from shapely.geometry import shape, Point

def get_landscape(data):
    # for simplicity: use coordinate of point in the center of the bbox
    if data.crs == 'EPSG:4326':
        lon = data.longitude.values[data.longitude.size // 2]
        lat = data.latitude.values[data.latitude.size // 2]
        centerpoint = Point(lon, lat)
    elif data.crs == 'EPSG:3857':
        x = data.x.values[data.x.size // 2]
        y = data.y.values[data.y.size // 2]
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
