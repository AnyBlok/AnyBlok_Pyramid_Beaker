# This file is a part of the AnyBlok / Pyramid / Beaker project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok_pyramid_beaker.config import (define_beaker_option,
                                           update_plugins)
from anyblok.tests.test_config import MockArgumentParser


@pytest.fixture(scope="function")
def parser():
    return MockArgumentParser()


class TestArgsParseOption:

    def test_define_beaker_option(self, parser):
        define_beaker_option(parser)

    def test_update_plugins(self, parser):
        update_plugins(parser)
