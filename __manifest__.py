# -*- coding: utf-8 -*-
{
'name': 'API / FacturaOnline.pe SUNAT',
'description': "Conecta con la API facturacion online  para aplicar legalidad fiscal en Peru / SUNAT",
'author': "Rockscripts",
    'website': "https://instagram.com/rockscripts",
    'summary': "Peru / SUNAT facturaonline.pe",
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
