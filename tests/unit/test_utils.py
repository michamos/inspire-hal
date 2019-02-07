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
from inspire_hal.utils import (
    get_divulgation,
    get_domains,

)


def test_get_divulgation():
    schema = load_schema('hep')
    subschema = schema['properties']['publication_type']

    record = {
        'publication_type': [
            'introductory',
        ],
    }
    assert validate(record['publication_type'], subschema) is None

    expected = 1
    result = get_divulgation(record)

    assert expected == result


def test_get_domains(app):
    schema = load_schema('hep')
    subschema = schema['properties']['inspire_categories']

    record = {
        'inspire_categories': [
            {'term': 'Experiment-HEP'},
        ],
    }
    assert validate(record['inspire_categories'], subschema) is None

    expected = ['phys.hexp']
    result = get_domains(record)

    assert expected == result
