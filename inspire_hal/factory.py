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

"""INSPIRE-HAL app factories."""

from __future__ import absolute_import, division, print_function

import os
import sys

from invenio_base.app import create_app_factory
from invenio_config import create_config_loader

from inspire_hal.cli import hal
from inspire_hal import config

env_prefix = 'APP'


def config_loader(app, **kwargs_config):
    invenio_config_loader = create_config_loader(config=config, env_prefix=env_prefix)
    result = invenio_config_loader(app, **kwargs_config)
    app.url_map.strict_slashes = False
    app.cli.add_command(hal)
    return result


instance_path = os.getenv(env_prefix + '_INSTANCE_PATH') or \
    os.path.join(sys.prefix, 'var', 'inspirehal-instance')
"""Instance path for Invenio.

Defaults to ``<env_prefix>_INSTANCE_PATH`` or if environment variable is not
set ``<sys.prefix>/var/<app_name>-instance``.
"""

create_app = create_app_factory(
    'inspire_hal',
    config_loader=config_loader,
    extension_entry_points=['invenio_base.apps'],
    instance_path=instance_path,
)

