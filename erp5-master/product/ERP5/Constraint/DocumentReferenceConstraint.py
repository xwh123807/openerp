##############################################################################
#
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#          Jerome Perrin <jerome@nexedi.com>
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

from Products.ERP5Type.Constraint import Constraint
translateString = lambda msg, **kw: msg # just to extract messages
_MARKER = []


class DocumentReferenceConstraint(Constraint):
  """
  This constraint checks if the document has all required coordinates
  (reference, version and language) and if there is no other document with
  the same coordinates.

  Fixing is not implemented on purpose
  (although we could, e.g. by changing version number)
  """

  _message_id_list = [ 'message_property_not_defined',
                       'message_another_document_exists',
                       'message_multiple_documents_exists' ]

  message_property_not_defined = translateString(
      'Property ${property_id} was not defined')
  message_another_document_exists = translateString(
      'Another document ${document_reference} - '
      '${document_language} - ${document_version} already exists')
  message_multiple_documents_exists = translateString(
      'Multiple (${document_count}) documents ${document_reference} - '
      '${document_language} - ${document_version} already exists')

  def _checkConsistency(self, document, fixit=0):
    """
      Implement here the consistency checker
    """
    # XXX we probably could check reference syntax here, based on regexp in
    # preferences?
    error_list = []

    for property_id in ('reference', 'language', 'version'):
      if document.getProperty(property_id) in (None, ''):
        error_list.append(self._generateError(document,
             self._getMessage('message_property_not_defined'),
             mapping=dict(property_id=property_id)))
    if error_list:
      return error_list

    # XXX isn't it better to use unrestrictedSearchResults ?
    #   potential problem is that we would get deleted documents aswell
    res = document.portal_catalog(reference=document.getReference(),
                                language=document.getLanguage(),
                                version=document.getVersion(),
                                portal_type=document.getPortalDocumentTypeList())
    res = list(res)
    if len(res) == 2: # this document and another document
      error_list.append(self._generateError(document,
                self._getMessage('message_another_document_exists'),
                mapping=dict(document_reference=document.getReference(),
                             document_language=document.getLanguage(),
                             document_version=document.getVersion())))

    if len(res) > 2:
      # this is very serious since there are many document with the same
      # reference
      error_list.append(self._generateError(document,
                self._getMessage('message_multiple_documents_exists'),
                mapping=dict(document_count=len(res),
                             document_reference=document.getReference(),
                             document_language=document.getLanguage(),
                             document_version=document.getVersion())))
    return error_list

