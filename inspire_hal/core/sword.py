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

"""HAL SWORD core."""

from __future__ import absolute_import, division, print_function

from tempfile import TemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile

import httplib2
from flask import current_app
from sword2 import Connection
from sword2.http_layer import HttpLib2Layer


def create(tei, doc_file=None):
    """Create a record on HAL using the SWORD2 protocol."""
    connection = _new_connection()
    payload, mimetype, filename = _create_payload(tei, doc_file)

    col_iri = current_app.config['HAL_COL_IRI']

    return connection.create(
        col_iri=col_iri,
        payload=payload,
        mimetype=mimetype,
        filename=filename,
        packaging='http://purl.org/net/sword-types/AOfr',
        in_progress=False,
    )


def update(tei, hal_id, doc_file=None):
    """Update a record on HAL using the SWORD2 protocol."""
    override_headers = {}
    if current_app.config.get('HAL_DISABLE_AFFILIATION_UPDATE'):
        override_headers['LoadFilter'] = 'noaffiliation'

    connection = _new_connection(override_headers=override_headers)
    payload, mimetype, filename = _create_payload(tei, doc_file)

    edit_iri = current_app.config['HAL_EDIT_IRI'] + hal_id
    edit_media_iri = edit_iri

    return connection.update(
        edit_iri=edit_iri,
        edit_media_iri=edit_media_iri,
        payload=payload,
        mimetype=mimetype,
        filename=filename,
        packaging='http://purl.org/net/sword-types/AOfr',
        in_progress=False,
    )


class HttpLib2LayerWithCustomOptions(HttpLib2Layer):
    def __init__(self, override_headers=None, *args, **kwargs):
        self.h = httplib2.Http(*args, **kwargs)
        self.override_headers = override_headers

    def request(self, uri, method, headers=None, payload=None):
        if self.override_headers:
            headers = headers.copy()
            headers.update(self.override_headers)
        return super(HttpLib2LayerWithCustomOptions, self).request(
            uri=uri, method=method, headers=headers, payload=payload
        )


def _new_connection(override_headers=None):
    user_name = current_app.config['HAL_USER_NAME']
    user_pass = current_app.config['HAL_USER_PASS']
    timeout = current_app.config['HAL_CONNECTION_TIMEOUT']
    ignore_cert = current_app.config.get('HAL_IGNORE_CERTIFICATES', False)
    http_impl = HttpLib2LayerWithCustomOptions(
        '.cache',
        timeout=timeout,
        disable_ssl_certificate_validation=ignore_cert,
        override_headers=override_headers
    )


    return Connection(
        '', user_name=user_name, user_pass=user_pass, http_impl=http_impl
    )


def _create_payload(tei, doc_file):
    if doc_file:
        temp_file = TemporaryFile()
        with ZipFile(temp_file, mode='w', compression=ZIP_DEFLATED) as zf:
            zf.writestr('meta.xml', tei)
            zf.write(doc_file, 'doc.pdf')
        temp_file.seek(0)

        return temp_file, 'application/zip', 'meta.xml'

    return tei, 'text/xml', 'meta.xml'
