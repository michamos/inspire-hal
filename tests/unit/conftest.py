# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2019 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import pytest

from inspire_hal.factory import create_app


@pytest.fixture(scope='session')
def app():
    """
    Deprecated: do not use this fixture for new tests, unless for very
    specific use cases. Use `isolated_app` instead.

    Flask application with demosite data and without any database isolation:
    any db transaction performed during the tests are persisted into the db.

    Creates a Flask application with a simple testing configuration,
    then creates an application context and inside of it recreates
    all databases and indices from the fixtures. Finally it yields,
    so that all tests that explicitly use the ``app`` fixture have
    access to an application context.

    See: http://flask.pocoo.org/docs/0.12/appcontext/.
    """
    app = create_app(
        DEBUG=False,
        SECRET_KEY='secret!',
        TESTING=True,
    )

    with app.app_context() as app:
        yield app
