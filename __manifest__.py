# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Flyt Remanufacturing",
    "version": "18.0.0.0.0",
    "summary": "Enhances MRP and Inventory to support remanufacturing operations with serial tracking",
    "description": """
    Flyt Remanufacturing
    -----------------------
    This module extends Odoo's Manufacturing (MRP) and Inventory (Stock) application to support remanufacturing workflows.
    It introduces a new 'Remanufacturing' order type with custom logic for handling stock moves based on
    serial numbers and defined operations: Add, Remove, and Recycle.
    """,
    "category": 'Custom',
    "author": "Odoo PS",
    "website": "https://www.odoo.com",
    "license": "LGPL-3",
    "depends": ['mrp'],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_production_views.xml",
        "views/mrp_bom_views.xml",
        "views/stock_lot_view.xml",
        "views/flyt_stock_lot_link_views.xml",
    ],
    "installable": True,
}
