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


from inspire_schemas.api import load_schema, validate
from inspire_hal.utils import get_conference_record


def test_get_conference_record(app, create_record_from_fixture, delete_record):
    rec_fixture = create_record_from_fixture('con', 'get_conference_record.json')

    schema = load_schema('hep')
    control_number_schema = schema['properties']['control_number']
    publication_info_schema = schema['properties']['publication_info']

    conference_record = {'control_number': 972464}
    assert validate(conference_record['control_number'], control_number_schema) is None

    record = {
        'publication_info': [
            {
                'conference_record': {
                    '$ref': 'http://localhost:5000/api/conferences/972464',
                },
            },
        ],
    }
    assert validate(record['publication_info'], publication_info_schema) is None

    expected = 972464

    result = get_conference_record(record)
    assert expected == result['control_number']

    delete_record(rec_fixture.id)
