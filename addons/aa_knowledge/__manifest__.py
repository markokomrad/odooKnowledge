{
    'name': "WikiDocs",
    'summary': 'Knowledge app',
    'description': "Knowledge based app similar to Wiki",
    'category': 'custom_apps',
    'version': '1.0',
    'depends': ['base', 'website'],
    'data': [
        'views/menu.xml',
        'views/document_views.xml',
        'views/category_views.xml',
        'views/templates.xml',
        'views/public_view.xml',
        'views/forbidden_view.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            'aa_knowledge/static/src/css/custom_style.css',
        ],
    },
    'images': ['static/description/icon.png'],
    'application': True,
    'license': 'LGPL-3',
}