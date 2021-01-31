{
    'name': 'Pharmacy POS',

    'summary': """
        POS and Inventory System that can run locally.""",

    'description': """
        POS and Inventory System that can run locally because it runs on Docker.
    """,

    'author': "Bienvenido Villabroza",

    'version': '1',

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/product.xml',
    ],
    'demo': [
        'demo/product.xml',
    ],
}
