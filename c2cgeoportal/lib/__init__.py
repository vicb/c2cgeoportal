# -*- coding: utf-8 -*-

from pyramid.interfaces import IRoutePregenerator, \
    IStaticURLInfo
from zope.interface import implementer
from random import randint
from pyramid.compat import WIN
from pyramid.config.views import StaticURLInfo


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

@implementer(IStaticURLInfo)
class MultiDommainStaticURLInfo(StaticURLInfo):
    def generate(self, path, request, **kw):
        registry = request.registry
        for (url, spec, route_name) in self._get_registrations(registry):
            if path.startswith(spec):
                subpath = path[len(spec):]
                if WIN:
                    subpath = subpath.replace('\\', '/') # windows
                print url
                if url is None:
                    kw['subpath'] = subpath
                    print route_name
                    return request.route_url(route_name, **kw)
                else:
                    subpath = url_quote(subpath)
                    return urljoin(url, subpath)
        raise ValueError('No static URL definition matching %s' % path)

    def add(self, config, name, spec, **extra):
        if 'pregenerator' not in extra:
            extra['pregenerator'] = MultiDommainPregenerator()
        print extra
        return super(MultiDommainStaticURLInfo, self) \
            .add(config, name, spec, **extra)
