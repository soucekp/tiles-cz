"""
Purpose: Script, which is calculating scales and resolutions for S-JTSK tile matrix sets
License: GNU/GPLv3
Author: Jachym Cepicky jachym.cepicky at opengeolabs.cz

Usage:

    python3 scales.py

Output: Tabular representation of zoom levels, scales and resolutions
Dependencies: pip3 install tabulate
"""

try:
    from tabulate import tabulate
except ModuleNotFoundError as e:
    tabulate = None
    print ("tabulate not installed, using `print`")

import json

dpi = 90
maxscaledenom = 7315200

top = -920000
left = -925000
meters_per_inch = 0.0254
inch_per_meter = 1/meters_per_inch
tilesize = 512

dots_per_meter = dpi * inch_per_meter

tilesize_meters = tilesize / dots_per_meter

data = [
        [
        "zoom", "scaledenom", "resolution", "columns and rows", "bbox"
        ]
       ]

for zoom in range(0, 20):

    scaledenom = maxscaledenom/(2**zoom)

    cols_rows = 2**zoom

    tilesize_meters_scale = tilesize_meters * scaledenom

    resolution = tilesize_meters_scale/tilesize

    bbox = [left,  top - cols_rows * tilesize_meters_scale, left + cols_rows * tilesize_meters_scale , top]

    data.append([zoom, scaledenom, resolution, cols_rows, bbox])

if tabulate:
    print(tabulate(data))
else:
    for row in data:
        print("\t|".join([str(i) for i in row]))

geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "polygon",
                    "coordinates": [[
                        [ data[-1][-1][0], data[-1][-1][1] ],
                        [ data[-1][-1][2], data[-1][-1][1] ],
                        [ data[-1][-1][2], data[-1][-1][3] ],
                        [ data[-1][-1][0], data[-1][-1][3] ],
                        [ data[-1][-1][0], data[-1][-1][1] ],
                        ]]
                    }
            }
        ]
        }
print(json.dumps(geojson))
