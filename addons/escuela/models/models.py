# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'escuela.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre', required=True)