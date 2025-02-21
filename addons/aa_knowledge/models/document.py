from odoo import models, fields, api
from odoo.exceptions import AccessError


class Documentation(models.Model):
    _name = "documentation.document"
    _description = "Documentation"

    title = fields.Char(required=True)
    content = fields.Html(required=True)
    category_id = fields.Many2one("documentation.category", string="Category")
    author_id = fields.Many2one("res.users", string="Author", default=lambda self: self.env.user)
    
    def check_access_rights(self, operation, raise_exception=True):
        if not self.env.user or self.env.user._is_public():
            if raise_exception:
                raise AccessError("You must be logged in to view the document.")
            return False
        return super(Documentation, self).check_access_rights(operation, raise_exception)

    @api.model
    def get_allowed_documents(self):
        """Vrati samo dokumente iz kategorija kojima korisnik ima pristup"""
        allowed_categories = self.env["documentation.category"].get_allowed_categories()
        return self.search([('category_id', 'in', allowed_categories.ids)])
    
class DocumentationCategory(models.Model):
    _name = "documentation.category"
    _description = "Documentation Category"

    name = fields.Char(required=True)
    document_ids = fields.One2many("documentation.document", "category_id", string="Documents")
    user_id = fields.Many2many("res.users", string="Users", help="Select a user")
    
    @api.model
    def get_allowed_categories(self):
        """Vrati samo kategorije kojima korisnik ima pristup"""
        return self.search([('user_id', 'in', [self.env.user.id])])