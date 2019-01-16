# -*- coding: utf-8 -*-
{
'name': 'Facturación Sunat',
'description': "Addon para enviar documentos a sunat",
'author': "Nakade",
    'website': "https://instagram.com",
    'summary': "Sunat",
    'version': '0.1',
    'category': 'module_category_account_voucher',
      # any module necessary for this one to work correctly
    'depends': ['base','account'],
 
    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}
