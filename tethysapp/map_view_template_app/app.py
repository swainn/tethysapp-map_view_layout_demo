from tethys_sdk.base import TethysAppBase, url_map_maker



class MapViewTemplateApp(TethysAppBase):
    """
    Tethys app class for Map View Template App.
    """

    name = 'Map View Template App'
    index = 'map_view_template_app:home'
    icon = 'map_view_template_app/images/icon.gif'
    package = 'map_view_template_app'
    root_url = 'map-view-template-app'
    color = '#2ecc71'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        from controllers import MyMapViewLayoutController
        # from tethys_sdk.layouts import MapViewLayoutController
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='map-view-template-app',
                           controller='map_view_template_app.controllers.home'),
                    UrlMap(name='map',
                           url='map-view-template-app/map',
                           controller=MyMapViewLayoutController.as_view()),
        )

        return url_maps
