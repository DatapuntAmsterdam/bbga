"""bbga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
# from django.contrib import admin

from bbga_data import views as bbga_views

import collections

from rest_framework import routers, views, reverse, response


# stack overflow hack
# http://stackoverflow.com/questions/18817988/using-django-rest-frameworks-browsable-api-with-apiviews

class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}

    def add_api_view(self, name, url):
        self._api_view_urls[name] = url

    def remove_api_view(self, name):
        del self._api_view_urls[name]

    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self):
        # Copy the following block from Default Router
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_view_urls = self._api_view_urls

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse.reverse(
                        url_name, request=request, format=format)

                # In addition to what had been added, now add the APIView urls
                for api_view_key in api_view_urls.keys():
                    ret[api_view_key] = reverse.reverse(
                        api_view_urls[api_view_key].name,
                        request=request, format=format)

                # sort the damn thing
                od = collections.OrderedDict(sorted(ret.items()))

                return response.Response(od)

        return APIRoot.as_view()


class BBGARouter(HybridRouter):
    """
    Basisbestand Gebieden Amsterdam

    [dashboard](http://www.ois.amsterdam.nl/visualisatie/dashboard_kerncijfers.html)


    Specifieke functionaliteit voor de BBGA API.
    """

    def get_api_root_view(self):
        view = super().get_api_root_view()
        cls = view.cls

        class BBGA(cls):
            pass

        BBGA.__doc__ = self.__doc__
        return BBGA.as_view()


bbga = BBGARouter()

# browsable links
bbga.add_api_view(
    'groepen',
    url(r'^groepen/', bbga_views.meta_groepen, name='groepen'))

bbga.add_api_view(
    'themas',
    url(r'^themas/', bbga_views.meta_themas, name='themas'))

bbga.add_api_view(
    'variabelen',
    url(r'^variabelen/', bbga_views.meta_variabelen, name='variabelen')
)

bbga.add_api_view(
    'gebieden',
    url(r'^gebieden/', bbga_views.meta_gebiedcodes, name='gebieden')
)


bbga.register(
    r'meta', bbga_views.MetaViewSet, base_name='bbga/meta',
)


bbga.register(
    r'cijfers', bbga_views.CijfersViewSet, base_name='bbga/cijfers'
)


# root url
urlpatterns = [
    url(r'^bbga/docs/', include('rest_framework_swagger.urls')),
    url(r'^bbga/', include(bbga.urls)),
    url(r'^status/', include("datapunt_generic.health.urls"))
]
