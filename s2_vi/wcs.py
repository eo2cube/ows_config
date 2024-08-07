# import the function by datacube-ows that does the TIFF conversion
from datacube_ows.wcs1_utils import get_tiff
from numpy import nan

# fake the two BandIndex functions that are used by get_tiff (band_label, nodata_val) and the one that is called in some error situations (band_labels)
# everything is hardcoded
class FakeBandIndex:
    def band_label(self, band):
        return "index_function"
    def band_labels(self):
        return ["index_function"]
    def nodata_val(self, band):
        return nan

def as_tiff_wcs1(req, data):
    # apply the index function of the first (and in our case usually only) style to the data
    dataarray = req.product.styles[0].apply_index(data)
    # convert the result into a Dataset because get_tiff expects a Dataset, not a DataArray
    dataset = dataarray.to_dataset()

    # variant that does (exactly?) the same:
    #dataarray = req.product.styles[0].index_function.__call__(data=data)
    #dataset = dataarray.to_dataset(name='index_function')

    # get the mask from the style (returns DataArray with True/False values)
    mask = req.product.styles[0].to_mask(data)
    # and directly apply it to our calculated data, putting `nan` where False
    masked = dataset.where(mask, nan)

    # overwrite BandIndex which is used in get_tiff but of course doesn't match the structure of the data anymore
    req.product.band_idx = FakeBandIndex()  # very hacky...
    # do the TIFF conversion with the normal function that datacube-ows would usually use anyway
    return get_tiff(req, masked)
