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

import json
import os
import pkg_resources

import pytest

from invenio_db import db
from invenio_records.models import RecordMetadata
from invenio_pidstore.models import PersistentIdentifier

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
        db.session.close()
        db.drop_all()
        db.create_all()
        yield app


def _get_fixture(filename):
    return pkg_resources.resource_string(
        __name__, os.path.join('fixtures', filename)
    )



@pytest.fixture
def create_record_from_fixture():
    def _create(pid_type, filename):
        data = json.loads(_get_fixture(filename))

        record = RecordMetadata(json=data)
        db.session.add(record)
        db.session.commit()

        pid = PersistentIdentifier(
            pid_type=pid_type,
            pid_value=data['control_number'],
            status='R',
            object_type='rec',
            object_uuid=record.id
        )
        db.session.add(pid)
        db.session.commit()

        return record
    return _create


@pytest.fixture
def delete_record(app):
    def _delete_record(rec_uuid):
        RecordMetadata.query.filter(RecordMetadata.id==rec_uuid).delete()
        PersistentIdentifier.query.filter(
            PersistentIdentifier.object_uuid == rec_uuid
        ).delete()
        db.session.commit()
    return _delete_record
