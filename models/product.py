import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .product_category_xref import products_categories_association_table


class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    product_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id"), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Categories.category_id", ondelete="CASCADE"), nullable=True)

    company = db.relationship("Companies", foreign_keys='[Products.company_id]', back_populates='products')
    categories = db.relationship("Categories",secondary=products_categories_association_table, back_populates='products', cascade='all,delete')

    def __init__(self, product_name, description, price, company_id,active):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.company_id = company_id
        self.active = active

    def new_product_obj():
        return Products("","",0,"",True)
    
class ProductsSchema(ma.Schema):
    class Meta:
        fields=['product_id','product_name','description','price','categories','active','company_id','company']
    company = ma.fields.Nested("CompaniesSchema",exclude=['products'])
    categories = ma.fields.Nested("CategoriesSchema",exclude=['products'])


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)