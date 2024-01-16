from ows_refactored.s2_vi.templates import base_config
from ows_refactored.s2_vi.templates import s2_c1_l2a
from ows_refactored.s2_vi.templates import rgb_and_nir
from ows_refactored.s2_vi.colorramps import colorramp_ndvi
from ows_refactored.s2_vi.colorramps import colorramp_ndvi_legend
from ows_refactored.s2_vi.colorramps import colorramp_ndvi_legend_abstract

ndvi = {
    "name": "s2_vi_ndvi",
    "title": "NDVI",
    "abstract": "Normalized Difference Vegetation Index",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "python_onthefly",
        "styles": [
            {
                "name": "python_onthefly",
                "title": "NDVI",
                "abstract": colorramp_ndvi_legend_abstract,
                "needed_bands": ["red", "green", "blue", "nir"],
                "index_function": {
                    "function": "ows_refactored.s2_vi.formulas.ndvi",
                },
                "color_ramp": colorramp_ndvi,
                "legend": {
                    "title": "NDVI",
                    **colorramp_ndvi_legend
                },
            },
        ],
    },
}

evi = {
    "name": "s2_vi_evi",
    "title": "EVI",
    "abstract": "Enhanced Vegetation Index",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "python_onthefly",
        "styles": [
            {
                "name": "python_onthefly",
                "title": "EVI",
                "abstract": colorramp_ndvi_legend_abstract,
                "needed_bands": ["red", "green", "blue", "nir"],
                "index_function": {
                    "function": "ows_refactored.s2_vi.formulas.evi",
                },
                "color_ramp": colorramp_ndvi,  # sic!
                "legend": {
                    "title": "EVI",
                    **colorramp_ndvi_legend
                },
            },
        ],
    },
}

ndvi_diff = {
    "name": "s2_vi_ndvi_diff",
    "title": "NDVI-Differenz",
    "abstract": "Abweichung des Normalized Difference Vegetation Index vom langjährigen Mittel für verschiedene Fruchtarten",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "python_onthefly",
        "styles": [
            {
                "name": "python_onthefly",
                "title": "NDVI-Differenz",
                "abstract": "von braun nach blau",
                "needed_bands": ["red", "green", "blue", "nir"],
                "index_function": {
                    "function": "ows_refactored.s2_vi.formulas.ndvi_diff",
                },
                "mpl_ramp": "BrBG",
                "range": [-4 * 0.06434399394499828, 4 * 0.06434399394499828],
                "legend": {
                    "title": "NDVI-Differenz",
                    "begin": "-0.26",  # apparently must be outside the range of `range`
                    "end": "0.26",
                    "ticks": ["-0.25", "-0.19", "-0.13", "-0.06", "0", "0.06", "0.13", "0.19", "0.25"]
                },
            },
        ],
    },
}

evi_diff = {
    "name": "s2_vi_evi_diff",
    "title": "EVI-Differenz",
    "abstract": "Abweichung des Enhanced Vegetation Index vom langjährigen Mittel für verschiedene Fruchtarten",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "python_onthefly",
        "styles": [
            {
                "name": "python_onthefly",
                "title": "EVI-Differenz",
                "abstract": "von braun nach blau",
                "needed_bands": ["red", "green", "blue", "nir"],
                "index_function": {
                    "function": "ows_refactored.s2_vi.formulas.evi_diff",
                },
                "mpl_ramp": "BrBG",
                "range": [-4 * 0.0447305790362834, 4 * 0.0447305790362834],
                "legend": {
                    "title": "EVI-Differenz",
                    "begin": "-0.18",
                    "end": "0.18",
                    "ticks": ["-0.18", "-0.135", "-0.09", "-0.045", "0", "0.18", "0.135", "0.09", "0.045"]
                },
            },
        ],
    },
}