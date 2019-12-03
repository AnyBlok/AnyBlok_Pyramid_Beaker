# This file is a part of the AnyBlok / Pyramid / Beaker project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest  # noqa
from anyblok.config import Configuration
from pyramid.response import Response
from anyblok_pyramid_beaker.config import get_db_name
from anyblok_pyramid.testing import init_web_server


def update_session_db_name(request):
    request.session['dbname'] = 'other_db_name'
    request.session.save()
    return Response('login')


def update_session_db_name2(request):
    request.session['dbname'] = None
    request.session.save()
    return Response('logout')


def _get_db_name(request):
    if request.anyblok and request.anyblok.registry:
        return Response(request.anyblok.registry.db_name)

    return Response('other_db_name')


def add_route_and_views(config):
    config.add_route('dbname-login', '/test/login/')
    config.add_view(update_session_db_name, route_name='dbname-login')
    config.add_route('dbname-logout', '/test/logout/')
    config.add_view(update_session_db_name2, route_name='dbname-logout')
    config.add_route('dbname', '/test/')
    config.add_view(_get_db_name, route_name='dbname')


class TestRegistry:

    def test_registry_by_default_method(self, registry_blok):
        webserver = init_web_server(add_route_and_views)
        res = webserver.get('/test/', status=200)
        assert Configuration.get('db_name') == res.body.decode('utf8')
        webserver.get('/test/login/')
        res = webserver.get('/test/', status=200)
        assert 'other_db_name' == res.body.decode('utf8')
        webserver.get('/test/logout/')
        res = webserver.get('/test/', status=200)
        assert Configuration.get('db_name') == res.body.decode('utf8')

    def test_plugin(self):
        assert Configuration.get('get_db_name') == get_db_name
