##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
"""
Products.ERP5Type.interfaces.category_access_provider
"""

from zope.interface import Interface

class ICategoryAccessProvider(Interface):
  """
    This interface defines the methods which must be implemented
    by a class in order to support Category accessors.
  """

  def _getAcquiredCategoryMembershipList(category, spec=(), filter=None,
      portal_type=(), base=0, keep_default=1, checked_permission=None, **kw):
    """
    Returns the membership for this category, with acquired membership.

      spec --

      filter --

      base --

      keep_default --

      checked_permission --

      kw --
    """

  def _getCategoryMembershipList(category, spec=(), filter=None, portal_type=(), base=0,
                                 keep_default=1, checked_permission=None, **kw):
    """
    Returns the membership for this category, without acquired membership.

    """

  def _getDefaultCategoryMembership(category, spec=(), filter=None, portal_type=(), base=0,
                                    default=None, checked_permission=None, **kw):
    """
    Returns the default membership for this category, without acquisition.

      default -- an optional default value, if no membership is found

    """

  def _getDefaultAcquiredCategoryMembership(category, spec=(), filter=None, portal_type=(), base=0,
                                    default=None, checked_permission=None, **kw):
    """
    Returns the default membership for this category, with acquisition.

      default -- an optional default value, if no membership is found

    """
