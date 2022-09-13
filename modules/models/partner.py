from odoo import fields , models
class partner(models.Model):
    _inherit = 'res.partner'
    instructor = fields.Boolean("instructor",default=False)
    session_ids = fields.Many2many('frameworks',string="Attended Sessions",readonly=True)