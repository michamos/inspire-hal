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

"""HAL utils."""

from __future__ import absolute_import, division, print_function

from itertools import chain

from elasticsearch import RequestError
from flask import current_app
from sqlalchemy import tuple_

from inspire_dojson.utils import get_recid_from_ref
from inspire_utils.name import ParsedName
from inspire_utils.record import get_value
from invenio_records.api import RecordMetadata
from invenio_pidstore.models import PersistentIdentifier


def get_authors(record):
    """Return the authors of a record.

    Queries the Institution records linked from the authors affiliations
    to add, whenever it exists, the HAL identifier of the institution to
    the affiliation.

    Args:
        record(InspireRecord): a record.

    Returns:
        list(dict): the authors of the record.

    Examples:
        >>> record = {
        ...     'authors': [
        ...         'affiliations': [
        ...             {
        ...                 'record': {
        ...                     '$ref': 'http://localhost:5000/api/institutions/902725',
        ...                 }
        ...             },
        ...         ],
        ...     ],
        ... }
        >>> authors = get_authors(record)
        >>> authors[0]['hal_id']
        '300037'

    """
    hal_id_map = _get_hal_id_map(record)

    result = []

    for author in record.get('authors', []):
        affiliations = []

        parsed_name = ParsedName.loads(author['full_name'])
        first_name, last_name = parsed_name.first, parsed_name.last

        for affiliation in author.get('affiliations', []):
            recid = get_recid_from_ref(affiliation.get('record'))
            if recid in hal_id_map and hal_id_map[recid]:
                affiliations.append({'hal_id': hal_id_map[recid]})

        result.append({
            'affiliations': affiliations,
            'first_name': first_name,
            'last_name': last_name,
        })

    return result


def get_conference_record(record, default=None):
    """Return the first Conference record associated with a record.

    Queries the database to fetch the first Conference record referenced
    in the ``publication_info`` of the record.

    Args:
        record(InspireRecord): a record.
        default: value to be returned if no conference record present/found

    Returns:
        InspireRecord: the first Conference record associated with the record.

    Examples:
        >>> record = {
        ...     'publication_info': [
        ...         {
        ...             'conference_record': {
        ...                 '$ref': '/api/conferences/972464',
        ...             },
        ...         },
        ...     ],
        ... }
        >>> conference_record = get_conference_record(record)
        >>> conference_record['control_number']
        972464

    """
    pub_info = get_value(record, 'publication_info.conference_record[0]')
    if not pub_info:
        return default

    conferences = get_db_records([('con', get_recid_from_ref(pub_info))])
    return conferences[0]


def get_divulgation(record):
    """Return 1 if a record is intended for the general public, 0 otherwise.

    Args:
        record(InspireRecord): a record.

    Returns:
        int: 1 if the record is intended for the general public, 0 otherwise.

    Examples:
        >>> get_divulgation({'publication_type': ['introductory']})
        1

    """
    return 1 if 'introductory' in get_value(record, 'publication_type', []) else 0


def get_domains(record):
    """Return the HAL domains of a record.

    Uses the mapping in the configuration to convert all INSPIRE categories
    to the corresponding HAL domains.

    Args:
        record(InspireRecord): a record.

    Returns:
        list(str): the HAL domains of the record.

    Examples:
        >>> record = {'inspire_categories': [{'term': 'Experiment-HEP'}]}
        >>> get_domains(record)
        ['phys.hexp']

    """
    terms = get_value(record, 'inspire_categories.term', default=[])
    mapping = current_app.config['HAL_DOMAIN_MAPPING']

    return [mapping[term] for term in terms]


def _get_hal_id_map(record):
    affiliation_records = chain.from_iterable(get_value(
        record, 'authors.affiliations.record', default=[]))
    affiliation_recids = [get_recid_from_ref(el) for el in affiliation_records]

    try:
        institutions = get_db_records([('ins', affiliation_recids)])
    except RequestError:
        institutions = []

    return {el['control_number']: _get_hal_id(el) for el in institutions}


def _get_hal_id(record):
    for el in record.get('external_system_identifiers', []):
        if el.get('schema') == 'HAL':
            return el['value']


def get_db_records(pids):
    """Get an iterator on record metadata from the DB.

    Args:
        pids (Iterable[Tuple[str, Union[str, int]]): a list of (pid_type, pid_value) tuples.

    Return:
        list(dict): metadata of the records found in the database.
    """
    pids = [(pid_type, str(pid_value)) for (pid_type, pid_value) in pids]

    if not pids:
        return

    query = RecordMetadata.query.join(
        PersistentIdentifier,
        RecordMetadata.id == PersistentIdentifier.object_uuid
    ).filter(
        PersistentIdentifier.object_type == 'rec',
        tuple_(
            PersistentIdentifier.pid_type,
            PersistentIdentifier.pid_value).in_(pids)
    )
    return [rec.json for rec in query.all()]
