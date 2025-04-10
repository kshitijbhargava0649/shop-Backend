from marshmallow import Schema, fields, validate

class UserSignupSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True) 