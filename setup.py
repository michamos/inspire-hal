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

"""Inspire service for pushing records to HAL"""

from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup


url = 'https://github.com/inspirehep/inspire-hal'

readme = open('README.rst').read()

setup_requires = [
    'autosemver~=0.0,>=0.5.3',
]

install_requires = [
    'celery~=4.0,>=4.1.0,<4.2.0',
    'Flask~=0.0,>=0.12.4',
    'Flask-CeleryExt~=0.0,>=0.3.1',
    'httplib2~=0.0,>=0.12.0',
    'inspire-dojson~=63.0',
    'inspire-schemas~=61.0',
    'inspire-utils~=3.0,>=3.0.0',
    'flask-shell-ipython<0.4.0',
    'invenio-app~=1.0,>=1.0.0',
    'invenio-base~=1.0,>=1.0.0',
    'invenio-config~=1.0,>=1.0.0',
    'invenio-db[postgresql,versioning]~=1.0,>=1.0.0',
    'invenio-pidstore==1.0.0',
    'invenio-records~=1.0,>=1.0.0',
    'langdetect~=1.0,>=1.0.7',
    'redis~=2.0,>=2.10.6',
    'SQLAlchemy~=1.0,>=1.2.5',
    'sword2@git+https://github.com/inspirehep/python-client-sword2.git',
    'urllib3==1.24.1',
    'zulip==0.5.8',
]

docs_require = []

tests_require = [
    'flake8-future-import~=0.0,>=0.4.4',
    'flake8~=3.0,>=3.5.0',
    'mock~=2.0,>=2.0.0',
    'pytest-cov~=2.0,>=2.5.1',
    'pytest~=3.0,>=3.5.0',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'tests:python_version=="2.7"': [
        'unicode-string-literal~=1.0,>=1.1',
    ],
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name not in ['all', 'tests:python_version=="2.7"']:
        extras_require['all'].extend(reqs)

packages = find_packages(exclude=['docs', 'tests'])

setup(
    name='inspire-hal',
    autosemver={
        'bugtracker_url': url + '/issues',
    },
    url=url,
    license='GPLv3',
    author='CERN',
    author_email='admin@inspirehep.net',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    description=__doc__,
    long_description=readme,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        "console_scripts": ["inspirehal = inspire_hal:cli"],
        "invenio_config.module": ["inspirehal = inspire_hal.config"],

    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
