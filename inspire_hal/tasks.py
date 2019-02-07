# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2018 - 2019 CERN.
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

"""HAL tasks."""

from __future__ import absolute_import, division, print_function

import zulip

from inspire_hal.bulk_push import run


def hal_push(limit, yield_amt):
    """Run a hal push."""

    print('HAL: Starting to process HAL records')
    send_start_message()

    total, now, ok, ko = run(
        limit=limit,
        yield_amt=yield_amt,
    )

    print(
        'HAL: Finished, %s records processed in %s: %s ok, %s ko'
        % (total, now, ok, ko)
    )
    send_summary(
        total=total,
        ok=ok,
        now=now,
        ko=ko,
    )


def send_start_message():
    message = '''Hal push **started**! :rocket:'''
    send_to_zulip(message)


def send_summary(total, ok, now, ko):
    summary = '''Hal push has **finished**!

Processed %s records in %s
* %s succeded 
* %s failed
    ''' % (total, now, ok, ko)
    send_to_zulip(summary)


def send_to_zulip(message):
    client = zulip.Client()

    request = {
        "type":    "stream",
        "to":      "ops",
        "subject": "HAL PUSH",
        "content": message,
    }
    response = client.send_message(request)
    if response.get("result") == "success":
        print ('New message sent to Zulip/ops/HAL_PUSH')
    else:
        print("Error sending the message to Zulip: %s" % response)
