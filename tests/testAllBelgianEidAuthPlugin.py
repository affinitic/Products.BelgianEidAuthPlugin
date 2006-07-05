# -*- coding: utf-8 -*-
#
# File: testAllBelgianEidAuthPlugin.py
#
# Copyright (c) 2006 by CommunesPlone
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
from AccessControl import Unauthorized

from AccessControl.SecurityManagement import getSecurityManager

from Products.CMFCore.permissions import View


##/code-section module-header

#
# Test-cases for class(es) 
#

from Testing import ZopeTestCase
from Products.BelgianEidAuthPlugin.config import *
from Products.BelgianEidAuthPlugin.tests.BaseBelgianEidAuthPluginTestCase import BaseBelgianEidAuthPluginTestCase

# Import the tested classes

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testAllBelgianEidAuthPlugin(BaseBelgianEidAuthPluginTestCase):
    """Test-cases for class(es) ."""

    ##code-section class-header_testAllBelgianEidAuthPlugin #fill in your manual code here
    ##/code-section class-header_testAllBelgianEidAuthPlugin

    def afterSetUp(self):
        """

        """
        BaseBelgianEidAuthPluginTestCase.afterSetup(self)

    # Manually created methods



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAllBelgianEidAuthPlugin))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


