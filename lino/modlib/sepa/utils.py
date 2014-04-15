# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""This defines a function `belgian_nban_to_iban_bic` which returns
the IBAN and BIC of a Belgian "old-style" "national" bank account
number.

Instead of maintaining our own mapping of bank numbers -> BIC code, we
currently use www.ibanbic.be SOAP service.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from suds.client import Client

_CLIENT = None


def client():
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    url = 'http://www.ibanbic.be/IBANBIC.asmx?WSDL'
    _CLIENT = Client(url)
    return _CLIENT


def belgian_nban_to_iban_bic(s):
    
    s = client().service.BBANtoIBANandBIC(s)
    return s.split('#')

if __name__ == '__main__':
 
    print belgian_nban_to_iban_bic("001-1148294-84")
