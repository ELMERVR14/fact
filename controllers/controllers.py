# -*- coding: utf-8 -*-
from odoo import http

# class FactOnline(http.Controller):
#     @http.route('/fact_online/fact_online/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fact_online/fact_online/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fact_online.listing', {
#             'root': '/fact_online/fact_online',
#             'objects': http.request.env['fact_online.fact_online'].search([]),
#         })

#     @http.route('/fact_online/fact_online/objects/<model("fact_online.fact_online"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fact_online.object', {
#             'object': obj
#         })