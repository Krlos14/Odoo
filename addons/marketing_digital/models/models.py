# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Servicio(models.Model):
    _name = 'marketing.servicio'
    _description = 'Servicio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True, tracking=True)
    descripcion = fields.Text(string='Descripción')
    precio = fields.Float(string='Precio (€)', required=True, tracking=True)
    tipo = fields.Selection([
        ('seo', 'SEO'),
        ('disenio_web', 'Diseño Web'),
        ('redes_sociales', 'Redes Sociales'),
        ('email_marketing', 'Email Marketing'),
        ('publicidad', 'Publicidad Online'),
    ], string='Tipo de Servicio', required=True, default='seo')
    activo = fields.Boolean(string='Activo', default=True)


class Tarea(models.Model):
    _name = 'marketing.tarea'
    _description = 'Tarea'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre de la Tarea', required=True, tracking=True)
    descripcion = fields.Text(string='Descripción')
    proyecto_id = fields.Many2one('marketing.proyecto', string='Proyecto', required=True, ondelete='cascade')
    responsable_id = fields.Many2one('res.users', string='Responsable')
    fecha_limite = fields.Date(string='Fecha Límite')
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ], string='Estado', default='pendiente', tracking=True)
    prioridad = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Alta'),
    ], string='Prioridad', default='0')

    def _actualizar_progreso_proyecto(self):
        for tarea in self:
            proyecto = tarea.proyecto_id
            if proyecto:
                total = len(proyecto.tarea_ids)
                completadas = len(proyecto.tarea_ids.filtered(lambda t: t.estado == 'completada'))
                progreso = int((completadas / total) * 100) if total > 0 else 0
                proyecto.sudo().write({
                    'progreso': progreso,
                    'num_tareas': total,
                    'num_tareas_completadas': completadas,
                })

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._actualizar_progreso_proyecto()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._actualizar_progreso_proyecto()
        return result

    def unlink(self):
        proyectos = self.mapped('proyecto_id')
        result = super().unlink()
        for proyecto in proyectos:
            total = len(proyecto.tarea_ids)
            completadas = len(proyecto.tarea_ids.filtered(lambda t: t.estado == 'completada'))
            progreso = int((completadas / total) * 100) if total > 0 else 0
            proyecto.sudo().write({
                'progreso': progreso,
                'num_tareas': total,
                'num_tareas_completadas': completadas,
            })
        return result


class Proyecto(models.Model):
    _name = 'marketing.proyecto'
    _description = 'Proyecto'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre del Proyecto', required=True, tracking=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True, tracking=True)
    email_cliente = fields.Char(string='Email del Cliente', compute='_compute_email_cliente', store=True)
    telefono_cliente = fields.Char(string='Teléfono del Cliente', compute='_compute_telefono_cliente', store=True)
    fecha_inicio = fields.Date(string='Fecha de Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha de Fin', required=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador', tracking=True)
    prioridad = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgente'),
    ], string='Prioridad', default='0')
    progreso = fields.Integer(string='Progreso (%)', default=0)
    descripcion = fields.Text(string='Descripción del Proyecto')
    servicio_ids = fields.Many2many('marketing.servicio', string='Servicios Contratados')
    tarea_ids = fields.One2many('marketing.tarea', 'proyecto_id', string='Tareas')
    presupuesto = fields.Float(string='Presupuesto (€)', tracking=True)
    importe_total = fields.Float(string='Importe Total Servicios (€)', compute='_compute_importe_total', store=True)
    num_tareas = fields.Integer(string='Nº Tareas', default=0)
    num_tareas_completadas = fields.Integer(string='Tareas Completadas', default=0)
    color = fields.Integer(string='Color')

    @api.depends('cliente_id')
    def _compute_email_cliente(self):
        for rec in self:
            rec.email_cliente = rec.cliente_id.email if rec.cliente_id else ''

    @api.depends('cliente_id')
    def _compute_telefono_cliente(self):
        for rec in self:
            rec.telefono_cliente = rec.cliente_id.phone if rec.cliente_id else ''

    @api.depends('servicio_ids')
    def _compute_importe_total(self):
        for rec in self:
            rec.importe_total = sum(rec.servicio_ids.mapped('precio'))

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for rec in self:
            if rec.fecha_inicio and rec.fecha_fin:
                if rec.fecha_fin < rec.fecha_inicio:
                    raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

    @api.onchange('cliente_id')
    def _onchange_cliente(self):
        if self.cliente_id:
            self.email_cliente = self.cliente_id.email
            self.telefono_cliente = self.cliente_id.phone

    def action_iniciar(self):
        self.estado = 'en_curso'

    def action_finalizar(self):
        self.estado = 'finalizado'
        self.progreso = 100

    def action_cancelar(self):
        self.estado = 'cancelado'

    def action_borrador(self):
        self.estado = 'borrador'
        self.progreso = 0