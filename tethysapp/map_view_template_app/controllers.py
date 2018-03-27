from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.layouts import MapViewLayoutController
# from .app import MapViewTemplateApp as test   // This is a problem, not sure why bt it won't
# let me import the app as a package for reference...important for file storage
from tethys_sdk.gizmos import *


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
    # attr_table = False
    # nav_pane = False

    # template_name = "map_view_template_app/my_map_view_layout.html"
    toc_legend = True

    def build_map_view(self, request, *args, **kwargs):
        map_view_gizmo = MapView(
            height='600px',
            width='100%',
            controls=self.build_controls(request, args, kwargs),
            layers=self.build_layers(request, args, kwargs),
            view=self.build_mvview(request, args, kwargs),
            basemap=self.basemap,
            toc_legend=self.toc_legend,
            draw=self.build_mvdraw(request, args, kwargs),
        )
        return map_view_gizmo

    def build_layers(self, request, *args, **kwargs):
        """
        Custom layers.
        """
        map_layers = []

        kml_layer = MVLayer(source='KML',
                            options={'url': '/static/tethys_gizmos/data/model.kml'},
                            legend_title='Park City Watershed',
                            data={'tethys_toc':True},
                            legend_extent=[-111.60, 40.57, -111.43, 40.70],
                            legend_classes=[
                                MVLegendClass('polygon', 'Watershed Boundary', fill='#ff8000'),
                                MVLegendClass('line', 'Stream Network', stroke='#0000ff'),
                            ])
        test_layer = MVLayer(source='KML',
                            options={'url': '/static/tethys_gizmos/data/model.kml'},
                            legend_title='Park City Watershed (2)',
                            data={'tethys_toc':True},
                            legend_extent=[-111.60, 40.57, -111.43, 40.70],
                            legend_classes=[
                                MVLegendClass('polygon', 'Watershed Boundary', fill='#ff8000'),
                                MVLegendClass('line', 'Stream Network', stroke='#0000ff'),
                            ])

        map_layers.append(kml_layer)
        map_layers.append(test_layer)

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
                                editable=True,
                                legend_title='Test GeoJSON',
                                data={
                                      'tethys_toc':True,
                                      'resType':'GeographicFeatureResource',
                                     },
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
                                data={'tethys_toc':True},
                                legend_title='ESRI USA Highway',
                                legend_extent=[-173, 17, -65, 72])

        map_layers.append(arc_gis_layer)
        return map_layers
