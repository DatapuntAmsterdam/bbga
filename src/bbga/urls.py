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

import collections

from django.conf.urls import include, url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import (
    permissions,
    response,
    reverse,
    routers,
    views)
from bbga_data import views as bbga_views

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

    def get_api_root_view(self, **kwargs):
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
    Basis Bestand Gebieden Amsterdam

    [dashboard](http://www.ois.amsterdam.nl/visualisatie/dashboard_kerncijfers.html)


    Specifieke functionaliteit voor de BBGA API.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class BBGA(cls):
            def get_view_name(self):
                return 'BBGA'

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
    r'meta', bbga_views.MetaViewSet, base_name='meta',
)

bbga.register(
    r'cijfers', bbga_views.CijfersViewSet, base_name='cijfers'
)


schema_view = get_schema_view(
    openapi.Info(
        title="BBGA API",
        default_version='v1',
        description="BBGA API",
        terms_of_service="https://data.amsterdam.nl/",
        contact=openapi.Contact(email="datapunt@amsterdam.nl"),
        license=openapi.License(name="license Not known yet."),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# root url
urlpatterns = [
    url(r'^bbga/docs/api-docs(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=None)),
    url('^bbga/docs/api-docs/$',
        schema_view.with_ui('swagger', cache_timeout=None)),
    url(r'^bbga/', include(bbga.urls)),
    url(r'^status/', include("health.urls"))
]
