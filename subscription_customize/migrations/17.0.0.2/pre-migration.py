from odoo.upgrade import util


def migrate(cr, version):

    cr.execute("UPDATE sale_order "
               "SET sale_order.amount_at_start = sale_subscription.amount_at_start"
               "FROM sale_subcription"
               "WHERE sale_order.id = sale_subscription.new_sale_order_id;")

    cr.execute("UPDATE sale_order "
              "SET sale_order.parent_id = sale_subscription.parent_id"
              "FROM sale_subcription "
              "WHERE sale_order.id = sale_subscription.new_sale_order_id;")

    cr.execute("UPDATE sale_order "
              "SET sale_order.child_ids = sale_subscription.child_ids "
              "FROM sale_subcription"
              "WHERE sale_order.id = sale_subscription.new_sale_order_id;")

    cr.execute("UPDATE sale_order "
              "SET sale_order.child_recurring_total = sale_subscription.child_recurring_total"
              "FROM sale_subcription"
              "WHERE sale_order.id = sale_subscription.new_sale_order_id;")
