from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.layouts import MapViewLayoutController
from tethys_sdk.gizmos import MVLayer, MVLegendClass


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'map_view_template_app/home.html', context)


class MyMapViewLayoutController(MapViewLayoutController):
    """
    My customized map view layout controller.
    """

    def build_layers(self, request, *args, **kwargs):
        """
        Custom layers.
        """
        map_layers = []

        kml_layer = MVLayer(source='KML',
                            options={'url': '/static/tethys_gizmos/data/model.kml'},
                            legend_title='Park City Watershed',
                            legend_extent=[-111.60, 40.57, -111.43, 40.70],
                            legend_classes=[
                                MVLegendClass('polygon', 'Watershed Boundary', fill='#ff8000'),
                                MVLegendClass('line', 'Stream Network', stroke='#0000ff'),
                            ])

        map_layers.append(kml_layer)

        # Define GeoJSON layer
        geojson_object = {
            'type': 'FeatureCollection',
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'EPSG:3857'
                }
            },
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [0, 0]
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[4e6, -2e6], [8e6, 2e6]]
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[[-5e6, -1e6], [-4e6, 1e6], [-3e6, -1e6]]]
                    }
                }
            ]
        }

        geojson_layer = MVLayer(source='GeoJSON',
                                options=geojson_object,
                                legend_title='Test GeoJSON',
                                legend_extent=[-46.7, -48.5, 74, 59],
                                legend_classes=[
                                    MVLegendClass('polygon', 'Polygons', fill='rgba(255,255,255,0.8)',
                                                  stroke='#3d9dcd'),
                                    MVLegendClass('line', 'Lines', stroke='#3d9dcd')
                                ])

        map_layers.append(geojson_layer)

        # Tiled ArcGIS REST Layer
        arc_gis_layer = MVLayer(source='TileArcGISRest',
                                options={'url': 'http://sampleserver1.arcgisonline.com/ArcGIS/rest/services/' +
                                                'Specialty/ESRI_StateCityHighway_USA/MapServer'},
                                legend_title='ESRI USA Highway',
                                legend_extent=[-173, 17, -65, 72])

        map_layers.append(arc_gis_layer)
        return map_layers
