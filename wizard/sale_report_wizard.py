from datetime import datetime

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import pytz



class SaleReportWizard(models.TransientModel):
    _name = "sale.report.wizard"
    _description = "Sale Report Wizard"

    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    
    channel_ids = fields.Many2many(
        'partner.channel',
    )
    
    product_id = fields.Many2one(
        'product.product',
    )

    website_id = fields.Many2one(
        'website',
    )

    partner_id = fields.Many2one(
        'res.partner',
    )

    export_type = fields.Selection([
        ('xlxs', 'Excel'),
    ], default="xlxs", required=True)

    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
    )


    def _print_xlsx(self):
        domain = self._generate_domain()
        action = self.env.ref('sale_reports.action_report_sale_xlsx')\
            .report_action(None, data={
                'domain': domain
            })
        action.update({'close_on_report_download': True})
        return action

    def ok(self):
        return self._print_xlsx()

    def _generate_domain(self):

        domain = [
            ('state', '=', 'sale'),
        ]
        
        if self.date_start:
            user_tz = pytz.timezone(
                self.env.context.get('tz') or
                self.env.user.tz or
                'UTC'
            )
            date = datetime(self.date_start.year, self.date_start.month, self.date_start.day, 00, 00, 00, 00, user_tz)
            domain.append(('date_order', '>=', date))
            domain.append(('date_order', '>=', date))

        if self.date_end:
            user_tz = pytz.timezone(
                self.env.context.get('tz') or
                self.env.user.tz or
                'UTC'
            )
            date = datetime(self.date_end.year, self.date_end.month, self.date_end.day, 23, 59, 59, 00, user_tz)
            domain.append(('date_order', '<=', date))
            domain.append(('date_order', '<=', date))

        if hasattr(self, 'channel_ids') and self.channel_ids:
            domain.append(('channel_ids', 'in', self.channel_ids.ids))

        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))
            
        if self.website_id:
            domain.append(('website_id', '=', self.website_id.id))
            
        if self.product_id:
            domain.append(('product_id', '=', self.product_id.id))

        account_move = self.env['sale.order'].search(domain)
        if not account_move:
            raise ValidationError("No records found.")

        return domain
