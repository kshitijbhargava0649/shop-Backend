from datetime import datetime
from mongoengine import (
    Document, StringField, FloatField, 
    DateTimeField, ListField, DictField
)

class Product(Document):
    shopify_id = StringField(required=True, unique=True)
    title = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    sku = StringField()
    image_url = StringField()
 
    
    meta = {
        'collection': 'identifier_products',
        # 'indexes': ['shopify_id', 'sku']
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'shopify_id': self.shopify_id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'sku': self.sku,
            'image_url': self.image_url,
        } 