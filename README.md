# stac-generator-fast-api-writer

Simple microservice which goes alongside the [stac-generator](https://github.com/SpatialDays/stac-generator) to write
the generated STAC items to a STAC API.

The microservice consumes a Redis list items published by the stac-generator and writes them to a STAC API.

## Environment Variables

| Name                    | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| REDIS_HOST              | Redis host                                                       |
| REDIS_PORT              | Redis port                                                       |
| REDIS_INPUT_LIST_NAME   | Redis input list name                                            |
| STAC_FASTAPI_READ_HOST  | STAC API host for checking if the STAC Items are already present |
| STAC_FASTAPI_WRITE_HOST | STAC API host for writing the STAC Items                         |
| NUM_RETRIES             | Number of retries for writing to STAC-FastAPI                    |

## Input Payload Example

Input paylaod is standard compliant stac, accompanied with the collection id where the
item needs to be written to.

```json
{
  "collection": "os_heightstore_dtm1m",
  "stac": {
    "type": "Feature",
    "stac_version": "1.0.0",
    "id": "cc8fc925-c486-aff3-949c-a7895b0f93b8-DTM-01-09",
    "properties": {
      "proj:epsg": 27700,
      "proj:geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              421000.0,
              449000.0
            ],
            [
              422000.0,
              449000.0
            ],
            [
              422000.0,
              450000.0
            ],
            [
              421000.0,
              450000.0
            ],
            [
              421000.0,
              449000.0
            ]
          ]
        ]
      },
      "proj:bbox": [
        421000.0,
        449000.0,
        422000.0,
        450000.0
      ],
      "proj:shape": [
        1000,
        1000
      ],
      "proj:transform": [
        1.0,
        0.0,
        421000.0,
        0.0,
        -1.0,
        450000.0,
        0.0,
        0.0,
        1.0
      ],
      "proj:projjson": {
        "$schema": "https://proj.org/schemas/v0.4/projjson.schema.json",
        "type": "ProjectedCRS",
        "name": "OSGB36 / British National Grid",
        "base_crs": {
          "name": "OSGB36",
          "datum": {
            "type": "GeodeticReferenceFrame",
            "name": "Ordnance Survey of Great Britain 1936",
            "ellipsoid": {
              "name": "Airy 1830",
              "semi_major_axis": 6377563.396,
              "inverse_flattening": 299.3249646
            }
          },
          "coordinate_system": {
            "subtype": "ellipsoidal",
            "axis": [
              {
                "name": "Geodetic latitude",
                "abbreviation": "Lat",
                "direction": "north",
                "unit": "degree"
              },
              {
                "name": "Geodetic longitude",
                "abbreviation": "Lon",
                "direction": "east",
                "unit": "degree"
              }
            ]
          },
          "id": {
            "authority": "EPSG",
            "code": 4277
          }
        },
        "conversion": {
          "name": "unnamed",
          "method": {
            "name": "Transverse Mercator",
            "id": {
              "authority": "EPSG",
              "code": 9807
            }
          },
          "parameters": [
            {
              "name": "Latitude of natural origin",
              "value": 49,
              "unit": "degree",
              "id": {
                "authority": "EPSG",
                "code": 8801
              }
            },
            {
              "name": "Longitude of natural origin",
              "value": -2,
              "unit": "degree",
              "id": {
                "authority": "EPSG",
                "code": 8802
              }
            },
            {
              "name": "Scale factor at natural origin",
              "value": 0.9996012717,
              "unit": "unity",
              "id": {
                "authority": "EPSG",
                "code": 8805
              }
            },
            {
              "name": "False easting",
              "value": 400000,
              "unit": "metre",
              "id": {
                "authority": "EPSG",
                "code": 8806
              }
            },
            {
              "name": "False northing",
              "value": -100000,
              "unit": "metre",
              "id": {
                "authority": "EPSG",
                "code": 8807
              }
            }
          ]
        },
        "coordinate_system": {
          "subtype": "Cartesian",
          "axis": [
            {
              "name": "Easting",
              "abbreviation": "",
              "direction": "east",
              "unit": "metre"
            },
            {
              "name": "Northing",
              "abbreviation": "",
              "direction": "north",
              "unit": "metre"
            }
          ]
        },
        "id": {
          "authority": "EPSG",
          "code": 27700
        }
      },
      "license": "proprietary",
      "gsd": 1.0,
      "datetime": "2023-08-14T15:38:35.384900Z",
      "bulk-upload-system-metadata:original-metadata-location": "https://oseoinfrastagingstrgacc.blob.core.windows.net/heightstore-dtm1m-raw/data/incremental/2023/07/13/02/35885-65664fd6-448a-cf4f-10b9-14272309510b.json",
      "os-heightstore-dtm1m:idem": "cc8fc925-c486-aff3-949c-a7895b0f93b8",
      "os-heightstore-dtm1m:tile-reference": "SE24",
      "os-heightstore-dtm1m:update-date": "2022-12-20T19:55:22",
      "os-heightstore-dtm1m:earliest-flight-date": "2022-04-21T00:00:00",
      "os-heightstore-dtm1m:latest-flight-date": "2022-04-21T00:00:00",
      "os-heightstore-dtm1m:dtm-grid-id": "65664fd6-448a-cf4f-10b9-14272309510b",
      "os-heightstore-dtm1m:change-cache-url": "https://dtmsproddtmchangecache.blob.core.windows.net:443/dtm1mstore/65664fd6-448a-cf4f-10b9-14272309510b/",
      "os-heightstore-dtm1m:dtm-base-change-event-id": null,
      "os-heightstore-dtm1m:version": 35885,
      "os-heightstore-dtm1m:grid-app-version": "2020.1.22.1"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [
            -1.6816126901041852,
            53.936696288685056
          ],
          [
            -1.680887364018827,
            53.93669436556608
          ],
          [
            -1.6801620380180073,
            53.93669243806749
          ],
          [
            -1.6794367121019174,
            53.93669050618925
          ],
          [
            -1.67871138627075,
            53.9366885699314
          ],
          [
            -1.6779860605246975,
            53.93668662929391
          ],
          [
            -1.6772607348639528,
            53.936684684276784
          ],
          [
            -1.6765354092887068,
            53.93668273488002
          ],
          [
            -1.6758100837991523,
            53.93668078110363
          ],
          [
            -1.6750847583954818,
            53.93667882294764
          ],
          [
            -1.6743594330778875,
            53.936676860411986
          ],
          [
            -1.6736341078465615,
            53.936674893496736
          ],
          [
            -1.6729087827016966,
            53.93667292220185
          ],
          [
            -1.6721834576434842,
            53.93667094652733
          ],
          [
            -1.6714581326721176,
            53.9366689664732
          ],
          [
            -1.6707328077877888,
            53.93666698203946
          ],
          [
            -1.6700074829906904,
            53.93666499322608
          ],
          [
            -1.6692821582810131,
            53.936663000033114
          ],
          [
            -1.6685568336589502,
            53.936661002460525
          ],
          [
            -1.6678315091246942,
            53.93665900050828
          ],
          [
            -1.667106184678437,
            53.93665699417646
          ],
          [
            -1.6663808603203716,
            53.93665498346501
          ],
          [
            -1.666377448892418,
            53.937082964101094
          ],
          [
            -1.6663740373760778,
            53.937510944706354
          ],
          [
            -1.6663706257713482,
            53.93793892528074
          ],
          [
            -1.6663672140782264,
            53.93836690582428
          ],
          [
            -1.6663638022967089,
            53.93879488633699
          ],
          [
            -1.666360390426792,
            53.93922286681883
          ],
          [
            -1.6663569784684737,
            53.93965084726984
          ],
          [
            -1.6663535664217506,
            53.94007882769001
          ],
          [
            -1.6663501542866195,
            53.94050680807932
          ],
          [
            -1.666346742063077,
            53.94093478843777
          ],
          [
            -1.66634332975112,
            53.94136276876538
          ],
          [
            -1.6663399173507465,
            53.94179074906213
          ],
          [
            -1.666336504861952,
            53.94221872932805
          ],
          [
            -1.6663330922847346,
            53.94264670956312
          ],
          [
            -1.6663296796190898,
            53.943074689767336
          ],
          [
            -1.666326266865016,
            53.94350266994073
          ],
          [
            -1.6663228540225095,
            53.94393065008324
          ],
          [
            -1.6663194410915663,
            53.94435863019492
          ],
          [
            -1.6663160280721852,
            53.94478661027575
          ],
          [
            -1.6663126149643612,
            53.945214590325726
          ],
          [
            -1.666309201768092,
            53.94564257034485
          ],
          [
            -1.6670346820353028,
            53.9456445817153
          ],
          [
            -1.6677601623907703,
            53.94564658870468
          ],
          [
            -1.6684856428343011,
            53.945648591313024
          ],
          [
            -1.6692111233657032,
            53.94565058954031
          ],
          [
            -1.6699366039847836,
            53.94565258338654
          ],
          [
            -1.6706620846913498,
            53.94565457285173
          ],
          [
            -1.671387565485211,
            53.945656557935855
          ],
          [
            -1.6721130463661735,
            53.945658538638924
          ],
          [
            -1.6728385273340451,
            53.94566051496094
          ],
          [
            -1.6735640083886334,
            53.9456624869019
          ],
          [
            -1.6742894895297458,
            53.94566445446179
          ],
          [
            -1.6750149707571906,
            53.945666417640645
          ],
          [
            -1.675740452070775,
            53.94566837643841
          ],
          [
            -1.676465933470306,
            53.94567033085513
          ],
          [
            -1.6771914149555915,
            53.945672280890776
          ],
          [
            -1.6779168965264386,
            53.94567422654537
          ],
          [
            -1.6786423781826563,
            53.94567616781889
          ],
          [
            -1.6793678599240514,
            53.94567810471134
          ],
          [
            -1.6800933417504313,
            53.94568003722273
          ],
          [
            -1.680818823661604,
            53.94568196535305
          ],
          [
            -1.6815443056573762,
            53.9456838891023
          ],
          [
            -1.6815475629034624,
            53.94525590843839
          ],
          [
            -1.6815508200651452,
            53.94482792774363
          ],
          [
            -1.6815540771424256,
            53.944399947018084
          ],
          [
            -1.6815573341353085,
            53.943971966261664
          ],
          [
            -1.6815605910437947,
            53.943543985474435
          ],
          [
            -1.6815638478678887,
            53.94311600465636
          ],
          [
            -1.6815671046075928,
            53.94268802380744
          ],
          [
            -1.68157036126291,
            53.9422600429277
          ],
          [
            -1.681573617833844,
            53.94183206201711
          ],
          [
            -1.6815768743203967,
            53.94140408107572
          ],
          [
            -1.6815801307225715,
            53.940976100103455
          ],
          [
            -1.6815833870403714,
            53.94054811910037
          ],
          [
            -1.6815866432737994,
            53.94012013806646
          ],
          [
            -1.6815898994228582,
            53.93969215700171
          ],
          [
            -1.6815931554875512,
            53.93926417590611
          ],
          [
            -1.681596411467881,
            53.9388361947797
          ],
          [
            -1.6815996673638505,
            53.93840821362243
          ],
          [
            -1.6816029231754626,
            53.93798023243434
          ],
          [
            -1.6816061789027206,
            53.937552251215415
          ],
          [
            -1.6816094345456272,
            53.937124269965636
          ],
          [
            -1.6816126901041852,
            53.936696288685056
          ]
        ]
      ]
    },
    "links": [
      {
        "rel": "license",
        "href": "https://www.ordnancesurvey.co.uk/business-government/tools-support/terms-conditions/os-open-data-licence",
        "type": "license"
      }
    ],
    "assets": {
      "metadata": {
        "href": "https://oseoinfrastagingstrgacc.blob.core.windows.net/heightstore-dtm1m-raw/data/incremental/2023/07/13/02/35885-65664fd6-448a-cf4f-10b9-14272309510b.json",
        "type": "application/json"
      },
      "rendered_preview": {
        "href": "https://oseoinfrastagingstrgacc.blob.core.windows.net/heightstore-dtm1m-raw-cog/data/incremental/2023/07/13/02/35885-65664fd6-448a-cf4f-10b9-14272309510b/DTM-01-09_thumbnail.png",
        "type": "image/png",
        "title": "Rendered preview",
        "rel": "preview",
        "roles": [
          "overview"
        ]
      },
      "data": {
        "href": "https://oseoinfrastagingstrgacc.blob.core.windows.net/heightstore-dtm1m-raw-cog/data/incremental/2023/07/13/02/35885-65664fd6-448a-cf4f-10b9-14272309510b/DTM-01-09.tif",
        "type": "image/tiff; application=geotiff",
        "raster:bands": [
          {
            "data_type": "float64",
            "scale": 1.0,
            "offset": 0.0,
            "sampling": "area",
            "nodata": -99999.0,
            "statistics": {
              "mean": 122.18526569399997,
              "minimum": 89.099,
              "maximum": 182.697,
              "stddev": 28.08825003699509,
              "valid_percent": 100.0
            },
            "histogram": {
              "count": 11,
              "min": 89.099,
              "max": 182.697,
              "buckets": [
                309214,
                79261,
                82557,
                84343,
                101611,
                92599,
                82241,
                78185,
                59770,
                30219
              ]
            }
          }
        ],
        "eo:bands": [
          {
            "name": "b1",
            "description": "Surface Model Raster Band"
          }
        ],
        "roles": []
      }
    },
    "bbox": [
      -1.6816126901041852,
      53.93665498346501,
      -1.666309201768092,
      53.9456838891023
    ],
    "stac_extensions": [
      "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
      "https://stac-extensions.github.io/raster/v1.1.0/schema.json",
      "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
      "https://raw.githubusercontent.com/SpatialDays/sd-stac-extensions/main/os-heightstore-dtm1m/v1.0.0/schema.json",
      "https://raw.githubusercontent.com/SpatialDays/sd-stac-extensions/main/bulk-upload-system-metadata/v1.0.1/schema.json"
    ]
  }
}


```