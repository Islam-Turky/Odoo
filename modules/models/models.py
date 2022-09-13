# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import timedelta

class modules(models.Model):

    _name = 'modules.course'
    _description = "modules courses"
    name = fields.Char(string="Courses", required=True, help='My First field')
    S_name = fields.Char(string="Description", required="True", help='My Second Field')
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="responsible")
    sessions_ids = fields.One2many('frameworks', 'course_id', string="Sessions")
    color = fields.Integer(string="color")
    # course_id = fields.One2many('modules.student', 'Course_in_id')

class Frameworks(models.Model):
    _name = 'frameworks'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sessions For ALl'
    _rec_name = 'course_id'

    name = fields.Char(string='Sessions', required=True, index=True)
    rate = fields.Integer(string='Rate')
    start_date = fields.Date(default=fields.Date.today)
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    duration = fields.Float(digits=(7, 3), help="duration in days")
    course_id = fields.Many2one('modules.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    seats = fields.Integer(string="Seats")
    taken_seats = fields.Float(string="Taken Seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    attendees_count = fields.Integer(string="Attendee Count", store=True, compute='_get_attendees_count')
    image = fields.Binary(string="Image")
    color = fields.Integer(string="color")
    name_second = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_second', _('New') == _('New')):
            vals['name_second'] = self.env['ir.sequence'].next_by_code('modules.sequence') or _('New')
        result = super(Frameworks, self).create(vals)
        return result

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not(r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            r.duration = (r.end_date - r.start_date).days + 1

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = 100.0 * len(record.attendee_ids)/record.seats

    @api.onchange('seats','attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'Seats' Value",
                    'message': "The Number Of Available Seats May Not Be Negative",
                        },
                }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too Many Attendees",
                    'message': "Increase Seats Or Remove Excess Attendees",
                         },
                }

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = ' %s ' % (rec.name)
    #         result.append((rec.id, name))
    #     return result

    @api.constrains('instructor_id','attendee_ids')
    def _check_instructor(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A Session's Instructor can't Be Attendee")




