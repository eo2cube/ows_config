# OWS config

The file `config.json` is the base config that includes the vegetation index layers from `s2_vi/layers.py`. That file again imports snippets that are used several times from `templates.py` and `colorramps.py`. The data is calculated on the fly with functions in `formulas.py`.

The config of the general Sentinel-2 imagery layers is taken from the [Digital Earth Africa `surface_reflectance` config](https://github.com/digitalearthafrica/config/tree/master/services/ows_refactored/surface_reflectance).

All user-facing texts are in German as requested by the project partners.