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

"""INSPIRE-HAL cli."""
from __future__ import absolute_import, division, print_function

import sys

import click

from flask import current_app
from flask.cli import with_appcontext

from inspire_hal.tasks import hal_push


@click.group()
def hal():
    pass


@hal.command()
@with_appcontext
def push():
    """Push to HAL api.

    By default the push is done to the HAL **preprod** environment.
    To push to the production environment overwrite in the environment the
    variables `APP_HAL_COL_IRI` and `HAL_EDIT_IRI`.
    """
    # Optional configurations
    limit = current_app.config.get('HAL_LIMIT', 0)
    yield_amt = current_app.config.get('HAL_YIELD_AMT', 100)

    try:
        hal_push(limit=limit, yield_amt=yield_amt)

    except Exception as e:
        print ('ERROR: cannot connect to DB. Quitting.')
        print ('Exception:\n\n' + e.message)

