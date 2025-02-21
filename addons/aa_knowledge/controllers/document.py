from odoo import http
from odoo.http import request


class DocumentationController(http.Controller):

    @http.route('/docs', auth='user', website=True)
    def docs_list(self, search=None):
        """Prikazuje samo kategorije i dokumente kojima korisnik ima pristup"""
        user = request.env.user
        
        # Filtriramo kategorije na osnovu user_id polja
        categories = request.env['documentation.category'].search([('user_id', 'in', [user.id])])

        # Filtriramo dokumente samo iz dozvoljenih kategorija
        allowed_category_ids = categories.ids
        docs = request.env['documentation.document'].search([('category_id', 'in', allowed_category_ids)])

        # Ako postoji pretraga, dodatno filtriramo dokumente
        if search:
            docs = docs.filtered(lambda d: search.lower() in d.title.lower() or search.lower() in d.content.lower())

        return request.render('aa_knowledge.docs_template', {
            'categories': categories,
            'docs': docs,
            'search': search
        })
    
    @http.route('/docs/<int:doc_id>', auth='user', website=True)
    def docs_detail(self, doc_id):
        """Prikazuje detalje dokumenta samo ako korisnik ima pristup kategoriji"""
        user = request.env.user
        document = request.env['documentation.document'].browse(doc_id)

        # Ako dokument ne postoji, vrati 404
        if not document.exists():
            return request.not_found()
        
        # Proveravamo da li korisnik ima pravo da vidi kategoriju ovog dokumenta
        allowed_categories = request.env['documentation.category'].search([('user_id', 'in', [user.id])])
        allowed_category_ids = allowed_categories.ids

        if document.category_id.id not in allowed_category_ids:
            return request.render('aa_knowledge.error_403_template')  # Prikazuje 403 Forbidden ako korisnik nema pristup

        # Filtriramo vidljive kategorije za sidebar
        categories = request.env['documentation.category'].search([('user_id', 'in', [user.id])])

        return request.render('aa_knowledge.doc_detail_template', {
            'categories': categories,
            'document': document,
        })
