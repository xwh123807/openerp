from Products.ERP5.Tool.Category import addBaseCategory
from Products.ERP5Type.Utils import convertToUpperCase

# This script defines init values for all base categories

def setBaseAcquisition(self):
  pc = self.portal_categories
  # Source and destination are defined by delivery, order, parent
  #   we should not use causality here because of production reports
  #   for which source or destination can be None (ie. different from Production Order)
  for bc in ('source', 'destination',
             'source_section', 'destination_section',):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList(('delivery', 'order', 'parent', ))
    pc[bc].setAcquisitionPortalTypeList('python: list( ' +
                                        'portal.getPortalAcquisitionMovementTypeList() + ' +
                                        'portal.getPortalItemTypeList() + ' +
                                        'portal.getPortalDeliveryTypeList() + ' +
                                        'portal.getPortalOrderTypeList() + ' +
                                        'portal.getPortalInvoiceTypeList()' +
                                        ')')
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
  # Other sources and destination are defined by delivery, order, parent or causality
  # None of those base categories should be set to None (incl. section)
  for bc in ('source_payment', 'destination_payment',
             'source_decision', 'destination_decision',
             'source_administration', 'destination_administration', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList(('delivery', 'order', 'parent', 'causality'))
    pc[bc].setAcquisitionPortalTypeList('python: list( ' +
                                        'portal.getPortalAcquisitionMovementTypeList() + ' +
                                        'portal.getPortalItemTypeList() + ' +
                                        'portal.getPortalDeliveryTypeList() + ' +
                                        'portal.getPortalOrderTypeList() + ' +
                                        'portal.getPortalInvoiceTypeList()' +
                                        ')')
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
  # Resource is defined by delivery, order or parent
  for bc in ('resource', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList(('delivery', 'order', 'parent'))
    pc[bc].setAcquisitionPortalTypeList('python: list( ' +
                                        'portal.getPortalAcquisitionMovementTypeList() + ' +
                                        'portal.getPortalItemTypeList() + ' +
                                        'portal.getPortalDeliveryTypeList() + ' +
                                        'portal.getPortalOrderTypeList() + ' +
                                        'portal.getPortalInvoiceTypeList()' +
                                        ')')
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
  # Coramy Specific for Variations
  for bc in ('coloris', 'taille', 'variante', 'morphologie' ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList(('delivery', 'order', 'parent', ))
    pc[bc].setAcquisitionPortalTypeList('python: list( ' +
                                        'portal.getPortalAcquisitionMovementTypeList() + ' +
                                        'portal.getPortalItemTypeList() + ' +
                                        'portal.getPortalDeliveryTypeList() + ' +
                                        'portal.getPortalOrderTypeList() + ' +
                                        'portal.getPortalInvoiceTypeList()' +
                                        ')')
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
  # Coramy Specific for Quantity Unit
  for bc in ('quantity_unit', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList(('delivery', 'order', 'parent', 'resource'))
    pc[bc].setAcquisitionPortalTypeList('python: list( ' +
                                        'portal.getPortalAcquisitionMovementTypeList() + ' +
                                        'portal.getPortalItemTypeList() + ' +
                                        'portal.getPortalDeliveryTypeList() + ' +
                                        'portal.getPortalOrderTypeList() + ' +
                                        'portal.getPortalInvoiceTypeList() + ' +
                                        'portal.getPortalResourceTypeList()' +
                                        ')')
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
  # Add some useful bcs
  for bc in ('parent', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
  # Region acquisition
  for bc in ('region', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList('subordination',)
    pc[bc].setAcquisitionPortalTypeList("python: ['Address', 'Organisation', 'Person']")
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
    pc[bc].setAcquisitionObjectIdList(['default_address'])
  # Subordination acquisition
  for bc in ('subordination', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    #pc[bc].setAcquisitionBaseCategoryList()
    pc[bc].setAcquisitionPortalTypeList("python: ['Career', ]")
    pc[bc].setAcquisitionMaskValue(0)
    pc[bc].setAcquisitionCopyValue(0)
    pc[bc].setAcquisitionAppendValue(0)
    pc[bc].setAcquisitionObjectIdList(['default_career'])
  # Immobilisation acquisition
  for bc in ('input_account', 'output_account', 'immobilisation_account',
             'amortisation_account', 'depreciation_account', 'vat_account',
             'amortisation_type', ):
    if not hasattr(pc, bc):
      addBaseCategory(pc, bc)
    pc[bc].setAcquisitionBaseCategoryList('parent',)
    pc[bc].setAcquisitionPortalTypeList('python: list(portal.getPortalItemTypeList())')
    pc[bc].setAcquisitionMaskValue(1)
    pc[bc].setAcquisitionCopyValue(1)
    pc[bc].setAcquisitionAppendValue(0)


  return '<html><body><p>Acquisition Done</p></body></html>'


