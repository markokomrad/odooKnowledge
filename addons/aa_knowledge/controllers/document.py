from odoo import http
from odoo.http import request

class DocumentationController(http.Controller):

    @http.route('/docs', auth='public', website=True)
    def docs_list(self, search=None):
        # Check if the user is logged in
        if not request.env.user or request.env.user._is_public():
            # User is not logged in or is a public user, show login message
            return request.render('aa_knowledge.login_message_template')
        
        # User is logged in, fetch categories and documents
        categories = request.env['documentation.category'].search([])

        # If there's a search term, filter the documents
        if search:
            docs = request.env['documentation.document'].search([
                ('title', 'ilike', search) | ('content', 'ilike', search)
            ])
        else:
            docs = request.env['documentation.document'].search([])

        # Pass categories and documents to the template
        return request.render('aa_knowledge.docs_template', {
            'categories': categories,
            'docs': docs,
            'search': search  # Pass the search term to the template
        })
    
    @http.route('/docs/<int:doc_id>', auth='public', website=True)
    def docs_detail(self, doc_id):
        # Check if the user is logged in
        if not request.env.user or request.env.user._is_public():
            # User is not logged in or is a public user, show login message
            return request.render('aa_knowledge.login_message_template')

        # Fetch the document by its ID
        document = request.env['documentation.document'].browse(doc_id)
        
        # Check if the document exists
        if not document.exists():
            return request.not_found()  # Return a 404 page if document is not found

        categories = request.env['documentation.category'].search([])  # Get all categories
        
        # Ensure the 'document' is passed correctly to the template
        return request.render('aa_knowledge.doc_detail_template', {
            'categories': categories,
            'document': document,  # Passing document to the template
        })
