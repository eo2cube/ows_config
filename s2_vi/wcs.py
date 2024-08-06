# import the function by datacube-ows that does the TIFF conversion
from datacube_ows.wcs1_utils import get_tiff

# fake the two BandIndex functions that are used by get_tiff
# everything is hardcoded
class FakeBandIndex:
    def band_label(self, band):
        return "index_function"   # here it shouldn't be a problem
    def nodata_val(self, band):
        return 0   # here it probably IS a problem

def as_tiff_wcs1(req, data):
    # apply the index function of the first (and in our case usually only) style to the data
    dataarray = req.product.styles[0].apply_index(data)
    # convert the result into a Dataset because get_tiff expects a Dataset, not a DataArray
    dataset = dataarray.to_dataset()
    # variant that does (exactly?) the same:
    #dataarray = req.product.styles[0].index_function.__call__(data=data)
    #dataset = dataarray.to_dataset(name='index_function')
    # overwrite BandIndex which is used in get_tiff but of course doesn't match the structure of the data anymore
    req.product.band_idx = FakeBandIndex()  # very hacky...
    # do the TIFF conversion with the normal function that datacube-ows would usually use anyway
    return get_tiff(req, dataset)
