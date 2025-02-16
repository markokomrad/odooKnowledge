from odoo import models, fields
from odoo.exceptions import AccessError


class Documentation(models.Model):
    _name = "documentation.document"
    _description = "Documentation"

    title = fields.Char(required=True)
    content = fields.Html(required=True)
    category_id = fields.Many2one("documentation.category", string="Category")
    author_id = fields.Many2one("res.users", string="Author", default=lambda self: self.env.user)
    
    # Access control login
    def check_access_rights(self, operation, raise_exception=True):
        if not self.env.user or self.env.user._is_public():
            if raise_exception:
                raise AccessError("You must be logged in to view the document.")
            return False
        return super(Documentation, self).check_access_rights(operation, raise_exception)

    
class DocumentationCategory(models.Model):
    _name = "documentation.category"
    _description = "Documentation Category"

    name = fields.Char(required=True)
    document_ids = fields.One2many("documentation.document", "category_id", string="Documents")

    