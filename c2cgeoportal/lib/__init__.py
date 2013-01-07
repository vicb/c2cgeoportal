# -*- coding: utf-8 -*-

from pyramid.interfaces import IRoutePregenerator, \
    IStaticURLInfo
from zope.interface import implementer
from random import randint


def get_setting(settings, path, default=None):
    value = settings
    for p in path:
        if value and p in value:
            value = value[p]
        else:
            return default
    return value if value else default

@implementer(IRoutePregenerator)
class MultiDommainPregenerator:
    def __call__(self, request, elements, kw):
        app_url = request.registry.settings['app_url']
        if isinstance(app_url, list):
            index = kw['url_index'] if 'url_index' in kw \
                    else randint(0, len(app_url) - 1)
            kw['_app_url'] = app_url[index]
        return elements, kw
