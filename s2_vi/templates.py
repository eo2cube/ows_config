from ows_refactored.common.ows_reslim_cfg import reslim_continental

image_processing = {
    "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
    "always_fetch_bands": [],
    "manual_merge": False,  # True
    "apply_solar_corrections": False,
}

base_config = {
    "dynamic": True,
    "resource_limits": reslim_continental,
    "image_processing": image_processing,
}

s2_c1_l2a = {
    "product_name": "s2_c1_l2a",
    "native_crs": "EPSG:32633",
    "native_resolution": [10.0, -10.0],
}

vegetation_params = {
    "product_name": "vegetation_params",
    "native_crs": "EPSG:32633",
    "native_resolution": [10.0, -10.0],
}

soil_params = {
    "product_name": "soil_params",
    "native_crs": "EPSG:32633",
    "native_resolution": [30.0, -30.0],
}

rgb_nir = {
    "red": [],
    "green": [],
    "blue": [],
    "nir": [],
}

rgb_nir_scl = {
    **rgb_nir,
    "scl": [],
}
