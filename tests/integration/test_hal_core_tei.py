# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2019 CERN.
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

import os

import pkg_resources
import pytest
from lxml import etree

from invenio_db import db
from invenio_records.api import RecordMetadata
from invenio_search.api import current_search_client as es

from inspire_hal.core.tei import convert_to_tei
from inspire_hal.utils import get_db_records


@pytest.fixture(scope='function')
def cern_with_hal_id(app):
    """Temporarily add the HAL id to the CERN record."""
    record = get_db_records[('ins', 902725)]
    record['external_system_identifiers'] = [{'schema': 'HAL', 'value': '300037'}]
    record = RecordMetadata(record)
    db.session.add(record)
    db.session.commit()
    es.indices.refresh('records-institutions')

    yield

    record = get_db_records[('ins', 902725)]
    del record.json['external_system_identifiers']
    from sqlalchemy import update
    update(RecordMetadata).where(RecordMetadata.id == record.id).values(json=record.json)
    db.session.commit()
    es.indices.refresh('records-institutions')


def test_convert_to_tei(app, create_record_from_fixture, delete_record):
    rec_fixture = create_record_from_fixture('lit', 'convert_to_tei.json')
    recid = rec_fixture.json['control_number']

    record = get_db_records([('lit', recid)])[0]

    schema = etree.XMLSchema(
        etree.parse(
            pkg_resources.resource_stream(
                __name__, os.path.join('fixtures', 'aofr.xsd')
            )
        )
    )
    result = etree.fromstring(convert_to_tei(record).encode('utf8'))
    assert schema.validate(result)

    delete_record(rec_fixture.id)


def test_convert_to_tei_handles_preprints(
    app,
    create_record_from_fixture,
    delete_record,
):
    rec_fixture = create_record_from_fixture('lit', 'convert_to_tei_handles_preprints.json')
    recid = rec_fixture.json['control_number']

    record = get_db_records([('lit', recid)])[0]

    schema = etree.XMLSchema(
        etree.parse(
            pkg_resources.resource_stream(
                __name__, os.path.join('fixtures', 'aofr.xsd'))
        )
    )
    result = etree.fromstring(convert_to_tei(record).encode('utf8'))
    assert schema.validate(result)

    delete_record(rec_fixture.id)
