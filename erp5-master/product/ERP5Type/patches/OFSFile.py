from App.special_dtml import DTMLFile
from OFS.Image import File
from Products.ERP5Type import _dtmldir

# Patch for displaying textearea in full window instead of
# remembering a quantity of lines to display in a cookie
manage_editForm = DTMLFile("fileEdit", _dtmldir)
manage_editForm._setName('manage_editForm')
File.manage_editForm = manage_editForm
File.manage = manage_editForm
File.manage_main = manage_editForm
File.manage_editDocument = manage_editForm
File.manage_editForm = manage_editForm
