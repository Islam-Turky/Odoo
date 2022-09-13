from odoo import fields , models

class student(models.Model):
    _name = 'modules.student'
    _description = 'Student page'

    name = fields.Char(string='Student Name', requierd=True, index=True)
    Gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], default='male', string='Gender')
    age = fields.Integer(string='Age', required=True)
    Course_in_id = fields.Many2one('modules.course', ondelete='cascade', string='Student Courses', required=True)

    image = fields.Binary(attachment=True)
