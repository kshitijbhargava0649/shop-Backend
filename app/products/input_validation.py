from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    shopify_id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()
    price = fields.Float(required=True, validate=validate.Range(min=0))
    sku = fields.Str()
    image_url = fields.Str()

class ProductUpdateSchema(ProductSchema):
    title = fields.Str(validate=validate.Length(min=1))
    price = fields.Float(validate=validate.Range(min=0))
