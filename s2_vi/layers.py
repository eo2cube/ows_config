from ows_refactored.s2_vi.templates import base_config
from ows_refactored.s2_vi.templates import s2_c1_l2a
from ows_refactored.s2_vi.templates import rgb_and_nir
from ows_refactored.s2_vi.colorramps import colorramp_ndvi
from ows_refactored.s2_vi.colorramps import colorramp_ndvi_legend
from ows_refactored.s2_vi.colorramps import colorramp_ndvi_legend_abstract

ndvi = {
    "name": "s2_vi_ndvi",
    "title": "NDVI",
    "abstract": "Normalized Difference Vegetation Index (räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI)",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "grey-brown-green",
        "styles": [
            {
                "name": "grey-brown-green",
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
    "abstract": "Enhanced Vegetation Index (räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI)",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "grey-brown-green",
        "styles": [
            {
                "name": "grey-brown-green",
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
    "abstract": "Abweichung des Normalized Difference Vegetation Index vom langjährigen Mittel für die Anbaufrucht Raps (räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI, Quelle: DLR - Deutsches Fernerkundungsdatenzentrum, Team Agrar- und Waldökosysteme und Earth Observation Research Cluster/Universität Würzburg)",
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "grey-brown-green",
        "styles": [
            {
                "name": "grey-brown-green",
                "title": "NDVI-Differenz",
                "abstract": "von braun nach blau",
                "needed_bands": ["red", "green", "blue", "nir"],
                "index_function": {
                    "function": "ows_refactored.s2_vi.formulas.ndvi_diff",
                },
                "mpl_ramp": "BrBG",
                "range": [-0.3, 0.3],
                "legend": {
                    "title": "NDVI-Differenz",
                    "begin": "-0.3",
                    "end": "0.3",
                    "ticks": ["-0.3", "-0.2", "-0.1", "0", "0.1", "0.2", "0.3"],
                },
            },
        ],
    },
}

evi_diff = {
    "name": "s2_vi_evi_diff",
    "title": "EVI-Differenz",
    "abstract": "Abweichung des Enhanced Vegetation Index vom langjährigen Mittel für die Anbaufrucht Raps (räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI, Quelle: DLR - Deutsches Fernerkundungsdatenzentrum, Team Agrar- und Waldökosysteme und Earth Observation Research Cluster/Universität Würzburg)",
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_and_nir,
    "styling": {
        "default_style": "grey-brown-green",
        "styles": [
            {
                "name": "grey-brown-green",
                "title": "EVI-Differenz",
                "abstract": "von braun nach blau",
                "needed_bands": ["red", "green", "blue", "nir"],
                "index_function": {
                    "function": "ows_refactored.s2_vi.formulas.evi_diff",
                },
                "mpl_ramp": "BrBG",
                "range": [-0.3, 0.3],
                "legend": {
                    "title": "EVI-Differenz",
                    "begin": "-0.3",
                    "end": "0.3",
                    "ticks": ["-0.3", "-0.2", "-0.1", "0", "0.1", "0.2", "0.3"],
                },
            },
        ],
    },
}