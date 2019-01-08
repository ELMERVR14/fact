# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from pprint import pprint
import importlib
import os
from sunatservice.sunatservice import Service

class res_company(models.Model):  
        
    _inherit = 'res.company' 

    def on_change_vat(self): 
        xmlPath = os.path.dirname(os.path.abspath(__file__))+'/xml'
        for record in self:
            if (record.vat) :
                ruc = record.vat
                if(ruc!=""):
                    SunatService = Service()
                    SunatService.setXMLPath(xmlPath)
                    response = {}
                    response = SunatService.consultRUC(ruc)
                    if not response:
                        raise Warning("El RUC no fue encontrado en registros de SUNAT")
                    else:
                        self.street = response['address']
                        self.name = response["name"]
