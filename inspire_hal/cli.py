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


def get_env_var(var_name):
    try:
        value = current_app.config[var_name]
        return value
    except KeyError:
        print("Environment variable '{}' not set. Quitting.".format(var_name))
        sys.exit(1)


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
    print('Loading credentials and settings from local environment')

    username = get_env_var('HAL_USER_NAME')
    password = get_env_var('HAL_USER_PASS')
    db_user = get_env_var('DB_INSPIRE_USER')
    db_pass = get_env_var('DB_INSPIRE_PASSWORD')
    db_port = get_env_var('DB_PORT')
    db_uri = get_env_var('PROD_DB_HOST')

    # Optional configurations
    limit = current_app.config.get('HAL_LIMIT', 0)
    yield_amt = current_app.config.get('HAL_YIELD_AMT', 100)

    db_resource = 'postgresql+psycopg2://{}:{}@{}:{}/inspirehep'.\
        format(db_user, db_pass, db_uri, db_port)

    current_app.config.update(
        HAL_USER_NAME=username,
        HAL_USER_PASS=password,
        SQLALCHEMY_DATABASE_URI=db_resource
    )

    try:
        hal_push(limit=limit, yield_amt=yield_amt)

    except Exception as e:
        print ('ERROR: cannot connect to DB. Quitting.')
        print ('Exception:\n\n' + e.message)

