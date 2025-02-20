from copy import deepcopy

from ows_refactored.s2_vi.templates import base_config
from ows_refactored.s2_vi.templates import s2_c1_l2a
from ows_refactored.s2_vi.templates import vegetation_params, soil_params
from ows_refactored.s2_vi.templates import rgb_nir, rgb_nir_scl
from ows_refactored.s2_vi.colorramps import colorramp_ndvi
from ows_refactored.s2_vi.colorramps import colorramp_ndvi_legend
from ows_refactored.s2_vi.colorramps import colorramp_ndvi_legend_abstract

rgb = {
    "title": "Sentinel-2",
    "name": "s2_l2a",
    "abstract": "Räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI",
    **base_config,
    **s2_c1_l2a,
    "bands": {
        "coastal": ["coastal_aerosol"],
        "blue": ["blue"],
        "green": ["green"],
        "red": ["red"],
        "rededge1": ["red_edge_1"],
        "rededge2": ["red_edge_2"],
        "rededge3": ["red_edge_3"],
        "nir": ["nir", "nir_1"],
        "nir08": ["nir_narrow", "nir_2"],
        "nir09": ["water_vapour"],
        "swir16": ["swir_1", "swir_16"],
        "swir22": ["swir_2", "swir_22"],
        "aot": ["aerosol_optical_thickness"],
        "wvp": ["scene_average_water_vapour"],
        "scl": ["mask", "qa"],
    },
    "styling": {
        "default_style": "simple_rgb",
        "styles": [
            {
                "name": "simple_rgb",
                "title": "Echtfarbbild",
                "abstract": "Simples Echtfarbbild aus Kombination des roten, grünen und blauen Bandes",
                "components": {"red": {"red": 1.0}, "green": {"green": 1.0}, "blue": {"blue": 1.0}},
                "scale_range": [0.0, 3000.0],
            }
        ],
    },
}

