import logging

from odoo.upgrade import util
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # Log the start of the column creation process
    _logger.info('Creating columns from previous version')

    # Create new columns in the 'sale_order' table
    util.create_column(cr, 'sale_order', 'parent_id', 'integer')
    util.create_column(cr, 'sale_order', 'child_recurring_total', 'double-precision')
    util.create_column(cr, 'sale_order', 'amount_at_start', 'double-precision')

    # Log that column creation is complete
    _logger.info('Columns created successfully')

    # Execute the SQL update to populate the new columns
    cr.execute('''
        UPDATE sale_order
        SET 
            parent_id = sale_subscription.parent_id,
            child_recurring_total = sale_subscription.child_recurring_total,
            amount_at_start = sale_subscription.amount_at_start
        FROM sale_subscription
        WHERE sale_subscription.new_sale_order_id = sale_order.id
    ''')

    # Log the completion of the update process
    _logger.info('Finished updating sale_order table')

