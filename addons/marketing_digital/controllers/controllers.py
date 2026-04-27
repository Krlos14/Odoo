# -*- coding: utf-8 -*-
# from odoo import http


# class MarketingDigital(http.Controller):
#     @http.route('/marketing_digital/marketing_digital', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_digital/marketing_digital/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_digital.listing', {
#             'root': '/marketing_digital/marketing_digital',
#             'objects': http.request.env['marketing_digital.marketing_digital'].search([]),
#         })

#     @http.route('/marketing_digital/marketing_digital/objects/<model("marketing_digital.marketing_digital"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_digital.object', {
#             'object': obj
#         })

