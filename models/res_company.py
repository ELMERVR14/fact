# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from pprint import pprint
import importlib
import os
from sunatservice.sunatservice import Service

class res_company(models.Model):  
        
    _inherit = 'res.company' 
    sol_ruc = fields.Text(name="sol_ruc", string="RUC", default='20603408111')
    sol_username = fields.Text(name="sol_username", string="Usuario", default='20603408111MODDATOS')
    sol_password = fields.Text(name="sol_password", string="Contraseña", default='moddatos')
    api_mode = fields.Selection([('SANDBOX','SANDBOX'),('PRODUCTION','PRODUCTION')], string='Modo Servicio', default='SANDBOX')

      #def on_change_vat(self): 
      #    xmlPath = os.path.dirname(os.path.abspath(__file__))+'/xml'
      #    for record in self:
      #        if (record.vat) :
      #            ruc = record.vat
      #            if(ruc!=""):
      #                SunatService = Service()
      #                SunatService.setXMLPath(xmlPath)
      #                response = {}
      #                response = SunatService.consultRUC(ruc)
      #                if not response:
      #                    raise Warning("El RUC no fue encontrado en registros de SUNAT")
      #                else:
      #                    self.street = response['address']
      #                    self.name = response["name"]
    