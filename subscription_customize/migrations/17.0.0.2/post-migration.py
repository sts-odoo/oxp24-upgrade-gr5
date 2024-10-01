from odoo.upgrade import util


from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    # SQL updates for simple fields
    cr.execute("""
        UPDATE sale_order so
        SET amount_at_start = ss.amount_at_start
        FROM sale_subscription ss
        WHERE so.id = ss.new_sale_order_id;
    """)

    cr.execute("""
        UPDATE sale_order so
        SET child_recurring_total = ss.child_recurring_total
        FROM sale_subscription ss
        WHERE so.id = ss.new_sale_order_id;
    """)

    # ORM updates for relational fields
    env = api.Environment(cr, SUPERUSER_ID, {})
    subscriptions = env['sale.subscription'].search([])

    for sub in subscriptions:
        sale_order = env['sale.order'].browse(sub.new_sale_order_id)
        if sale_order.exists():
            # Update parent_id
            if sub.parent_id and sub.parent_id.new_sale_order_id:
                parent_sale_order = env['sale.order'].browse(sub.parent_id.new_sale_order_id)
                if parent_sale_order.exists():
                    sale_order.parent_id = parent_sale_order.id
                else:
                    sale_order.parent_id = False
            else:
                sale_order.parent_id = False

            # Update child_ids
            child_sale_order_ids = [
                child_sub.new_sale_order_id
                for child_sub in sub.child_ids
                if child_sub.new_sale_order_id
            ]
            child_sale_orders = env['sale.order'].browse(child_sale_order_ids).filtered('id')

            if child_sale_orders:
                sale_order.child_ids = [(6, 0, child_sale_orders.ids)]
            else:
                sale_order.child_ids = [(5, 0, 0)]  # Clear existing child_ids

