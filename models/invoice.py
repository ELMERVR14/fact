# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from pprint import pprint
import time
from datetime import datetime
import hmac
import hashlib
import requests 
import json
import os
from decimal import Decimal
from sunatservice.sunatservice import Service

class account_invoice(models.Model):

    _inherit = 'account.invoice'
    
    #diario = fields.Selection([('factura','Factura'),('boleta','Boleta'),('creadito','Nota Crédito'),('debito','Nota Débito')], string='Diario', default='factura')
    api_message = fields.Text(name="api_message", string="Estado", default='Documento contable sin emitir.')
    discrepance_code = fields.Text(name="discrepance_code", default='')
    discrepance_text = fields.Text(name="discrepance_text", string="Discrepancia", default='')
    #_columns = { 'api_message': fields.Text('Estado'), 'diario':fields.Selection([('factura','Factura'),('boleta','Boleta'),('creadito','Nota Crédito'),('debito','Nota Débito')], string='Diario')}
    _columns = { 'api_message': fields.Text('Estado'),'discrepance': fields.Text('Discrepancia')}
    _defaults = {'api_message':'Documento contable sin emitir.','diario':'factura','discrepance':''}

    @api.multi
    def invoice_validate(self):
        tipo_documento_consultar = self.journal_id.code

        if(tipo_documento_consultar=="NCR"):
            invoice_items = []
            total_venta_gravada = 0.0
            total_venta = 0.0
            sumatoria_ivg = 0.0
            
            for invoice in self:            
                items = invoice.invoice_line_ids
                for item in items:
                    index = 0
                    for taxes in invoice.tax_line_ids:
                    
                        if(index==0):
                            impuesto = taxes.tax_id.amount/100
                            valor_venta = (item.price_unit * item.quantity)                        
                            monto_afectacion_IGV = valor_venta * impuesto                   
                            precio_unitario = (item.price_unit * impuesto) + item.price_unit
                            invoice_item = {
                                                'cantidad':str(item.quantity), 
                                                'descripcion':item.name, 
                                                'valorVenta':valor_venta, 
                                                'valorUnitario':item.price_unit, 
                                                'precioVentaUnitario':precio_unitario, 
                                                'tipoPrecioVentaUnitario':'01', 
                                                'montoAfectacionIgv':monto_afectacion_IGV, 
                                                'tipoAfectacionIgv':'10',
                                                'unidadMedidaCantidad':'ZZ'
                                            }
                            invoice_items.append(invoice_item)
                            total_venta_gravada += valor_venta
                            total_venta += precio_unitario
                            sumatoria_ivg += monto_afectacion_IGV
                            index=index+1

           
            serieParts = str(invoice.number).split("-")             
            serieConsecutivoString = serieParts[0]
            serieConsecutivo = serieParts[1]
            currentDateTime = datetime.now()
            currentTime = currentDateTime.strftime("%H:%M:%S")
            data = {
                    'serie': str(serieConsecutivoString),
                    "numero":str(serieConsecutivo),
                    "emisor":{
                        "tipo":6,
                        "nro":invoice.company_id.sol_ruc,
                        "nombre":invoice.company_id.name,
                        "direccion":invoice.company_id.street,
                        "ciudad":invoice.company_id.city,
                        "departamento":invoice.company_id.state_id.name,
                        "codigoPostal":invoice.company_id.zip,
                        "codigoPais":invoice.company_id.country_id.code
                     },
                    "receptor": {
                            "tipo": 6,
                            "nro": invoice.partner_id.vat,
                            "nombre":invoice.partner_id.name,
                            "direccion":invoice.partner_id.street,
                        },
                    "tipoDocumento":"01",
                    "notaDescripcion":self.name,
                    "notaDiscrepanciaCode":self.discrepance_code,
                    "documentoOrigen":self.origin,
                    "fechaEmision":str(invoice.date_invoice).replace("/","-",3),
                    "fechaVencimiento":str(invoice.date_due).replace("/","-",3),
                    "horaEmision":currentTime,
                    'totalVentaGravada': total_venta_gravada,
                    'sumatoriaIgv': str(round(float(sumatoria_ivg),2)),
                    'totalVenta': total_venta,
                    'tipoMoneda': invoice.currency_id.name,
                    'items':invoice_items,
                    'sol':{
                            'usuario':invoice.company_id.sol_username,
                            'clave':invoice.company_id.sol_password
                          }
                    }
            #
            xmlPath = os.path.dirname(os.path.abspath(__file__))+'/xml'
            SunatService = Service()
            SunatService.setXMLPath(xmlPath)
            SunatService.fileName = str(invoice.company_id.sol_ruc)+"-07-"+str(serieConsecutivoString)+"-"+str(serieConsecutivo)
            SunatService.initSunatAPI(invoice.company_id.api_mode, "sendBill")
            sunatResponse = SunatService.processCreditNote(data)

            #with open('/home/rockscripts/Documents/data1.json', 'w') as outfile:
            #    json.dump(data, outfile)
                        
            if(sunatResponse["status"] == "OK"):
                self.api_message = "ESTADO: "+str(sunatResponse["status"])+"\n"+"REFERENCIA: "+str(sunatResponse["body"]["referencia"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"]["description"])
                return super(account_invoice, self).invoice_validate()
            else:
                errorMessage = "ESTADO: "+str(sunatResponse["status"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"])+"\n"+"CÓDIGO ERROR: "+str(sunatResponse["code"])
                raise Warning(errorMessage)
            
            

        elif(tipo_documento_consultar=="NDB"):
            invoice_items = []
            total_venta_gravada = 0.0
            total_venta = 0.0
            sumatoria_ivg = 0.0
            
            for invoice in self:            
                items = invoice.invoice_line_ids
                for item in items:
                    index = 0
                    for taxes in invoice.tax_line_ids:
                    
                        if(index==0):
                            impuesto = taxes.tax_id.amount/100
                            valor_venta = (item.price_unit * item.quantity)                        
                            monto_afectacion_IGV = valor_venta * impuesto                   
                            precio_unitario = (item.price_unit * impuesto) + item.price_unit
                            invoice_item = {
                                                'cantidad':str(item.quantity), 
                                                'descripcion':item.name, 
                                                'valorVenta':valor_venta, 
                                                'valorUnitario':item.price_unit, 
                                                'precioVentaUnitario':precio_unitario, 
                                                'tipoPrecioVentaUnitario':'01', 
                                                'montoAfectacionIgv':monto_afectacion_IGV, 
                                                'tipoAfectacionIgv':'10',
                                                'unidadMedidaCantidad':"ZZ",
                                            }
                            invoice_items.append(invoice_item)
                            total_venta_gravada += valor_venta
                            total_venta += precio_unitario
                            sumatoria_ivg += monto_afectacion_IGV
                            index=index+1

            serieParts = str(invoice.number).split("-")             
            serieConsecutivoString = serieParts[0]
            serieConsecutivo = serieParts[1]
            currentDateTime = datetime.now()
            currentTime = currentDateTime.strftime("%H:%M:%S")
            data = {
                    'serie': str(serieConsecutivoString),
                    "numero":str(serieConsecutivo),
                    "emisor":{
                        "tipo":6,
                        "nro":invoice.company_id.sol_ruc,
                        "nombre":invoice.company_id.name,
                        "direccion":invoice.company_id.street,
                        "ciudad":invoice.company_id.city,
                        "departamento":invoice.company_id.state_id.name,
                        "codigoPostal":invoice.company_id.zip,
                        "codigoPais":invoice.company_id.country_id.code
                     },
                    "receptor": {
                            "tipo": 6,
                            "nro": invoice.partner_id.vat,
                            "nombre":invoice.partner_id.name,
                            "direccion":invoice.partner_id.street,
                        },
                    "tipoDocumento":"01",
                    "notaDescripcion":self.name,
                    "notaDiscrepanciaCode":self.discrepance_code,
                    "documentoOrigen":self.origin,
                    "fechaEmision":str(invoice.date_invoice).replace("/","-",3),
                    "fechaVencimiento":str(invoice.date_due).replace("/","-",3),
                    "horaEmision":currentTime,
                    'totalVentaGravada': total_venta_gravada,
                    'sumatoriaIgv': str(round(float(sumatoria_ivg),2)),
                    'totalVenta': total_venta,
                    'tipoMoneda': invoice.currency_id.name,
                    'items':invoice_items,
                    'sol':{
                            'usuario':invoice.company_id.sol_username,
                            'clave':invoice.company_id.sol_password
                          }
                    }
            #
            xmlPath = os.path.dirname(os.path.abspath(__file__))+'/xml'
            SunatService = Service()
            SunatService.setXMLPath(xmlPath)
            SunatService.fileName = str(invoice.company_id.sol_ruc)+"-08-"+str(serieConsecutivoString)+"-"+str(serieConsecutivo)
            SunatService.initSunatAPI(invoice.company_id.api_mode, "sendBill")
            sunatResponse = SunatService.processDebitNote(data)

            #with open('/home/rockscripts/Documents/data1.json', 'w') as outfile:
            #    json.dump(sunatResponse, outfile)
                        
            if(sunatResponse["status"] == "OK"):
                self.api_message = "ESTADO: "+str(sunatResponse["status"])+"\n"+"REFERENCIA: "+str(sunatResponse["body"]["referencia"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"]["description"])
                return super(account_invoice, self).invoice_validate()
            else:
                errorMessage = "ESTADO: "+str(sunatResponse["status"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"])+"\n"+"CÓDIGO ERROR: "+str(sunatResponse["code"])
                raise Warning(errorMessage)
            

        elif(tipo_documento_consultar=="BOL"):
            invoice_items = []
            total_venta_gravada = 0.0
            total_venta = 0.0
            sumatoria_ivg = 0.0
            
            for invoice in self:            
                items = invoice.invoice_line_ids
                for item in items:
                    index = 0
                    for taxes in invoice.tax_line_ids:
                    
                        if(index==0):
                            impuesto = taxes.tax_id.amount/100
                            valor_venta = (item.price_unit * item.quantity)                        
                            monto_afectacion_IGV = valor_venta * impuesto                   
                            precio_unitario = (item.price_unit * impuesto) + item.price_unit
                            invoice_item = {
                                                'cantidad':str(item.quantity), 
                                                'descripcion':item.name, 
                                                'valorVenta':valor_venta, 
                                                'valorUnitario':item.price_unit, 
                                                'precioVentaUnitario':precio_unitario, 
                                                'tipoPrecioVentaUnitario':'01', 
                                                'montoAfectacionIgv':monto_afectacion_IGV, 
                                                'tipoAfectacionIgv':'10',
                                                'unidadMedidaCantidad':"ZZ",
                                            }
                            invoice_items.append(invoice_item)
                            total_venta_gravada += valor_venta
                            total_venta += precio_unitario
                            sumatoria_ivg += monto_afectacion_IGV
                            index=index+1

            #old - serieParts = str(invoice.number).split("/")
            #old - serieConsecutivo = serieParts[2]
            #old - serieConsecutivo = serieConsecutivo[1:]
            
            serieParts = str(invoice.number).split("-")             
            serieConsecutivoString = serieParts[0]
            serieConsecutivo = serieParts[1]
            currentDateTime = datetime.now()
            currentTime = currentDateTime.strftime("%H:%M:%S")
            data = {
                    'serie': str(serieConsecutivoString),
                    "numero":str(serieConsecutivo),
                    "emisor":{
                        "tipo":6,
                        "nro":invoice.company_id.sol_ruc,
                        "nombre":invoice.company_id.name,
                        "direccion":invoice.company_id.street,
                        "ciudad":invoice.company_id.city,
                        "departamento":invoice.company_id.state_id.name,
                        "codigoPostal":invoice.company_id.zip,
                        "codigoPais":invoice.company_id.country_id.code
                     },
                    "receptor": {
                            "tipo": 6,
                            "nro": invoice.partner_id.vat,
                            "nombre":invoice.partner_id.name,
                            "direccion":invoice.partner_id.street,
                        },
                    "fechaEmision":str(invoice.date_invoice).replace("/","-",3),
                    "fechaVencimiento":str(invoice.date_due).replace("/","-",3),
                    "horaEmision":currentTime,
                    'totalVentaGravada': total_venta_gravada,
                    'sumatoriaIgv': str(round(float(sumatoria_ivg),2)),
                    'totalVenta': total_venta,
                    'tipoMoneda': invoice.currency_id.name,
                    'items':invoice_items,
                    'sol':{
                            'usuario':invoice.company_id.sol_username,
                            'clave':invoice.company_id.sol_password
                          }
                    }
            #
            xmlPath = os.path.dirname(os.path.abspath(__file__))+'/xml'
            SunatService = Service()
            SunatService.setXMLPath(xmlPath)
            SunatService.setXMLPath(xmlPath)
            SunatService.fileName = str(invoice.company_id.sol_ruc)+"-03-"+str(serieConsecutivoString)+"-"+str(serieConsecutivo)
            SunatService.initSunatAPI(invoice.company_id.api_mode, "sendBill")
            sunatResponse = SunatService.processTicket(data)

            #with open('/home/rockscripts/Documents/data1.json', 'w') as outfile:
            #    json.dump(sunatResponse, outfile)
                        
            if(sunatResponse["status"] == "OK"):
                self.api_message = "ESTADO: "+str(sunatResponse["status"])+"\n"+"REFERENCIA: "+str(sunatResponse["body"]["referencia"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"]["description"])
                return super(account_invoice, self).invoice_validate()
            else:
                errorMessage = "ESTADO: "+str(sunatResponse["status"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"])+"\n"+"CÓDIGO ERROR: "+str(sunatResponse["code"])
                raise Warning(errorMessage)
                
        else:
            #FOR INVOICES
            invoice_items = []
            total_venta_gravada = 0.0
            total_venta = 0.0
            sumatoria_ivg = 0.0
            
            for invoice in self:            
                items = invoice.invoice_line_ids
                for item in items:
                    index = 0
                    for taxes in invoice.tax_line_ids:
                    
                        if(index==0):
                            impuesto = taxes.tax_id.amount/100
                            valor_venta = (item.price_unit * item.quantity)                        
                            monto_afectacion_IGV = valor_venta * impuesto                   
                            precio_unitario = (item.price_unit * impuesto) + item.price_unit
                            invoice_item = {
                                                'cantidad':str(item.quantity),
                                                'descripcion':item.name, 
                                                'valorVenta':valor_venta, 
                                                'valorUnitario':item.price_unit, 
                                                'precioVentaUnitario':precio_unitario, 
                                                'tipoPrecioVentaUnitario':'01', 
                                                'montoAfectacionIgv':monto_afectacion_IGV, 
                                                'tipoAfectacionIgv':'10',
                                                'unidadMedidaCantidad':"ZZ",
                                            }
                            invoice_items.append(invoice_item)
                            total_venta_gravada += valor_venta
                            total_venta += precio_unitario
                            sumatoria_ivg += monto_afectacion_IGV
                            index=index+1

            serieParts = str(invoice.number).split("-")             
            serieConsecutivoString = serieParts[0]
            serieConsecutivo = serieParts[1]
            currentDateTime = datetime.now()
            currentTime = currentDateTime.strftime("%H:%M:%S")
            data = {
                    'serie': str(serieConsecutivoString),
                    "numero":str(serieConsecutivo),
                    "emisor":{
                        "tipo":6,
                        "nro":invoice.company_id.sol_ruc,
                        "nombre":invoice.company_id.name,
                        "direccion":invoice.company_id.street,
                        "ciudad":invoice.company_id.city,
                        "departamento":invoice.company_id.state_id.name,
                        "codigoPostal":invoice.company_id.zip,
                        "codigoPais":invoice.company_id.country_id.code
                     },
                    "receptor": {
                            "tipo": 6,
                            "nro": invoice.partner_id.vat,
                            "nombre":invoice.partner_id.name,
                            "direccion":invoice.partner_id.street,
                        },
                    "fechaEmision":str(invoice.date_invoice).replace("/","-",3),
                    "fechaVencimiento":str(invoice.date_due).replace("/","-",3),
                    "horaEmision":currentTime,
                    'totalVentaGravada': total_venta_gravada,
                    'sumatoriaIgv': str(round(float(sumatoria_ivg),2)),
                    'totalVenta': total_venta,
                    'tipoMoneda': invoice.currency_id.name,
                    'items':invoice_items,
                    'sol':{
                            'usuario':invoice.company_id.sol_username,
                            'clave':invoice.company_id.sol_password
                          }
                    }   
            #with open('/opt/odoo/custom-addons/sfact_addon/data.json', 'w') as outfile:
            #     json.dump(data, outfile)
            xmlPath = os.path.dirname(os.path.abspath(__file__))+'/xml'
            SunatService = Service()
            SunatService.setXMLPath(xmlPath)
            SunatService.setXMLPath(xmlPath)
            SunatService.fileName = str(invoice.company_id.sol_ruc)+"-01-"+str(serieConsecutivoString)+"-"+str(serieConsecutivo)
            SunatService.initSunatAPI(invoice.company_id.api_mode, "sendBill")
            sunatResponse = SunatService.processInvoice(data)

            #with open('/home/rockscripts/Documents/data1.json', 'w') as outfile:
            #    json.dump(sunatResponse, outfile)
                        
            if(sunatResponse["status"] == "OK"):
                self.api_message = "ESTADO: "+str(sunatResponse["status"])+"\n"+"REFERENCIA: "+str(sunatResponse["body"]["referencia"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"]["description"])
                return super(account_invoice, self).invoice_validate()
            else:
                errorMessage = "ESTADO: "+str(sunatResponse["status"])+"\n"+"DESCRIPCIÓN: "+str(sunatResponse["body"])+"\n"+"CÓDIGO ERROR: "+str(sunatResponse["code"])
                raise Warning(errorMessage)