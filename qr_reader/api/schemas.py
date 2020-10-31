from marshmallow import Schema, fields, validate


class  QR_Schema(Schema):
    id = fields.String(validate=validate.Length(min=24, max=24), dump_only=True)
    id_files = fields.Integer(required=True)
    name = fields.String(validate=validate.Length(min=2, max=255))
    telephone = fields.String(validate=validate.Length(min=10, max=12))