ndvi = {
    "name": "s2_vi_ndvi",
    "title": "NDVI",
    "abstract": "Normalized Difference Vegetation Index (räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI)",  # also multiline possible with """\nLorem ipsum\n"""
    **base_config,
    **s2_c1_l2a,
    "bands": rgb_nir,
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
    "bands": rgb_nir,
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

croptypes = {
    "winter_wheat": "Winterweizen",
    "winter_barley": "Wintergerste",
    "spring_barley": "Sommergerste",
    "rapeseed": "Raps",
    "maize": "Mais",
    "potatoes": "Kartoffeln",
    "sugar_beet": "Zuckerrüben",
}

vegetation_indices = {
    "ndvi": "Normalized Difference Vegetation Index",
    "evi": "Enhanced Vegetation Index",
}

diff = []
for ct_key, ct_name in croptypes.items():
    layers = []
    for vi_key, vi_name in vegetation_indices.items():
        layers.append({
            "name": "s2_vi_" + vi_key + "_diff_" + ct_key,
            "title": vi_key.upper() + "-Differenz " + ct_name,
            "abstract": "Abweichung des " + vi_name + " vom langjährigen Mittel für die Anbaufrucht " + ct_name + " (räumliche Auflösung: 10 m, genutzte Satellitensensoren: Sentinel-2 MSI, Quelle: DLR - Deutsches Fernerkundungsdatenzentrum, Team Agrar- und Waldökosysteme und Earth Observation Research Cluster/Universität Würzburg)",
            **base_config,
            **s2_c1_l2a,
            "bands": rgb_nir_scl,
            "flags": [
                { "band": "scl" }
            ],
            "styling": {
                "default_style": "brown-blue",
                "styles": [
                    {
                        "name": "brown-blue",
                        "title": vi_key.upper() + "-Differenz " + ct_name,
                        "abstract": "von braun nach blau",
                        "needed_bands": ["red", "green", "blue", "nir", "scl"],
                        "index_function": {
                            "function": "ows_refactored.s2_vi.formulas." + vi_key + "_diff",
                            "kwargs": { "croptype": ct_key }
                        },
                        "pq_masks": [
                            { "band": "scl", "values": [4, 5] },   # only keep 4 = vegetation and 5 = not vegetated
                        ],
                        "mpl_ramp": "BrBG",
                        "range": [-0.3, 0.3],
                        "legend": {
                            "title": vi_key.upper() + "-Differenz " + ct_name,
                            "begin": "-0.3",
                            "end": "0.3",
                            "ticks": ["-0.3", "-0.2", "-0.1", "0", "0.1", "0.2", "0.3"],
                        }
                    },
                ],
            },
        })
    diff.append({
        "title": "VI-Differenzen " + ct_name,
        "abstract": "Abweichung vom langjährigen Mittel für " + ct_name,
        "layers": layers
    })

diff_norm = deepcopy(diff)
for entry in diff_norm:
    entry['title'] = "Normierte " + entry['title']
    entry['abstract'] += " in Vielfachen der Standardabweichung"
    for layer in entry['layers']:
        layer['title'] = "Normierte " + layer['title']
        layer['abstract'] = layer['abstract'].replace("(", "in Vielfachen der Standardabweichung (")
        layer['name'] = layer['name'].replace("_diff_", "_diff_norm_")
        for style in layer['styling']['styles']:
            style['index_function']['function'] += "_norm"
            style['title'] = "Normierte " + style['title']
            style['range'] = [-1.0, 1.0]
            style['legend']['begin'] = "-1.0"
            style['legend']['end'] = "1.0"
            style['legend']['ticks'] = ["-1.0", "-0.5", "0.0", "0.5", "1.0"]

lai = {
    "name": "s2_vp_lai_winter_wheat",
    "title": "LAI Winterweizen",
    "abstract": "Leaf Area Index für Winterweizen, Wochenmittel (Mo-So), Ableitung mittels Gaussian Process Regression - trainiert auf der MISPEL Hyperspektraldatenbank (räumliche Auflösung: 10m, genutzte Satellitensensoren: Sentinel-2 MSI, Quelle: JKI - Institut für Pflanzenbau und Bodenkunde, FLF)",
    **base_config,
    **vegetation_params,
    "bands": {
        "lai": ["lai"],
    },
    "styling": {
        "default_style": "red-green",
        "styles": [
            {
                "name": "red-green",
                "title": "LAI Winterweizen",
                "abstract": "Leaf Area Index für Winterweizen",
                "needed_bands": ["lai"],
                "index_function": {
                    "function": "datacube_ows.band_utils.single_band",
                    "mapped_bands": True,
                    "kwargs": {
                        "band": "lai"
                    },
                },
                "mpl_ramp": "RdYlGn",
                "range": [0, 6],
                "legend": {
                    "title": "LAI",
                    "begin": "0.0",
                    "end": "6.0",
                    "ticks": ["0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0"],
                },
            },
        ],
    },
}

bm = {
    "name": "s2_vp_bm_winter_wheat",
    "title": "Biomasse Winterweizen",
    "abstract": "Biomasse [t/ha] für Winterweizen, Wochenmittel (Mo-So), Ableitung mittels Gaussian Process Regression - trainiert auf der MISPEL Hyperspektraldatenbank (räumliche Auflösung: 10m, genutzte Satellitensensoren: Sentinel-2 MSI, Quelle: JKI - Institut für Pflanzenbau und Bodenkunde, FLF)",
    **base_config,
    **vegetation_params,
    "bands": {
        "bm": ["bm"],
    },
    "styling": {
        "default_style": "red-green",
        "styles": [
            {
                "name": "red-green",
                "title": "Biomasse Winterweizen",
                "abstract": "Biomasse [t/ha] für Winterweizen",
                "needed_bands": ["bm"],
                "index_function": {
                    "function": "datacube_ows.band_utils.single_band",
                    "mapped_bands": True,
                    "kwargs": {
                        "band": "bm"
                    },
                },
                "mpl_ramp": "RdYlGn",
                "range": [0, 60],
                "legend": {
                    "title": "Biomasse [t/ha]",
                    "begin": "0.0",
                    "end": "60.0",
                    "ticks": ["0", "10", "20", "30", "40", "50", "60"],
                },
            },
        ],
    },
}

soc = {
    "name": "soc_demmin",
    "title": "Soil Organic Carbon",
    "abstract": "Soil Organic Carbon (SOC) [g/kg] basierend auf Bare-Soil-Pixels (2020-2021, Median, räumliche Auflösung: 30m, genutzte Satellitensensoren: ASI PRISMA (hyperspektral), Quelle: GFZ)",
    **base_config,
    **soil_params,
    "bands": {
        "soc": ["soc"],
    },
    "styling": {
        "default_style": "cividis",
        "styles": [
            {
                "name": "cividis",
                "title": "Soil Organic Carbon",
                "abstract": "Soil Organic Carbon [g/kg]",
                "needed_bands": ["soc"],
                "index_function": {
                    "function": "datacube_ows.band_utils.single_band",
                    "mapped_bands": True,
                    "kwargs": {
                        "band": "soc"
                    },
                },
                "mpl_ramp": "cividis_r",
                "range": [2, 22],
                "legend": {
                    "title": "Soil Organic Carbon [g/kg]",
                    "begin": "2.0",
                    "end": "22.0",
                    "ticks": ["2", "7", "12", "17", "22"],
                },
            },
        ],
    },
}

"""
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
"""