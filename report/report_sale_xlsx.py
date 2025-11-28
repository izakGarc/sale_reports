from odoo.addons.report_xlsx_helper.report.report_xlsx_format import (
    FORMATS,
    XLS_HEADERS,
)
from odoo import models
from odoo.fields import Date as odate
from odoo.exceptions import ValidationError


class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.sale_reports.report_sale_xlsx'
    _description = 'Report xlsx Sale_Order'
    _inherit = 'report.report_xlsx.abstract'


    def _sale_order_report(self, workbook, ws, ws_params, data, sale_orders):

        domain = data['domain']
        
        orders = self.env['sale.order'].search(domain)


        if not orders:
            raise ValidationError("No records found.")

        border_grey = '#D3D3D3'
        border = {'border': True, 'border_color': border_grey}
        theader = dict(border, bold=True)
        bg_yellow = '#00A300'
        theader_yellow = dict(theader, bg_color=bg_yellow)

        format_theader_green_left = workbook.add_format(theader_yellow)

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(XLS_HEADERS['xls_headers']['standard'])
        ws.set_footer(XLS_HEADERS['xls_footers']['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section='header',
            default_format=format_theader_green_left,
        )
        ws.freeze_panes(row_pos, 0)

        wl = ws_params['wanted_list']


        for record in orders:
            for line in record.order_line:
                row_pos = self._write_line(
                    ws,
                    row_pos,
                    ws_params,
                    col_specs_section='data',
                    render_space={
                        'date_order': record.date_order.strftime('%d-%m-%Y %H:%M:%S'),
                        'partner_id': record.partner_id.name,
                        'ref': record.name,
                        'email': record.partner_id.email,
                        'channel_ids': ', '.join(record.channel_ids.mapped('name')) if hasattr(record, 'channel_ids') else '',
                        'zip': record.partner_id.zip,
                        'street': record.partner_id.street,
                        'street2': record.partner_id.street2,
                        'l10n_mx_edi_colony': record.partner_id.l10n_mx_edi_colony,
                        'city': record.partner_id.city,
                        'house_ref': record.partner_id.house_ref,
                        'country_id': record.partner_id.country_id.name,
                        'phone': record.partner_id.phone,                        
                        'product_id': line.product_id.name,
                        'sku': line.product_id.default_code,
                        'product_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal,
                        'price_tax': line.price_tax,
                        'price_total': line.price_total,
                    },
                    default_format=FORMATS['format_tcell_left'],
                )
                    
            
    def _get_ws_params(self, wb, data, sale_orders):

        sale_order_template = {
            'partner_id': {
                'header': {
                    'value': 'Cliente',
                },
                'data': {
                    'value': self._render('partner_id'),
                },
                'width': 30,
            },
            'ref': {
                'header': {
                    'value': 'Referencia de orden',
                },
                'data': {
                    'value': self._render('ref'),
                },
                'width': 20,
            },
            'date_order': {
                'header': {
                    'value': 'Fecha de Orden',
                },
                'data': {
                    'value': self._render('date_order'),
                },
                'width': 15,
            },
            'email': {
                'header': {
                    'value': 'Email',
                },
                'data': {
                    'value': self._render('email'),
                },
                'width': 30,
            },
            'channel_ids': {
                'header': {
                    'value': 'Canal',
                },
                'data': {
                    'value': self._render('channel_ids'),
                },
                'width': 20,
            },
            'zip': {
                'header': {
                    'value': 'CP',
                },
                'data': {
                    'value': self._render('zip'),
                },
                'width': 10,
            },
            'street': {
                'header': {
                    'value': 'Calle',
                },
                'data': {
                    'value': self._render('street'),
                },
                'width': 35,
            },
            'street2': {
                'header': {
                    'value': 'Entre calles',
                },
                'data': {
                    'value': self._render('street2'),
                },
                'width': 25,
            },
            'l10n_mx_edi_colony': {
                'header': {
                    'value': 'Colonia',
                },
                'data': {
                    'value': self._render('l10n_mx_edi_colony'),
                },
                'width': 25,
            },
            'city': {
                'header': {
                    'value': 'Ciudad',
                },
                'data': {
                    'value': self._render('city'),
                },
                'width': 20,
            },
            'house_ref': {
                'header': {
                    'value': 'Referencia',
                },
                'data': {
                    'value': self._render('house_ref'),
                },
                'width': 30,
            },
            'country_id': {
                'header': {
                    'value': 'País',
                },
                'data': {
                    'value': self._render('country_id'),
                },
                'width': 15,
            },
            'phone': {
                'header': {
                    'value': 'Teléfono',
                },
                'data': {
                    'value': self._render('phone'),
                },
                'width': 15,
            },
            # CAMPOS DE LÍNEA
            'sku': {
                'header': {
                    'value': 'SKU',
                },
                'data': {
                    'value': self._render('sku'),
                },
                'width': 35,
            },
            'product_id': {
                'header': {
                    'value': 'Producto',
                },
                'data': {
                    'value': self._render('product_id'),
                },
                'width': 35,
            },
            'product_qty': {
                'header': {
                    'value': 'Cantidad',
                },
                'data': {
                    'value': self._render('product_qty'),
                    'format': wb.add_format({'num_format': '#,##0.00'}),
                },
                'width': 12,
            },
            'price_unit': {
                'header': {
                    'value': 'Precio unitario',
                },
                'data': {
                    'value': self._render('price_unit'),
                    'format': wb.add_format({'num_format': '$#,##0.00'}),
                },
                'width': 15,
            },
            'price_subtotal': {
                'header': {
                    'value': 'Subtotal',
                },
                'data': {
                    'value': self._render('price_subtotal'),
                    'format': wb.add_format({'num_format': '$#,##0.00'}),
                },
                'width': 15,
            },
            'price_tax': {
                'header': {
                    'value': 'Impuestos',
                },
                'data': {
                    'value': self._render('price_tax'),
                    'format': wb.add_format({'num_format': '$#,##0.00'}),
                },
                'width': 15,
            },
            'price_total': {
                'header': {
                    'value': 'Total',
                },
                'data': {
                    'value': self._render('price_total'),
                    'format': wb.add_format({'num_format': '$#,##0.00'}),
                },
                'width': 15,
            },
        }

        wanted_list = sale_order_template.keys()
        ws_params = {
            'ws_name': 'Pedidos',
            'generate_ws_method': '_sale_order_report',
            'title': 'Reporte de Pedidos',
            'wanted_list': wanted_list,
            'col_specs': sale_order_template,
        }

        return [ws_params]
    